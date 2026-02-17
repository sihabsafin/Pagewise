"""
PDF Intelligence — AI-Powered Document Query Platform
Built with Streamlit + Groq + AstraDB + LangChain
"""

import streamlit as st
import os
import time
import hashlib
from datetime import datetime

# ─── Page Config (MUST be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="PDF Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Injection ────────────────────────────────────────────────────────────
from styles import GLOBAL_CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ─── Lazy imports (after page config) ─────────────────────────────────────────
from backend import (
    initialize_vector_store,
    ingest_pdfs,
    build_rag_chain,
    query_with_streaming,
    clear_knowledge_base,
    get_retrieval_config,
)
from ui_components import (
    render_top_bar,
    render_empty_state,
    render_message_bubble,
    render_source_citations,
    render_dev_panel_content,
    render_document_card,
    render_skeleton_loader,
)

# ─── Session State Init ────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "messages": [],
        "documents": [],          # list of {name, pages, size, status, id}
        "vector_store": None,
        "chat_history": [],
        "query_mode": "⚡ Factual Answer",
        "k_chunks": 3,
        "strict_mode": False,
        "dev_mode": False,
        "show_clear_modal": False,
        "last_retrieval_info": None,
        "is_streaming": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ─── Credentials Check ────────────────────────────────────────────────────────
