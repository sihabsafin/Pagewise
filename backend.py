"""
PDF Intelligence — Backend
Handles: PDF ingestion, embedding, AstraDB vector store, RAG chain, streaming
"""

import os
import io
import time
import streamlit as st

# Lazy imports for better startup time
def _import_pdf_tools():
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    return PyPDFLoader, RecursiveCharacterTextSplitter

def _import_embeddings():
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings

def _import_astra():
    from langchain_astradb import AstraDBVectorStore
    return AstraDBVectorStore

def _import_groq():
    from langchain_groq import ChatGroq
    return ChatGroq

def _import_chain_tools():
    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationBufferWindowMemory
    from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
    from langchain_core.messages import HumanMessage, AIMessage
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain.prompts import PromptTemplate
    return (ConversationalRetrievalChain, ConversationBufferWindowMemory,
            ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate,
            HumanMessage, AIMessage, StrOutputParser, RunnablePassthrough, PromptTemplate)


# ─── Credentials ────────────────────────────────────────────────────────────
def _get_secret(key):
    try:
        return st.secrets.get(key) or os.environ.get(key, "")
    except Exception:
        return os.environ.get(key, "")


# ─── Embeddings (cached) ─────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def _get_embeddings():
    HuggingFaceEmbeddings = _import_embeddings()
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


# ─── Vector Store ─────────────────────────────────────────────────────────────
def initialize_vector_store():
    """Initialize or return cached AstraDB vector store."""
    if st.session_state.get("vector_store") is not None:
        return st.session_state.vector_store

    AstraDBVectorStore = _import_astra()
    embeddings = _get_embeddings()

    token = _get_secret("ASTRA_DB_APPLICATION_TOKEN")
    endpoint = _get_secret("ASTRA_DB_API_ENDPOINT")

    if not token or not endpoint:
        raise ValueError("Missing AstraDB credentials. Please set ASTRA_DB_APPLICATION_TOKEN and ASTRA_DB_API_ENDPOINT.")

    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="pdf_intelligence_docs",
        token=token,
        api_endpoint=endpoint,
    )

    st.session_state.vector_store = vstore
    return vstore


# ─── PDF Ingestion ────────────────────────────────────────────────────────────
def ingest_pdfs(new_docs: list, progress_placeholder) -> dict:
    """
    Ingest a list of new PDF documents into AstraDB.

    Args:
        new_docs: list of doc dicts with 'file', 'name', 'id'
        progress_placeholder: Streamlit placeholder for status updates

    Returns:
        dict mapping doc_id -> {pages: int}
    """
    PyPDFLoader, RecursiveCharacterTextSplitter = _import_pdf_tools()

    results = {}

    try:
        vstore = initialize_vector_store()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )

        for doc_info in new_docs:
            file_obj = doc_info.get("file")
            if file_obj is None:
                continue

            doc_id = doc_info["id"]
            fname = doc_info["name"]

            # Status: Splitting
            with progress_placeholder:
                st.markdown(
                    f'<div class="status-pill status-indexing">Splitting pages... {fname}</div>',
                    unsafe_allow_html=True,
                )

            # Save to temp file for PyPDFLoader
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file_obj.read())
                tmp_path = tmp.name

            loader = PyPDFLoader(tmp_path)
            pages = loader.load()
            num_pages = len(pages)

            # Inject metadata
            for page in pages:
                page.metadata["source_file"] = fname
                page.metadata["doc_id"] = doc_id

            # Status: Embedding
            with progress_placeholder:
                st.markdown(
                    f'<div class="status-pill status-indexing">Generating embeddings... {fname}</div>',
                    unsafe_allow_html=True,
                )

            chunks = splitter.split_documents(pages)

            # Status: Storing
            with progress_placeholder:
                st.markdown(
                    f'<div class="status-pill status-indexing">Storing {len(chunks)} vectors... {fname}</div>',
                    unsafe_allow_html=True,
                )

            vstore.add_documents(chunks)

            results[doc_id] = {"pages": num_pages}

            # Cleanup temp file
            os.unlink(tmp_path)

    except Exception as e:
        with progress_placeholder:
            st.error(f"Ingestion failed: {str(e)[:200]}")

    return results


