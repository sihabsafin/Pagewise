"""
PDF Intelligence — UI Components
All Streamlit rendering components for the design system.
"""

import streamlit as st
import re
from datetime import datetime


# ─── Top Navigation Bar ───────────────────────────────────────────────────────
def render_top_bar():
    has_docs = bool(st.session_state.get("documents"))
    status_color = "var(--accent-teal)" if has_docs else "var(--text-muted)"
    status_label = "Online" if has_docs else "Ready"

    doc_count = len(st.session_state.get("documents", []))
    doc_label = f"{doc_count} doc{'s' if doc_count != 1 else ''} indexed" if doc_count else "No documents"

    st.markdown(f"""
    <div class="top-bar">
      <div class="top-bar-left">
        <div class="top-bar-logo"></div>
        <span class="top-bar-name">PDF Intelligence</span>
      </div>
      <div class="top-bar-right">
        <div class="model-badge">
          <span class="model-badge-dot"></span>
          Gemma 2 · Groq
        </div>
        <div class="model-badge" style="gap:6px">
          <span style="width:6px;height:6px;border-radius:50%;background:{status_color};display:inline-block;"></span>
          {doc_label}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Empty State ──────────────────────────────────────────────────────────────
def render_empty_state():
    st.markdown("""
    <div class="empty-state">
      <div class="empty-orb empty-orb-1"></div>
      <div class="empty-orb empty-orb-2"></div>
      <div class="empty-diamond"></div>
      <div class="empty-title">PDF Intelligence</div>
      <div class="empty-sub">Drop your documents to begin. Ask questions. Get cited answers.</div>
      <div class="empty-pills">
        <span class="empty-pill">Ask questions</span>
        <span class="empty-pill">Cited answers</span>
        <span class="empty-pill">Retrieval control</span>
        <span class="empty-pill">Developer mode</span>
      </div>
      <div style="font-size:13px;color:var(--text-muted);margin-top:8px;">
        ← Upload PDFs in the sidebar to get started
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Document Card ─────────────────────────────────────────────────────────────
def render_document_card(doc: dict):
    name = doc.get("name", "Unknown")
    pages = doc.get("pages", 0)
    size = doc.get("size", 0)
    status = doc.get("status", "indexing")

    size_str = _format_size(size)
    pages_str = f"{pages} page{'s' if pages != 1 else ''}" if pages else ""

    meta_parts = [x for x in [pages_str, size_str] if x]
    meta = " · ".join(meta_parts)

    status_class = "status-ready" if status == "ready" else "status-indexing"
    status_text = "✓ Ready" if status == "ready" else "Indexing..."

    # Truncate long filenames
    display_name = name if len(name) <= 24 else name[:21] + "..."

    st.markdown(f"""
    <div class="doc-card">
      <div style="display:flex;align-items:center;gap:8px;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
          <polyline points="10 9 9 9 8 9"/>
        </svg>
        <span class="doc-card-name" title="{name}">{display_name}</span>
      </div>
      <div class="doc-card-meta">{meta}</div>
      <span class="status-pill {status_class}">{status_text}</span>
    </div>
    """, unsafe_allow_html=True)


# ─── Message Bubble ────────────────────────────────────────────────────────────
def render_message_bubble(msg: dict):
    role = msg["role"]
    content = msg["content"]
    timestamp = msg.get("timestamp", "")

    if role == "user":
        st.markdown(f"""
        <div class="message-wrapper user-message-wrapper">
          <div class="user-bubble">{_escape_html(content)}</div>
          <div class="msg-timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)

    else:  # assistant
        html_content = _markdown_to_html(content)
        st.markdown(f"""
        <div class="message-wrapper ai-message-wrapper">
          <div class="ai-bubble">
            <div class="ai-bubble-header">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="var(--accent-violet)" style="flex-shrink:0">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
              PDF Intelligence
            </div>
            <div class="ai-bubble-body">{html_content}</div>
          </div>
          <div class="msg-timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)


# ─── Skeleton Loader ──────────────────────────────────────────────────────────
def render_skeleton_loader():
    st.markdown("""
    <div class="message-wrapper ai-message-wrapper">
      <div class="skeleton-wrapper">
        <div class="skeleton-header"></div>
        <div class="skeleton-body">
          <div class="skeleton-line" style="width:82%"></div>
          <div class="skeleton-line" style="width:65%"></div>
          <div class="skeleton-line" style="width:48%"></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Source Citations ──────────────────────────────────────────────────────────
def render_source_citations(sources: list, query: str = ""):
    if not sources:
        return

    n = len(sources)
    query_words = set(query.lower().split()) if query else set()

    with st.expander(f"▸ Source Citations ({n} passage{'s' if n != 1 else ''})", expanded=False):
        for source in sources:
            _render_citation_card(source, query_words)


def _render_citation_card(source: dict, query_words: set):
    filename = source.get("filename", "Unknown")
    page = source.get("page", 1)
    score = source.get("score", 0.5)
    snippet = source.get("snippet", "")

    score_pct = int(score * 100)

    # Color coding
    if score >= 0.90:
        accent_class = "citation-accent-emerald"
        score_class = "score-emerald"
    elif score >= 0.70:
        accent_class = "citation-accent-teal"
        score_class = "score-teal"
    elif score >= 0.50:
        accent_class = "citation-accent-amber"
        score_class = "score-amber"
    else:
        accent_class = "citation-accent-muted"
        score_class = "score-muted"

    # Short filename
    display_fname = filename if len(filename) <= 30 else filename[:27] + "..."

    # Highlight keywords in snippet
    highlighted_snippet = _highlight_keywords(snippet, query_words)

    st.markdown(f"""
    <div class="citation-card {accent_class}">
      <div class="citation-header">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2" style="flex-shrink:0">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
        <span class="citation-filename" title="{filename}">{display_fname}</span>
        <span class="citation-page-pill">p.{page}</span>
        <span class="citation-score {score_class}">{score_pct}%</span>
      </div>
      <div class="citation-snippet">{highlighted_snippet}</div>
    </div>
    """, unsafe_allow_html=True)


def _highlight_keywords(text: str, keywords: set) -> str:
    """Highlight keyword matches in snippet text."""
    if not keywords:
        return _escape_html(text)

    # Escape HTML first
    escaped = _escape_html(text)

    # Highlight each keyword (case-insensitive, whole-ish words)
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
                  "to", "of", "and", "or", "for", "with", "this", "that", "it",
                  "be", "by", "from", "as", "but", "not", "have", "has", "had"}

    significant_words = keywords - stop_words

    for word in significant_words:
        if len(word) < 3:
            continue
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        escaped = pattern.sub(
            lambda m: f'<span class="highlight-kw">{m.group()}</span>',
            escaped
        )

    return escaped


# ─── Developer Panel ───────────────────────────────────────────────────────────
def render_dev_panel_content(info: dict):
    if not info:
        return

    st.markdown("""
    <div class="dev-panel">
      <div class="dev-section-label">Retrieval Configuration</div>
    """, unsafe_allow_html=True)

    config_rows = [
        ("model", info.get("model", "—")),
        ("embedding", info.get("embedding_model", "—")),
        ("dimensions", str(info.get("dimensions", "—"))),
        ("similarity", info.get("similarity_metric", "—")),
        ("k_retrieved", str(info.get("k", "—"))),
        ("temperature", str(info.get("temperature", "—"))),
        ("strict_mode", str(info.get("strict_mode", False))),
        ("query_mode", info.get("query_mode", "—")),
    ]

    rows_html = "".join(
        f'<div class="dev-kv-row"><span class="dev-key">{k}</span><span class="dev-val">{v}</span></div>'
        for k, v in config_rows
    )

    st.markdown(rows_html, unsafe_allow_html=True)
    st.markdown('<div class="dev-section-label" style="margin-top:16px">Retrieved Chunks</div>', unsafe_allow_html=True)

    chunks = info.get("chunks", [])
    for i, chunk in enumerate(chunks):
        chunk_text = chunk.get("text", "")[:600]
        source = chunk.get("source", "Unknown")
        page = chunk.get("page", 1)
        length = chunk.get("length", 0)

        st.markdown(f"""
        <div class="dev-chunk-box">
          <div class="dev-chunk-label">Chunk {i+1} · {source} · p.{page} · {length} chars</div>
          <div class="dev-chunk-text">{_escape_html(chunk_text)}{"..." if len(chunk.get("text","")) > 600 else ""}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─── Utility: Markdown → HTML ──────────────────────────────────────────────────
def _markdown_to_html(text: str) -> str:
    """Convert markdown to HTML for AI response rendering."""
    import re

    # Escape HTML
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Headers
    text = re.sub(r'^### (.+)$', r'<h3 style="font-family:var(--font-prose);font-size:18px;margin:16px 0 8px 0;color:var(--text-primary);">\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2 style="font-family:var(--font-prose);font-size:20px;margin:18px 0 10px 0;color:var(--text-primary);">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1 style="font-family:var(--font-prose);font-size:24px;margin:20px 0 12px 0;color:var(--text-primary);">\1</h1>', text, flags=re.MULTILINE)

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

    # Bullet lists
    lines = text.split('\n')
    result = []
    in_list = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- ') or stripped.startswith('* ') or stripped.startswith('• '):
            if not in_list:
                result.append('<ul style="margin:8px 0;padding-left:22px;">')
                in_list = True
            item = stripped[2:]
            result.append(f'<li style="margin:4px 0;">{item}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            if not in_list:
                result.append('<ol style="margin:8px 0;padding-left:22px;">')
                in_list = 'ol'
            item = re.sub(r'^\d+\.\s', '', stripped)
            result.append(f'<li style="margin:4px 0;">{item}</li>')
        else:
            if in_list:
                tag = 'ol' if in_list == 'ol' else 'ul'
                result.append(f'</{tag}>')
                in_list = False
            result.append(line)

    if in_list:
        tag = 'ol' if in_list == 'ol' else 'ul'
        result.append(f'</{tag}>')

    text = '\n'.join(result)

    # Paragraphs
    paragraphs = text.split('\n\n')
    processed = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if para.startswith('<'):
            processed.append(para)
        else:
            para = para.replace('\n', '<br>')
            processed.append(f'<p style="margin:0 0 12px 0;">{para}</p>')

    return '\n'.join(processed)


def _escape_html(text: str) -> str:
    """Safely escape HTML."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _format_size(size_bytes: int) -> str:
    """Format file size."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes // 1024}KB"
    else:
        return f"{size_bytes // (1024 * 1024):.1f}MB"