def check_credentials():
    missing = []
    for key in ["GROQ_API_KEY", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_API_ENDPOINT"]:
        if not (st.secrets.get(key) or os.environ.get(key)):
            missing.append(key)
    return missing

missing_creds = check_credentials()

# ─── Top Navigation Bar ───────────────────────────────────────────────────────
render_top_bar()

# ─── Clear Confirmation Modal ─────────────────────────────────────────────────
if st.session_state.show_clear_modal:
    st.markdown("""
    <div class="modal-overlay" id="clearModal">
      <div class="modal-box">
        <div class="modal-icon">⚠</div>
        <h3 class="modal-title">Clear Knowledge Base?</h3>
        <p class="modal-body">
          This will permanently delete all indexed documents and clear your conversation history.
          This action cannot be undone.
        </p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("Cancel", key="modal_cancel", use_container_width=True):
            st.session_state.show_clear_modal = False
            st.rerun()
    with col3:
        if st.button("Yes, Clear All", key="modal_confirm", type="primary", use_container_width=True):
            with st.spinner("Clearing knowledge base..."):
                clear_knowledge_base()
            st.session_state.show_clear_modal = False
            st.session_state.messages = []
            st.session_state.documents = []
            st.session_state.vector_store = None
            st.session_state.chat_history = []
            st.session_state.last_retrieval_info = None
            st.rerun()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:

    # Credentials warning
    if missing_creds:
        st.markdown(f"""
        <div class="cred-warning">
          <div class="cred-warning-title">⚠ Missing API Keys</div>
          <div class="cred-warning-body">Add to Streamlit Secrets:<br>
            {'<br>'.join(f'<code>{k}</code>' for k in missing_creds)}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── PDF Upload ────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section-label">DOCUMENTS</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdf_uploader",
        label_visibility="collapsed",
    )

    # Custom upload zone overlay (pure CSS, the native widget is hidden underneath)
    st.markdown("""
    <div class="upload-hint">
      Drop PDFs here · Max 200MB each
    </div>
    """, unsafe_allow_html=True)

    # Process uploaded files
    if uploaded_files:
        if not missing_creds:
            for file in uploaded_files:
                file_id = hashlib.md5(file.name.encode() + str(file.size).encode()).hexdigest()[:8]
                existing_ids = [d["id"] for d in st.session_state.documents]

                if file_id not in existing_ids:
                    # Add with indexing status
                    doc_entry = {
                        "id": file_id,
                        "name": file.name,
                        "size": file.size,
                        "pages": 0,
                        "status": "indexing",
                        "file": file,
                    }
                    st.session_state.documents.append(doc_entry)

            # Ingest any new documents
            new_docs = [d for d in st.session_state.documents if d["status"] == "indexing"]
            if new_docs:
                progress_placeholder = st.empty()
                with progress_placeholder:
                    result = ingest_pdfs(new_docs, progress_placeholder)
                progress_placeholder.empty()

                for doc in st.session_state.documents:
                    if doc["status"] == "indexing":
                        doc["status"] = "ready"
                        if doc["id"] in result:
                            doc["pages"] = result[doc["id"]].get("pages", 0)

                st.rerun()

    # Document cards
    if st.session_state.documents:
        to_remove = None
        for i, doc in enumerate(st.session_state.documents):
            col_doc, col_rm = st.columns([9, 1])
            with col_doc:
                render_document_card(doc)
            with col_rm:
                if st.button("✕", key=f"rm_{doc['id']}", help="Remove document"):
                    to_remove = i

        if to_remove is not None:
            st.session_state.documents.pop(to_remove)
            st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # ── Query Mode ────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section-label">QUERY MODE</div>', unsafe_allow_html=True)

    mode_options = [
        "⚡ Factual Answer",
        "📋 Detailed Explanation",
        "• Bullet Summary",
        "⚖ Compare Sections",
        "📊 Executive Summary",
    ]
    mode_tooltips = {
        "⚡ Factual Answer": "Returns a direct, concise answer to your question.",
        "📋 Detailed Explanation": "Provides thorough context and elaboration.",
        "• Bullet Summary": "Structures key points as a scannable bullet list.",
        "⚖ Compare Sections": "Identifies similarities and differences across sources.",
        "📊 Executive Summary": "Creates a high-level overview suitable for briefings.",
    }

    selected_mode = st.selectbox(
        "Query Mode",
        mode_options,
        index=mode_options.index(st.session_state.query_mode),
        label_visibility="collapsed",
    )
    if selected_mode != st.session_state.query_mode:
        st.session_state.query_mode = selected_mode

    st.markdown(
        f'<div class="mode-tooltip">{mode_tooltips[st.session_state.query_mode]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # ── Retrieval Controls ────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section-label">RETRIEVAL CONTROLS</div>', unsafe_allow_html=True)

    k = st.slider(
        "Retrieved Chunks",
        min_value=1,
        max_value=10,
        value=st.session_state.k_chunks,
        label_visibility="collapsed",
    )
    st.session_state.k_chunks = k
    st.markdown(
        f'<div class="slider-sublabel">Retrieving {k} most relevant passage{"s" if k != 1 else ""}</div>',
        unsafe_allow_html=True,
    )

    strict = st.toggle("Strict Mode", value=st.session_state.strict_mode)
    st.session_state.strict_mode = strict
    if strict:
        st.markdown(
            '<div class="toggle-sublabel">Context-only · Low temperature</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # ── Developer Mode ────────────────────────────────────────────────────
    dev = st.toggle("Developer Mode", value=st.session_state.dev_mode)
    st.session_state.dev_mode = dev

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # ── Clear Knowledge Base ──────────────────────────────────────────────
    st.markdown('<div class="sidebar-section-label">DANGER ZONE</div>', unsafe_allow_html=True)

    if st.button(
        "Clear Knowledge Base",
        key="clear_kb_btn",
        use_container_width=True,
        type="secondary",
    ):
        st.session_state.show_clear_modal = True
        st.rerun()

    st.markdown('<div class="clear-btn-style"></div>', unsafe_allow_html=True)


# ─── Main Chat Area ────────────────────────────────────────────────────────────
main_col, dev_col = st.columns([3, 1]) if st.session_state.dev_mode else (st.container(), None)

with main_col:
    # Empty state
    if not st.session_state.documents and not st.session_state.messages:
        render_empty_state()

    # Chat messages
    elif st.session_state.messages:
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                render_message_bubble(msg)

                # Source citations for AI messages
                if msg["role"] == "assistant" and msg.get("sources"):
                    render_source_citations(msg["sources"], msg.get("query", ""))

                # Dev panel for last AI message
                if (
                    st.session_state.dev_mode
                    and msg["role"] == "assistant"
                    and msg.get("retrieval_info")
                    and msg == next(
                        (m for m in reversed(st.session_state.messages) if m["role"] == "assistant"), None
                    )
                ):
                    render_dev_panel_content(msg["retrieval_info"])

    else:
        # Has documents but no messages yet
        st.markdown("""
        <div class="ready-state">
          <div class="ready-icon">◈</div>
          <div class="ready-title">Knowledge Base Ready</div>
          <div class="ready-sub">Ask anything about your documents below</div>
        </div>
        """, unsafe_allow_html=True)


# ─── Chat Input ────────────────────────────────────────────────────────────────
if not missing_creds or True:  # always show input area, error on submit if no creds
    # Mode pill shown next to input
    mode_short = st.session_state.query_mode.split(" ")[0]

    st.markdown(
        f'<div class="input-mode-pill">{mode_short} {st.session_state.query_mode.split(" ", 1)[1] if " " in st.session_state.query_mode else ""}</div>',
        unsafe_allow_html=True,
    )

    prompt = st.chat_input(
        "Ask a question about your documents...",
        disabled=not st.session_state.documents or bool(missing_creds),
    )

    if prompt:
        if missing_creds:
            st.error(f"Missing API credentials: {', '.join(missing_creds)}")
        elif not st.session_state.documents:
            st.warning("Please upload at least one PDF first.")
        else:
            # Add user message
            ts = datetime.now().strftime("%H:%M")
            user_msg = {
                "role": "user",
                "content": prompt,
                "timestamp": ts,
            }
            st.session_state.messages.append(user_msg)

            # Build RAG chain and query
            with st.spinner(""):
                # Show skeleton loader
                skeleton_placeholder = st.empty()
                with skeleton_placeholder:
                    render_skeleton_loader()

                try:
                    chain, retriever = build_rag_chain(
                        k=st.session_state.k_chunks,
                        strict=st.session_state.strict_mode,
                        mode=st.session_state.query_mode,
                    )

                    response_text, sources, retrieval_info = query_with_streaming(
                        chain=chain,
                        retriever=retriever,
                        question=prompt,
                        chat_history=st.session_state.chat_history,
                        stream_placeholder=skeleton_placeholder,
                    )

                    skeleton_placeholder.empty()

                    # Add AI message
                    ai_msg = {
                        "role": "assistant",
                        "content": response_text,
                        "timestamp": datetime.now().strftime("%H:%M"),
                        "sources": sources,
                        "query": prompt,
                        "retrieval_info": retrieval_info,
                    }
                    st.session_state.messages.append(ai_msg)

                    # Update conversation memory (windowed)
                    st.session_state.chat_history.append(("human", prompt))
                    st.session_state.chat_history.append(("ai", response_text))
                    # Keep last 10 exchanges (20 messages)
                    if len(st.session_state.chat_history) > 20:
                        st.session_state.chat_history = st.session_state.chat_history[-20:]

                    st.rerun()

                except Exception as e:
                    skeleton_placeholder.empty()
                    st.error(f"Something went wrong: {str(e)[:200]}")