# ─── Mode Prompts ─────────────────────────────────────────────────────────────
MODE_PROMPTS = {
    "⚡ Factual Answer": {
        "system": """You are PDF Intelligence, a precise document analysis AI.
Answer the question DIRECTLY and CONCISELY based solely on the provided context.
Do not add unnecessary elaboration. If the context doesn't contain the answer, say so clearly.
Be factual and confident.""",
        "temperature": 0.1,
    },
    "📋 Detailed Explanation": {
        "system": """You are PDF Intelligence, a thorough document analysis AI.
Provide a comprehensive, detailed explanation based on the provided context.
Cover all relevant aspects, provide background where useful, and ensure completeness.
Structure your response clearly with logical flow.""",
        "temperature": 0.2,
    },
    "• Bullet Summary": {
        "system": """You are PDF Intelligence, a document analysis AI.
Format your response as a well-organized bullet list.
Extract and present key points clearly and concisely.
Use nested bullets for sub-points when appropriate.
Start with a one-sentence summary, then bullets.""",
        "temperature": 0.15,
    },
    "⚖ Compare Sections": {
        "system": """You are PDF Intelligence, a document analysis AI specializing in comparison.
Identify similarities and differences across the provided context sections.
Use a structured format: first list similarities, then differences, then synthesis.
Be precise about which source each point comes from.""",
        "temperature": 0.15,
    },
    "📊 Executive Summary": {
        "system": """You are PDF Intelligence, a document analysis AI.
Create a concise executive summary suitable for a business briefing.
Format: Key Finding (1-2 sentences), then 3-5 key takeaways, then a brief conclusion.
Focus on actionable insights and high-level conclusions.""",
        "temperature": 0.2,
    },
}


# ─── Build RAG Chain ──────────────────────────────────────────────────────────
def build_rag_chain(k: int = 3, strict: bool = False, mode: str = "⚡ Factual Answer"):
    """
    Build the RAG retrieval chain.

    Returns:
        tuple: (chain_config dict, retriever)
    """
    vstore = initialize_vector_store()

    retriever = vstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )

    mode_cfg = MODE_PROMPTS.get(mode, MODE_PROMPTS["⚡ Factual Answer"])
    temperature = 0.05 if strict else mode_cfg["temperature"]

    chain_config = {
        "retriever": retriever,
        "temperature": temperature,
        "mode": mode,
        "system_prompt": mode_cfg["system"],
        "strict": strict,
    }

    return chain_config, retriever


# ─── Query with Streaming ─────────────────────────────────────────────────────
def query_with_streaming(chain, retriever, question: str, chat_history: list, stream_placeholder):
    """
    Execute a RAG query with streaming response.

    Returns:
        tuple: (response_text, sources, retrieval_info)
    """
    ChatGroq = _import_groq()

    groq_key = _get_secret("GROQ_API_KEY")
    if not groq_key:
        raise ValueError("Missing GROQ_API_KEY. Please add it to Streamlit Secrets.")

    temperature = chain.get("temperature", 0.1)
    system_prompt = chain.get("system_prompt", "Answer based on context only.")
    strict = chain.get("strict", False)

    # Retrieve relevant documents
    total_chunks = _estimate_total_chunks()
    with stream_placeholder:
        st.markdown(
            f'<div class="skeleton-wrapper"><div class="skeleton-header"></div>'
            f'<div class="skeleton-body">'
            f'<div class="skeleton-line" style="width:80%"></div>'
            f'<div class="skeleton-line" style="width:60%"></div>'
            f'<div class="skeleton-line" style="width:40%"></div>'
            f'</div></div>'
            f'<div style="font-size:12px;color:var(--text-muted);margin-top:8px;font-family:var(--font-mono);">'
            f'Searching {total_chunks} chunks...</div>',
            unsafe_allow_html=True,
        )

    docs = retriever.get_relevant_documents(question)

    # Build context
    context_parts = []
    for doc in docs:
        fname = doc.metadata.get("source_file", doc.metadata.get("source", "Unknown"))
        page = doc.metadata.get("page", 0)
        context_parts.append(f"[Source: {fname}, Page {page + 1}]\n{doc.page_content}")

    context = "\n\n---\n\n".join(context_parts)

    # Build conversation history string
    history_str = ""
    if chat_history:
        pairs = []
        for i in range(0, len(chat_history) - 1, 2):
            if i + 1 < len(chat_history):
                human_msg = chat_history[i][1] if isinstance(chat_history[i], tuple) else chat_history[i]
                ai_msg = chat_history[i+1][1] if isinstance(chat_history[i+1], tuple) else chat_history[i+1]
                pairs.append(f"Human: {human_msg}\nAssistant: {ai_msg}")
        if pairs:
            history_str = "\n\n".join(pairs[-4:])  # last 4 exchanges

    # Build full prompt
    strict_instruction = "\nIMPORTANT: Answer ONLY from the provided context. Do not use external knowledge." if strict else ""

    full_prompt = f"""{system_prompt}{strict_instruction}

CONVERSATION HISTORY:
{history_str if history_str else "No previous conversation."}

RETRIEVED CONTEXT:
{context if context else "No relevant context found in the documents."}

QUESTION: {question}

If the context doesn't contain relevant information, respond: "I couldn't find relevant information in your documents for this question."

Answer:"""

    # Initialize LLM
    llm = ChatGroq(
        groq_api_key=groq_key,
        model_name="gemma2-9b-it",
        temperature=temperature,
        streaming=True,
    )

    # Stream response
    response_text = ""

    with stream_placeholder:
        response_container = st.empty()

    try:
        for chunk in llm.stream(full_prompt):
            token = chunk.content if hasattr(chunk, 'content') else str(chunk)
            response_text += token

            # Render streaming with cursor
            with response_container:
                st.markdown(
                    f'<div class="ai-bubble">'
                    f'<div class="ai-bubble-header">◈ &nbsp; PDF Intelligence</div>'
                    f'<div class="ai-bubble-body">{_simple_md_to_html(response_text)}'
                    f'<span class="typing-cursor"></span></div></div>',
                    unsafe_allow_html=True,
                )

    except Exception as e:
        response_text = f"I encountered an error processing your request. Please try again. (Error: {str(e)[:100]})"

    # Extract sources
    sources = _extract_sources(docs, question)

    # Build retrieval info for developer panel
    retrieval_info = _build_retrieval_info(
        docs=docs,
        k=len(docs),
        temperature=temperature,
        strict=strict,
        mode=chain.get("mode", "⚡ Factual Answer"),
    )

    return response_text, sources, retrieval_info


