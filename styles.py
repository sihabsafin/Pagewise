"""
PDF Intelligence — Global CSS Design System
Deep Intelligence aesthetic: Dark, precise, layered, trustworthy.
"""

GLOBAL_CSS = """
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,400&family=Lora:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>

/* ════════════════════════════════════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════════════════════════════════ */
:root {
  --color-base:          #060d1f;
  --color-surface-1:     #0c1a35;
  --color-surface-2:     #0f2248;
  --color-surface-3:     #162b55;
  --color-surface-glass: rgba(15,34,72,0.6);
  --color-border:        rgba(99,131,191,0.12);
  --color-border-hover:  rgba(99,131,191,0.28);

  --accent-primary:      #4f83ff;
  --accent-primary-glow: rgba(79,131,255,0.15);
  --accent-violet:       #8b5cf6;
  --accent-violet-glow:  rgba(139,92,246,0.12);
  --accent-teal:         #2dd4bf;
  --accent-amber:        #f59e0b;
  --accent-rose:         #f43f5e;
  --accent-emerald:      #10b981;
  --accent-yellow:       #fbbf24;

  --text-primary:   #e8edf7;
  --text-secondary: #8fa3c9;
  --text-muted:     #4d6491;
  --text-code:      #a5f3fc;

  --font-display: 'DM Sans', sans-serif;
  --font-ui:      'DM Sans', sans-serif;
  --font-prose:   'Lora', Georgia, serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;

  --shadow-card: 0 1px 3px rgba(0,0,0,0.4), 0 0 0 1px var(--color-border);
  --glow-blue: 0 0 0 3px rgba(79,131,255,0.12);
  --glow-violet: 0 0 0 3px rgba(139,92,246,0.12);
}

/* ════════════════════════════════════════════════════════════════════
   GLOBAL RESET & BASE
═══════════════════════════════════════════════════════════════════ */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stStatusWidget"],
.viewerBadge_container__1QSob,
.viewerBadge_link__1S137 { visibility: hidden !important; display: none !important; }

html, body { background: var(--color-base) !important; }

html, body, [class*="css"],
.stApp, .stMarkdown, .stText,
button, input, select, textarea {
  font-family: var(--font-ui) !important;
  color: var(--text-primary);
}

.stApp {
  background: var(--color-base) !important;
  min-height: 100vh;
}

.main .block-container {
  padding: 64px 32px 120px 32px !important;
  max-width: 100% !important;
}

/* ════════════════════════════════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(99,131,191,0.2);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(99,131,191,0.4); }

/* ════════════════════════════════════════════════════════════════════
   TOP BAR
═══════════════════════════════════════════════════════════════════ */
.top-bar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 52px;
  background: rgba(6,13,31,0.92);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 1000;
}

.top-bar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.top-bar-logo {
  width: 28px; height: 28px;
  background: linear-gradient(135deg, var(--accent-violet), var(--accent-primary));
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
  flex-shrink: 0;
}

.top-bar-name {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 500;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.model-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  padding: 4px 10px;
  font-size: 12px;
  color: var(--text-secondary);
}

.model-badge-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--accent-teal);
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.status-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--accent-teal);
}

/* ════════════════════════════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: var(--color-surface-1) !important;
  border-right: 1px solid var(--color-border) !important;
  padding-top: 60px !important;
}

[data-testid="stSidebar"] > div {
  padding: 16px !important;
}

.sidebar-section-label {
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.12em;
  color: var(--text-muted);
  text-transform: uppercase;
  margin: 0 0 10px 2px;
  font-family: var(--font-ui);
}

.sidebar-divider {
  height: 1px;
  background: var(--color-border);
  margin: 16px 0;
}

/* File uploader */
[data-testid="stFileUploader"] {
  background: transparent !important;
}

[data-testid="stFileUploaderDropzone"] {
  background: var(--color-surface-2) !important;
  border: 1.5px dashed rgba(79,131,255,0.35) !important;
  border-radius: var(--radius-md) !important;
  padding: 20px !important;
  transition: all 0.2s ease;
  cursor: pointer;
}

[data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--accent-primary) !important;
  background: rgba(79,131,255,0.05) !important;
  transform: scale(1.01);
}

[data-testid="stFileUploaderDropzone"] * {
  color: var(--text-secondary) !important;
  font-family: var(--font-ui) !important;
  font-size: 13px !important;
}

.upload-hint {
  font-size: 11px;
  color: var(--text-muted);
  text-align: center;
  margin: 4px 0 12px 0;
}

/* Document card */
.doc-card {
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  margin-bottom: 6px;
  transition: all 0.15s ease;
  position: relative;
}

.doc-card:hover {
  border-color: var(--color-border-hover);
  background: var(--color-surface-3);
}

.doc-card-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.doc-card-meta {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 3px;
}

.status-pill {
  display: inline-block;
  font-size: 10px;
  font-weight: 500;
  padding: 2px 7px;
  border-radius: 20px;
  margin-top: 5px;
}

.status-indexing {
  background: rgba(245,158,11,0.15);
  color: var(--accent-amber);
  border: 1px solid rgba(245,158,11,0.3);
}

.status-ready {
  background: rgba(45,212,191,0.1);
  color: var(--accent-teal);
  border: 1px solid rgba(45,212,191,0.25);
}

/* Mode tooltip */
.mode-tooltip {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 6px;
  padding: 6px 8px;
  background: var(--color-surface-2);
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  font-style: italic;
}

/* Slider labels */
.slider-sublabel, .toggle-sublabel {
  font-size: 11px;
  color: var(--text-muted);
  letter-spacing: 0.02em;
  margin-top: 4px;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
  background: var(--color-surface-2) !important;
  border: 1px solid var(--color-border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-ui) !important;
}

[data-testid="stSelectbox"] > div > div:hover {
  border-color: var(--color-border-hover) !important;
}

/* Slider */
[data-testid="stSlider"] > div > div > div {
  background: var(--accent-primary) !important;
}

[data-testid="stSlider"] .stSlider [data-testid="stThumbValue"] {
  background: var(--accent-primary) !important;
  color: white !important;
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
}

/* Toggle */
[data-testid="stToggle"] > label {
  color: var(--text-secondary) !important;
  font-size: 13px !important;
}

/* Clear button */
[data-testid="stButton"][key="clear_kb_btn"] > button,
.stButton button[kind="secondary"] {
  background: transparent !important;
  border: 1px solid rgba(244,63,94,0.2) !important;
  color: rgba(244,63,94,0.7) !important;
  border-radius: var(--radius-sm) !important;
  font-size: 12px !important;
  transition: all 0.2s ease;
}

.stButton button[kind="secondary"]:hover {
  border-color: rgba(244,63,94,0.6) !important;
  background: rgba(244,63,94,0.08) !important;
  color: var(--accent-rose) !important;
}

/* Credentials warning */
.cred-warning {
  background: rgba(244,63,94,0.08);
  border: 1px solid rgba(244,63,94,0.3);
  border-radius: var(--radius-sm);
  padding: 12px;
  margin-bottom: 16px;
}

.cred-warning-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--accent-rose);
  margin-bottom: 6px;
}

.cred-warning-body {
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.cred-warning-body code {
  background: var(--color-surface-3);
  padding: 1px 4px;
  border-radius: 3px;
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--accent-teal);
}

/* ════════════════════════════════════════════════════════════════════
   EMPTY / READY STATES
═══════════════════════════════════════════════════════════════════ */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  padding: 40px 20px;
  position: relative;
  overflow: hidden;
}

.empty-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.06;
  animation: drift 12s ease-in-out infinite alternate;
}

.empty-orb-1 {
  width: 400px; height: 400px;
  background: var(--accent-violet);
  top: -100px; left: -100px;
  animation-delay: 0s;
}

.empty-orb-2 {
  width: 300px; height: 300px;
  background: var(--accent-primary);
  bottom: -50px; right: -50px;
  animation-delay: -6s;
}

@keyframes drift {
  from { transform: translate(0, 0) scale(1); }
  to { transform: translate(40px, 20px) scale(1.1); }
}

.empty-diamond {
  width: 52px; height: 52px;
  background: linear-gradient(135deg, var(--accent-violet), var(--accent-primary));
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
  margin-bottom: 24px;
  animation: float 4s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.empty-title {
  font-family: var(--font-display);
  font-size: 34px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 10px;
  letter-spacing: -0.02em;
}

.empty-sub {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 28px;
  max-width: 400px;
}

.empty-pills {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 32px;
}

.empty-pill {
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 13px;
  color: var(--text-muted);
}

.ready-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
  gap: 12px;
}

.ready-icon {
  font-size: 40px;
  background: linear-gradient(135deg, var(--accent-violet), var(--accent-teal));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.ready-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 500;
  color: var(--text-primary);
}

.ready-sub {
  font-size: 14px;
  color: var(--text-muted);
}

/* ════════════════════════════════════════════════════════════════════
   CHAT MESSAGES
═══════════════════════════════════════════════════════════════════ */

/* Override Streamlit chat container */
[data-testid="stChatMessage"] {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  max-width: 100% !important;
}

.message-wrapper {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* User message */
.user-message-wrapper {
  align-items: flex-end;
}

.user-bubble {
  background: linear-gradient(135deg, #1e3a6e, #162b55);
  border: 1px solid rgba(79,131,255,0.2);
  border-radius: 16px 4px 16px 16px;
  padding: 14px 18px;
  max-width: 72%;
  font-size: 15px;
  color: var(--text-primary);
  line-height: 1.6;
  font-family: var(--font-ui);
}

/* AI response */
.ai-message-wrapper {
  align-items: flex-start;
}

.ai-bubble {
  background: rgba(15,34,72,0.5);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--color-border);
  border-radius: 4px 16px 16px 16px;
  overflow: hidden;
  width: 100%;
  max-width: 860px;
}

.ai-bubble-header {
  background: rgba(139,92,246,0.08);
  border-left: 3px solid var(--accent-violet);
  padding: 10px 18px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 500;
  color: var(--accent-violet);
  letter-spacing: 0.05em;
}

.ai-bubble-body {
  padding: 18px 24px;
  font-family: var(--font-prose) !important;
  font-size: 17px !important;
  line-height: 1.8 !important;
  color: var(--text-primary) !important;
}

.ai-bubble-body * {
  font-family: var(--font-prose) !important;
}

.ai-bubble-body p { margin: 0 0 12px 0; }
.ai-bubble-body p:last-child { margin-bottom: 0; }

.ai-bubble-body ul, .ai-bubble-body ol {
  padding-left: 22px;
  margin: 8px 0;
}

.ai-bubble-body li { margin: 5px 0; }

.ai-bubble-body strong {
  color: var(--text-primary);
  font-weight: 600;
}

.ai-bubble-body code {
  font-family: var(--font-mono) !important;
  font-size: 14px !important;
  background: var(--color-surface-3);
  padding: 1px 5px;
  border-radius: 3px;
  color: var(--accent-teal);
}

.msg-timestamp {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 5px;
  font-family: var(--font-ui);
}

/* Typing cursor */
.typing-cursor {
  display: inline-block;
  width: 2px;
  height: 1.1em;
  background: var(--accent-violet);
  margin-left: 2px;
  vertical-align: text-bottom;
  animation: blink 0.8s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* Skeleton loader */
.skeleton-wrapper {
  background: rgba(15,34,72,0.5);
  border: 1px solid var(--color-border);
  border-radius: 4px 16px 16px 16px;
  overflow: hidden;
  max-width: 860px;
}

.skeleton-header {
  background: rgba(139,92,246,0.08);
  border-left: 3px solid var(--accent-violet);
  padding: 10px 18px;
  height: 36px;
}

.skeleton-body {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton-line {
  height: 14px;
  background: linear-gradient(
    90deg,
    var(--color-surface-2) 0%,
    var(--color-surface-3) 40%,
    var(--color-surface-2) 80%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ════════════════════════════════════════════════════════════════════
   SOURCE CITATIONS
═══════════════════════════════════════════════════════════════════ */
.citations-toggle {
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 8px 0;
  display: flex;
  align-items: center;
  gap: 6px;
  user-select: none;
  font-family: var(--font-ui);
}

.citation-card {
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  overflow: hidden;
  margin-bottom: 8px;
  transition: border-color 0.15s ease;
}

.citation-card:hover {
  border-color: var(--color-border-hover);
}

.citation-accent-emerald { border-left: 3px solid var(--accent-emerald); }
.citation-accent-teal    { border-left: 3px solid var(--accent-teal); }
.citation-accent-amber   { border-left: 3px solid var(--accent-amber); }
.citation-accent-muted   { border-left: 3px solid var(--text-muted); }

.citation-header {
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.citation-filename {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  font-family: var(--font-ui);
  flex: 1;
}

.citation-page-pill {
  background: var(--color-surface-3);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 2px 9px;
  font-size: 11px;
  color: var(--accent-primary);
  font-family: var(--font-mono);
}

.citation-score {
  font-size: 11px;
  font-family: var(--font-mono);
  padding: 2px 7px;
  border-radius: 12px;
}

.score-emerald { color: var(--accent-emerald); background: rgba(16,185,129,0.1); }
.score-teal    { color: var(--accent-teal);    background: rgba(45,212,191,0.1); }
.score-amber   { color: var(--accent-amber);   background: rgba(245,158,11,0.1); }
.score-muted   { color: var(--text-muted);     background: var(--color-surface-3); }

.citation-snippet {
  padding: 0 14px 12px 14px;
  font-size: 13px;
  color: var(--text-secondary);
  font-family: var(--font-ui);
  line-height: 1.6;
}

.highlight-kw {
  background: rgba(251,191,36,0.18);
  color: #fbbf24;
  border-radius: 2px;
  padding: 0 2px;
}

/* ════════════════════════════════════════════════════════════════════
   DEVELOPER PANEL
═══════════════════════════════════════════════════════════════════ */
.dev-panel {
  background: var(--color-surface-1);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px;
  font-family: var(--font-mono);
  font-size: 12px;
}

.dev-section-label {
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.12em;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 10px;
  margin-top: 14px;
}

.dev-section-label:first-child { margin-top: 0; }

.dev-kv-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  border-bottom: 1px solid rgba(99,131,191,0.06);
}

.dev-key {
  color: var(--text-muted);
  font-size: 11px;
}

.dev-val {
  color: var(--accent-teal);
  font-size: 11px;
}

.dev-chunk-box {
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  margin-bottom: 8px;
  max-height: 110px;
  overflow-y: auto;
}

.dev-chunk-label {
  font-size: 10px;
  color: var(--text-muted);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 5px;
}

.dev-chunk-text {
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.5;
  word-break: break-word;
}

/* ════════════════════════════════════════════════════════════════════
   CHAT INPUT
═══════════════════════════════════════════════════════════════════ */
[data-testid="stChatInput"] {
  position: fixed !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  background: rgba(6,13,31,0.95) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border-top: 1px solid var(--color-border) !important;
  padding: 16px 24px !important;
  z-index: 900 !important;
}

[data-testid="stChatInput"] textarea {
  background: var(--color-surface-2) !important;
  border: 1px solid var(--color-border) !important;
  border-radius: 12px !important;
  color: var(--text-primary) !important;
  font-family: var(--font-ui) !important;
  font-size: 15px !important;
  padding: 14px 18px !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stChatInput"] textarea:focus {
  border-color: var(--accent-primary) !important;
  box-shadow: var(--glow-blue) !important;
  outline: none !important;
}

[data-testid="stChatInput"] textarea::placeholder {
  color: var(--text-muted) !important;
}

[data-testid="stChatInput"] button {
  background: var(--accent-primary) !important;
  border-radius: 50% !important;
  width: 40px !important;
  height: 40px !important;
  padding: 0 !important;
  border: none !important;
  transition: all 0.15s ease;
}

[data-testid="stChatInput"] button:hover {
  transform: scale(1.05);
  filter: brightness(1.1);
}

.input-mode-pill {
  position: fixed;
  bottom: 80px;
  left: 310px;
  background: var(--color-surface-3);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 11px;
  color: var(--text-muted);
  z-index: 901;
  font-family: var(--font-ui);
}

/* ════════════════════════════════════════════════════════════════════
   MODAL
═══════════════════════════════════════════════════════════════════ */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(6,13,31,0.8);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-box {
  background: var(--color-surface-1);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 32px;
  max-width: 420px;
  width: 100%;
  text-align: center;
  animation: modalIn 0.2s ease;
}

@keyframes modalIn {
  from { opacity: 0; transform: scale(0.96); }
  to { opacity: 1; transform: scale(1); }
}

.modal-icon {
  font-size: 32px;
  margin-bottom: 16px;
  color: var(--accent-amber);
}

.modal-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.modal-body {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 24px;
}

/* Primary button override */
.stButton button[kind="primary"] {
  background: var(--accent-rose) !important;
  border: none !important;
  color: white !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-ui) !important;
}

/* ════════════════════════════════════════════════════════════════════
   EXPANDER (citation container)
═══════════════════════════════════════════════════════════════════ */
.streamlit-expanderHeader {
  background: transparent !important;
  border: none !important;
  font-size: 13px !important;
  color: var(--text-secondary) !important;
  font-family: var(--font-ui) !important;
  padding: 6px 0 !important;
}

.streamlit-expanderContent {
  border: none !important;
  padding: 8px 0 0 0 !important;
}

/* Spinner override */
.stSpinner > div {
  border-top-color: var(--accent-violet) !important;
}

/* General button */
.stButton > button {
  font-family: var(--font-ui) !important;
  border-radius: var(--radius-sm) !important;
  transition: all 0.15s ease !important;
}

/* Alert overrides */
.stAlert {
  background: var(--color-surface-2) !important;
  border: 1px solid var(--color-border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-secondary) !important;
}

</style>
"""
