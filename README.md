# ◈ PDF Intelligence

**AI-Powered Document Query Platform**  
Built with Streamlit · Groq (Gemma 2) · AstraDB · LangChain

---

## Overview

PDF Intelligence is a production-grade RAG (Retrieval-Augmented Generation) SaaS application that allows users to upload multiple PDFs, ask conversational questions, and receive AI-generated answers with exact document citations.

**Design Aesthetic:** Bloomberg Terminal meets Linear.app meets Perplexity AI — dark, precise, trustworthy.

---

## Features

### Core (Level 1)
- **Multi-PDF Upload** — drag-and-drop, multiple files, cross-document questions
- **Source Citations** — every answer includes document name, page number, text snippet, similarity score
- **Conversational RAG** — windowed memory for follow-up questions
- **Document Reset** — confirmation modal, full AstraDB + session clear

### Advanced (Level 2)
- **5 Query Modes** — Factual, Detailed, Bullet Summary, Compare, Executive Summary
- **Retrieval Controls** — adjustable k (1–10 chunks), Strict Mode toggle
- **Developer Panel** — chunk inspection, similarity scores, embedding metadata
- **Real-Time Streaming** — skeleton loaders → streaming tokens → typing cursor

### Design System
- Deep dark theme with glass-morphism surfaces
- Lora serif for AI responses (authoritative, distinct from generic chatbots)
- Color-coded citations (emerald ≥90%, teal 70-89%, amber 50-69%)
- Animated micro-interactions throughout

---

## Setup

### 1. Clone & Install

```bash
git clone <your-repo>
cd pdf_intelligence_app
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "gsk_..."
ASTRA_DB_APPLICATION_TOKEN = "AstraCS:..."
ASTRA_DB_API_ENDPOINT = "https://your-db-id-region.apps.astra.datastax.com"
```

**Get your keys:**
- **Groq:** [console.groq.com](https://console.groq.com) → API Keys (free tier available)
- **AstraDB:** [astra.datastax.com](https://astra.datastax.com) → Create DB → Generate Token
  - Database: Vector type, any cloud/region
  - Token role: `Database Administrator`

### 3. Run Locally

```bash
streamlit run app.py
```

---

## Deployment (Streamlit Cloud)

1. Push to GitHub (public or private repo)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. New app → select your repo → `app.py`
4. **Settings → Secrets** → paste your API credentials
5. Deploy!

---

## Architecture

```
User Upload → PyPDF Loader → RecursiveCharacterTextSplitter
           → HuggingFace Embeddings (all-MiniLM-L6-v2, 384d)
           → AstraDB Vector Store (cosine similarity)

User Query → Retriever (top-k similarity search)
          → Context Assembly → Groq LLM (Gemma 2)
          → Streaming Response → Source Citations
```

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit + Deep CSS |
| LLM | Groq API (Gemma 2 9B) |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| Vector Store | AstraDB (Cassandra) |
| RAG Framework | LangChain |
| Memory | Windowed conversation buffer |

---

## File Structure

```
pdf_intelligence_app/
├── app.py              # Main Streamlit application
├── backend.py          # RAG engine, AstraDB, Groq integration
├── ui_components.py    # All UI rendering functions
├── styles.py           # Complete CSS design system
├── requirements.txt    # Python dependencies
└── .streamlit/
    ├── config.toml     # Streamlit configuration
    └── secrets.toml    # API keys (never commit this)
```

---

## Configuration

| Setting | Default | Range |
|---------|---------|-------|
| Retrieved chunks (k) | 3 | 1–10 |
| Embedding dimensions | 384 | Fixed |
| Similarity metric | Cosine | Fixed |
| Temperature (normal) | 0.1–0.2 | Mode-dependent |
| Temperature (strict) | 0.05 | Fixed |
| Memory window | 10 exchanges | Configurable |
| Max upload size | 200MB | Streamlit config |

---

## Query Modes

| Mode | Behavior | Temperature |
|------|----------|-------------|
| ⚡ Factual Answer | Direct, concise | 0.10 |
| 📋 Detailed Explanation | Thorough, contextual | 0.20 |
| • Bullet Summary | Structured key points | 0.15 |
| ⚖ Compare Sections | Similarities & differences | 0.15 |
| 📊 Executive Summary | High-level briefing | 0.20 |

---

## Safety & Quality

- Answers grounded in documents only — no hallucination
- Clear fallback when context is insufficient
- User input sanitized before prompting
- PDF size validated before processing
- All AstraDB/API errors shown as friendly messages
- Destructive actions require confirmation

---

*Built to demonstrate production RAG engineering capability.*