# ─── Helper: Source extraction ─────────────────────────────────────────────────
def _extract_sources(docs, query: str) -> list:
    """Extract and score source documents."""
    sources = []
    query_words = set(query.lower().split())

    for i, doc in enumerate(docs):
        fname = doc.metadata.get("source_file", doc.metadata.get("source", "Unknown"))
        page = doc.metadata.get("page", 0)

        # Approximate similarity score based on keyword overlap
        doc_words = set(doc.page_content.lower().split())
        overlap = len(query_words & doc_words)
        max_possible = max(len(query_words), 1)
        base_score = min(0.95, 0.5 + (overlap / max_possible) * 0.45)

        # Decay by rank
        score = base_score * (1 - i * 0.08)
        score = round(max(0.35, score), 3)

        snippet = doc.page_content.strip()[:400]
        if len(doc.page_content) > 400:
            snippet += "..."

        sources.append({
            "filename": fname,
            "page": page + 1,
            "score": score,
            "snippet": snippet,
            "chunk_text": doc.page_content,
        })

    return sources


# ─── Helper: Retrieval info ────────────────────────────────────────────────────
def _build_retrieval_info(docs, k, temperature, strict, mode):
    return {
        "model": "gemma2-9b-it",
        "embedding_model": "all-MiniLM-L6-v2",
        "dimensions": 384,
        "similarity_metric": "cosine",
        "k": k,
        "temperature": temperature,
        "strict_mode": strict,
        "query_mode": mode,
        "chunks_retrieved": len(docs),
        "chunks": [
            {
                "source": doc.metadata.get("source_file", "Unknown"),
                "page": doc.metadata.get("page", 0) + 1,
                "text": doc.page_content,
                "length": len(doc.page_content),
            }
            for doc in docs
        ],
    }


# ─── Helper: Estimate total chunks ────────────────────────────────────────────
def _estimate_total_chunks() -> int:
    """Estimate total chunks from document list."""
    docs = st.session_state.get("documents", [])
    if not docs:
        return 0
    total_pages = sum(d.get("pages", 5) for d in docs)
    return total_pages * 3  # ~3 chunks per page avg


# ─── Helper: Simple Markdown → HTML ────────────────────────────────────────────
def _simple_md_to_html(text: str) -> str:
    """Convert basic markdown to HTML for streaming render."""
    import re
    # Escape HTML special chars except for already-converted
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Code inline
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Line breaks
    text = text.replace("\n\n", "</p><p>").replace("\n", "<br>")
    # Wrap in paragraph
    if not text.startswith("<"):
        text = f"<p>{text}</p>"

    return text


# ─── Clear Knowledge Base ─────────────────────────────────────────────────────
def clear_knowledge_base():
    """Delete all vectors from AstraDB and reset session."""
    try:
        vstore = st.session_state.get("vector_store")
        if vstore is not None:
            vstore.clear()
        st.session_state.vector_store = None
    except Exception as e:
        # Even if AstraDB clear fails, reset locally
        st.session_state.vector_store = None


# ─── Retrieval Config (for dev panel) ────────────────────────────────────────
def get_retrieval_config():
    return {
        "model": "gemma2-9b-it (Groq)",
        "embedding": "all-MiniLM-L6-v2",
        "dimensions": 384,
        "metric": "cosine",
        "vector_store": "AstraDB",
        "chunk_size": 1000,
        "chunk_overlap": 150,
    }
