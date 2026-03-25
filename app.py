"""
StudyMind AI — Premium Streamlit Interface
Dark-themed study tool with sidebar navigation and multiple AI-powered features.
"""

import streamlit as st
import os
import json
import graphviz
from modules.extractor import extract_text
from modules.summarizer import summarize_pdf
from modules.quiz_gen import generate_quiz
from modules.flashcard_gen import generate_flashcards
from modules.mindmap_gen import generate_mindmap
from modules.podcast_gen import create_podcast
from modules.exporter import export_summary, export_quiz

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="StudyMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ── */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121f 0%, #1a1a2e 100%) !important;
        border-right: 1px solid rgba(108, 92, 231, 0.15) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #c0c0d0;
    }

    /* ── Main Content Area ── */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1100px;
    }

    /* ── Cards / Containers ── */
    .glass-card {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
        border: 1px solid rgba(108, 92, 231, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* ── Header Card ── */
    .header-card {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.95) 0%, rgba(22, 33, 62, 0.95) 100%);
        border: 1px solid rgba(108, 92, 231, 0.25);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* ── Badges ── */
    .ai-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-left: 8px;
        vertical-align: middle;
    }

    .count-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        font-size: 0.75rem;
        font-weight: 700;
        margin-left: auto;
    }

    /* ── Section Labels ── */
    .section-label {
        color: #8888aa;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 1.5rem 0 0.5rem 0;
        padding-left: 4px;
    }

    .topic-label {
        color: #8888aa;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 1rem 0 0.5rem 0;
    }

    /* ── Topic Items ── */
    .topic-item {
        display: flex;
        align-items: flex-start;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .topic-dot {
        width: 8px;
        height: 8px;
        min-width: 8px;
        background: #6c5ce7;
        border-radius: 50%;
        margin-top: 6px;
        margin-right: 12px;
    }
    .topic-text {
        color: #d0d0e0;
        font-size: 0.92rem;
        line-height: 1.5;
    }

    /* ── Definition Items ── */
    .def-card {
        background: rgba(108, 92, 231, 0.06);
        border-left: 3px solid #6c5ce7;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    }
    .def-term {
        color: #a29bfe;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }
    .def-meaning {
        color: #b0b0c8;
        font-size: 0.88rem;
        line-height: 1.5;
    }

    /* ── Formula Items ── */
    .formula-card {
        background: rgba(46, 213, 115, 0.05);
        border: 1px solid rgba(46, 213, 115, 0.15);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    }
    .formula-name {
        color: #2ed573;
        font-weight: 600;
        font-size: 0.88rem;
        margin-bottom: 4px;
    }
    .formula-expr {
        color: #e0e0e0;
        font-family: 'Courier New', monospace;
        font-size: 1rem;
        padding: 6px 0;
        letter-spacing: 0.5px;
    }
    .formula-desc {
        color: #8888aa;
        font-size: 0.82rem;
        margin-top: 4px;
    }

    /* ── Nav Buttons ── */
    .nav-btn {
        display: flex;
        align-items: center;
        width: 100%;
        padding: 10px 14px;
        margin: 2px 0;
        border-radius: 10px;
        color: #b0b0c8;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        background: transparent;
        text-decoration: none;
    }
    .nav-btn:hover {
        background: rgba(108, 92, 231, 0.12);
        color: #e0e0f0;
    }
    .nav-btn-active {
        background: rgba(108, 92, 231, 0.18) !important;
        color: #ffffff !important;
        border-left: 3px solid #6c5ce7;
    }
    .nav-icon {
        margin-right: 12px;
        font-size: 1.1rem;
        width: 24px;
        text-align: center;
    }

    /* ── Flashcard ── */
    .flashcard {
        background: linear-gradient(135deg, rgba(108, 92, 231, 0.15), rgba(162, 155, 254, 0.08));
        border: 1px solid rgba(108, 92, 231, 0.3);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    .flashcard:hover {
        border-color: rgba(108, 92, 231, 0.5);
        box-shadow: 0 16px 48px rgba(108, 92, 231, 0.15);
        transform: translateY(-2px);
    }
    .flashcard-front {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 600;
        line-height: 1.6;
    }
    .flashcard-back {
        color: #a29bfe;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .flashcard-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 12px;
        color: #6c5ce7;
    }

    /* ── Quiz ── */
    .quiz-question-card {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(22, 33, 62, 0.95));
        border: 1px solid rgba(108, 92, 231, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    .quiz-type-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .badge-mcq { background: rgba(108, 92, 231, 0.2); color: #a29bfe; }
    .badge-short { background: rgba(253, 203, 110, 0.2); color: #fdcb6e; }
    .badge-fill { background: rgba(46, 213, 115, 0.2); color: #2ed573; }
    .badge-tf { background: rgba(116, 185, 255, 0.2); color: #74b9ff; }

    .correct-answer {
        background: rgba(46, 213, 115, 0.08);
        border: 1px solid rgba(46, 213, 115, 0.2);
        border-radius: 10px;
        padding: 10px 14px;
        margin-top: 8px;
        color: #2ed573;
        font-size: 0.88rem;
    }

    /* ── Tabs styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(26, 26, 46, 0.5);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(108, 92, 231, 0.1);
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 24px;
        border-radius: 8px;
        color: #8888aa;
        font-weight: 500;
        font-size: 0.88rem;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(108, 92, 231, 0.2) !important;
        color: #ffffff !important;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.4) !important;
    }

    /* ── File Uploader ── */
    .stFileUploader {
        border: 2px dashed rgba(108, 92, 231, 0.3) !important;
        border-radius: 12px !important;
        background: rgba(108, 92, 231, 0.05) !important;
    }

    /* ── Radio / Checkbox ── */
    .stRadio > label, .stCheckbox > label {
        color: #c0c0d0 !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: rgba(108, 92, 231, 0.08) !important;
        border-radius: 10px !important;
        color: #d0d0e0 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f0f1a; }
    ::-webkit-scrollbar-thumb { background: #6c5ce7; border-radius: 3px; }

    /* ── Download button ── */
    .stDownloadButton > button {
        background: transparent !important;
        border: 1px solid rgba(108, 92, 231, 0.4) !important;
        color: #a29bfe !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover {
        background: rgba(108, 92, 231, 0.1) !important;
        border-color: #6c5ce7 !important;
    }

    /* ── Progress bar ── */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #6c5ce7, #a29bfe) !important;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-top-color: #6c5ce7 !important;
    }

    /* ── Text input ── */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background: rgba(26, 26, 46, 0.8) !important;
        border: 1px solid rgba(108, 92, 231, 0.2) !important;
        border-radius: 10px !important;
        color: #e0e0e0 !important;
    }

    /* ── Metric ── */
    [data-testid="stMetricValue"] {
        color: #a29bfe !important;
        font-size: 1.5rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #8888aa !important;
    }

    /* ── Hide Streamlit branding ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* ── Mind map ── */
    .mindmap-node {
        background: rgba(108, 92, 231, 0.1);
        border: 1px solid rgba(108, 92, 231, 0.25);
        border-radius: 10px;
        padding: 8px 14px;
        margin: 4px 0;
        color: #d0d0e0;
        font-size: 0.88rem;
    }
    .mindmap-root {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
        color: white;
        font-weight: 600;
        padding: 12px 20px;
        border-radius: 14px;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ─── Ensure outputs dir ───────────────────────────────────────
os.makedirs("outputs", exist_ok=True)

# ─── Session State Init ───────────────────────────────────────
defaults = {
    "page": "summary",
    "processed": False,
    "summary_data": None,
    "quiz_data": None,
    "flashcards": None,
    "mindmap_data": None,
    "podcast_path": None,
    "extracted_text": "",
    "file_info": {},
    "quiz_current": 0,
    "quiz_answers": {},
    "quiz_revealed": set(),
    "flash_index": 0,
    "flash_flipped": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    # Logo & Title
    st.markdown("""
    <div style="padding: 1rem 0 0.5rem 0;">
        <div style="font-size: 1.4rem; font-weight: 700; color: #ffffff;">
            🧠 StudyMind AI
        </div>
        <div style="font-size: 0.78rem; color: #8888aa; margin-top: 2px;">
            AI-Powered Study Tool
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # File uploader
    uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf", "txt", "md"], label_visibility="collapsed")

    if uploaded_file and not st.session_state.processed:
        st.markdown(f"""
        <div style="background: rgba(108,92,231,0.1); border-radius:10px; padding:10px 14px; margin:8px 0;
                    border:1px solid rgba(108,92,231,0.2); font-size:0.82rem; color:#c0c0d0;">
            📎 {uploaded_file.name}<br>
            <span style="color:#8888aa; font-size:0.75rem;">
                {round(uploaded_file.size / 1024, 1)} KB
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Process Document", use_container_width=True):
            # Save file
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())

            # Extract text
            with st.spinner("Extracting text..."):
                try:
                    text = extract_text("temp.pdf")
                    st.session_state.extracted_text = text

                    # Count pages
                    try:
                        import fitz
                        doc = fitz.open("temp.pdf")
                        page_count = len(doc)
                        doc.close()
                    except Exception:
                        page_count = text.count("--- Page ")

                    word_count = len(text.split())
                    st.session_state.file_info = {
                        "name": uploaded_file.name,
                        "pages": page_count,
                        "words": word_count
                    }
                except Exception as e:
                    st.error(f"❌ Text extraction failed: {e}")
                    st.stop()

            # Generate summary only (other features on-demand)
            with st.spinner("Generating AI Summary..."):
                try:
                    summary = summarize_pdf(text)
                    st.session_state.summary_data = summary
                except Exception as e:
                    st.error(f"❌ Summary generation failed: {e}")
                    summary = {"overview": "Summary generation failed. Please check your API key in .env file.", "key_topics": [], "definitions": [], "formulas": [], "takeaway": ""}
                    st.session_state.summary_data = summary

            # Build text version of summary for other generators
            summary_text = ""
            if isinstance(summary, dict):
                summary_text = summary.get("overview", "")
                for topic in summary.get("key_topics", []):
                    summary_text += f"\n- {topic.get('title', '')}: {topic.get('description', '')}"
                for defn in summary.get("definitions", []):
                    summary_text += f"\n{defn.get('term', '')}: {defn.get('definition', '')}"
            st.session_state._summary_text = summary_text

            st.session_state.processed = True
            st.rerun()

    # Navigation
    if st.session_state.processed:
        st.markdown('<div class="section-label">STUDY TOOLS</div>', unsafe_allow_html=True)

        quiz_count = len(st.session_state.quiz_data) if st.session_state.quiz_data else 0
        flash_count = len(st.session_state.flashcards) if st.session_state.flashcards else 0

        nav_items = [
            ("summary",    "≡",  "Summary",      None),
            ("quiz",       "⊕",  "Quiz & Q&A",   quiz_count),
            ("flashcards", "▢",  "Flashcards",   flash_count),
            ("mindmap",    "✦",  "Mind Map",     None),
            ("podcast",    "♪",  "Podcast",      None),
        ]

        for key, icon, label, count in nav_items:
            if st.sidebar.button(
                f"{icon}  {label}" + (f"  ({count})" if count else ""),
                key=f"nav_{key}",
                use_container_width=True
            ):
                st.session_state.page = key
                st.rerun()

        st.markdown('<div class="section-label" style="margin-top:2rem;">MORE</div>', unsafe_allow_html=True)

        if st.button("📋  Dev Roadmap", key="nav_roadmap", use_container_width=True):
            pass
        if st.button("➕  Add Feature ↗", key="nav_feature", use_container_width=True):
            pass


# ─── Main Content ─────────────────────────────────────────────

if not st.session_state.processed:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🧠</div>
        <h1 style="color: #ffffff; font-weight: 700; font-size: 2.2rem; margin-bottom: 0.5rem;">
            StudyMind AI
        </h1>
        <p style="color: #8888aa; font-size: 1.05rem; max-width: 500px; margin: 0 auto 2rem auto; line-height: 1.6;">
            Upload any PDF and get an AI-powered summary, quiz questions, flashcards, mind maps, and a study podcast — all in one place.
        </p>
        <div style="display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap; margin-top: 2rem;">
            <div class="glass-card" style="width: 160px; text-align: center; padding: 1.2rem;">
                <div style="font-size: 1.5rem; margin-bottom: 6px;">📄</div>
                <div style="color: #a29bfe; font-weight: 600; font-size: 0.85rem;">Smart Summary</div>
                <div style="color: #8888aa; font-size: 0.75rem; margin-top: 4px;">Structured overview</div>
            </div>
            <div class="glass-card" style="width: 160px; text-align: center; padding: 1.2rem;">
                <div style="font-size: 1.5rem; margin-bottom: 6px;">❓</div>
                <div style="color: #a29bfe; font-weight: 600; font-size: 0.85rem;">Quiz & Q&A</div>
                <div style="color: #8888aa; font-size: 0.75rem; margin-top: 4px;">Test your knowledge</div>
            </div>
            <div class="glass-card" style="width: 160px; text-align: center; padding: 1.2rem;">
                <div style="font-size: 1.5rem; margin-bottom: 6px;">🗂️</div>
                <div style="color: #a29bfe; font-weight: 600; font-size: 0.85rem;">Flashcards</div>
                <div style="color: #8888aa; font-size: 0.75rem; margin-top: 4px;">Quick revision</div>
            </div>
            <div class="glass-card" style="width: 160px; text-align: center; padding: 1.2rem;">
                <div style="font-size: 1.5rem; margin-bottom: 6px;">🧩</div>
                <div style="color: #a29bfe; font-weight: 600; font-size: 0.85rem;">Mind Map</div>
                <div style="color: #8888aa; font-size: 0.75rem; margin-top: 4px;">Visual hierarchy</div>
            </div>
        </div>
        <p style="color: #555; font-size: 0.82rem; margin-top: 3rem;">
            ← Upload a PDF from the sidebar to get started
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    # ─── SUMMARY PAGE ─────────────────────────────────────────
    if st.session_state.page == "summary":
        info = st.session_state.file_info
        summary = st.session_state.summary_data

        # Header
        col_title, col_actions = st.columns([3, 1])
        with col_title:
            st.markdown(f"""
            <div style="margin-bottom: 0.25rem;">
                <span style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">AI Summary</span>
            </div>
            <div style="color: #8888aa; font-size: 0.82rem;">
                {info.get('name', 'document.pdf')} · {info.get('pages', '?')} pages · {info.get('words', 0):,} words
            </div>
            """, unsafe_allow_html=True)

        with col_actions:
            c1, c2 = st.columns(2)
            with c1:
                # Export button
                if summary:
                    full_text = json.dumps(summary, indent=2)
                    st.download_button(
                        "Export ↗",
                        full_text,
                        file_name="summary.json",
                        use_container_width=True
                    )
            with c2:
                if st.button("Analyze ↗", use_container_width=True):
                    st.info("🔍 Deep analysis feature coming soon!")

        st.markdown("---")

        if summary:
            # Tabs
            tab_overview, tab_definitions, tab_formulas = st.tabs(["Overview", "Definitions", "Formulas"])

            # ── Overview Tab ──
            with tab_overview:
                st.markdown("""
                <div class="glass-card">
                    <div style="margin-bottom: 1rem;">
                        <span style="font-size: 1.1rem; font-weight: 600; color: #ffffff;">Overview</span>
                        <span class="ai-badge">AI Generated</span>
                    </div>
                """, unsafe_allow_html=True)

                # Topic paragraph
                overview = summary.get("overview", "No overview available.")
                st.markdown(f"""
                    <div class="topic-label">TOPIC PARAGRAPH</div>
                    <p style="color: #c0c0d0; font-size: 0.92rem; line-height: 1.7; margin-bottom: 1.5rem;">
                        {overview}
                    </p>
                """, unsafe_allow_html=True)

                # Key Topics
                topics = summary.get("key_topics", [])
                if topics:
                    st.markdown('<div class="topic-label">KEY TOPICS &nbsp; ↓</div>', unsafe_allow_html=True)
                    for topic in topics:
                        title = topic.get("title", "")
                        desc = topic.get("description", "")
                        st.markdown(f"""
                        <div class="topic-item">
                            <div class="topic-dot"></div>
                            <div class="topic-text">
                                <strong>{title}</strong> — {desc}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # Takeaway
                takeaway = summary.get("takeaway", "")
                if takeaway:
                    st.markdown(f"""
                    <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(108,92,231,0.06);
                                border-radius: 12px; border-left: 3px solid #6c5ce7;">
                        <div class="topic-label" style="margin-top:0;">TAKEAWAY</div>
                        <p style="color: #c0c0d0; font-size: 0.9rem; line-height: 1.6; margin: 0;">
                            {takeaway}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            # ── Definitions Tab ──
            with tab_definitions:
                definitions = summary.get("definitions", [])
                if definitions:
                    st.markdown("""
                    <div class="glass-card">
                        <div style="margin-bottom: 1rem;">
                            <span style="font-size: 1.1rem; font-weight: 600; color: #ffffff;">Definitions</span>
                            <span class="ai-badge">AI Generated</span>
                        </div>
                    """, unsafe_allow_html=True)

                    for defn in definitions:
                        term = defn.get("term", "")
                        meaning = defn.get("definition", "")
                        st.markdown(f"""
                        <div class="def-card">
                            <div class="def-term">{term}</div>
                            <div class="def-meaning">{meaning}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="glass-card" style="text-align: center; padding: 3rem;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📖</div>
                        <div style="color: #8888aa;">No specific definitions found in this document.</div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Formulas Tab ──
            with tab_formulas:
                formulas = summary.get("formulas", [])
                if formulas:
                    st.markdown("""
                    <div class="glass-card">
                        <div style="margin-bottom: 1rem;">
                            <span style="font-size: 1.1rem; font-weight: 600; color: #ffffff;">Formulas</span>
                            <span class="ai-badge">AI Generated</span>
                        </div>
                    """, unsafe_allow_html=True)

                    for formula in formulas:
                        name = formula.get("name", "")
                        expr = formula.get("formula", "")
                        desc = formula.get("description", "")
                        st.markdown(f"""
                        <div class="formula-card">
                            <div class="formula-name">{name}</div>
                            <div class="formula-expr">{expr}</div>
                            <div class="formula-desc">{desc}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="glass-card" style="text-align: center; padding: 3rem;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔢</div>
                        <div style="color: #8888aa;">No formulas found in this document.</div>
                    </div>
                    """, unsafe_allow_html=True)


    # ─── QUIZ & Q&A PAGE ──────────────────────────────────────
    elif st.session_state.page == "quiz":
        quiz = st.session_state.quiz_data

        st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">Quiz & Q&A</span>
            <span class="ai-badge">AI Generated</span>
        </div>
        """, unsafe_allow_html=True)

        # On-demand quiz generation
        if not quiz:
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📝</div>
                <div style="color: #ffffff; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">Generate Quiz Questions</div>
                <div style="color: #8888aa; font-size: 0.88rem; margin-bottom: 1.5rem;">
                    AI will create 15 quiz questions (MCQ, Short Answer, Fill in Blank, True/False) from your document.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🧠 Generate Quiz Now", use_container_width=True, key="gen_quiz_btn"):
                summary_text = st.session_state.get("_summary_text", "")
                if not summary_text:
                    summary_text = st.session_state.extracted_text[:5000]
                with st.spinner("Generating Quiz Questions..."):
                    try:
                        quiz_result = generate_quiz(summary_text)
                        st.session_state.quiz_data = quiz_result if quiz_result else []
                    except Exception as e:
                        st.error(f"❌ Quiz generation failed: {e}")
                        st.session_state.quiz_data = []
                st.rerun()

        if quiz:
            # Stats bar
            total = len(quiz)
            answered = len(st.session_state.quiz_answers)

            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Total Questions", total)
            with col_stat2:
                st.metric("Answered", answered)
            with col_stat3:
                st.metric("Remaining", total - answered)

            st.progress(answered / total if total > 0 else 0)
            st.markdown("---")

            # Question display
            for i, q in enumerate(quiz):
                q_type = q.get("type", "mcq")
                badge_class = {
                    "mcq": "badge-mcq",
                    "short_answer": "badge-short",
                    "fill_blank": "badge-fill",
                    "true_false": "badge-tf"
                }.get(q_type, "badge-mcq")

                type_label = {
                    "mcq": "MCQ",
                    "short_answer": "Short Answer",
                    "fill_blank": "Fill in Blank",
                    "true_false": "True / False"
                }.get(q_type, q_type.upper())

                st.markdown(f"""
                <div class="quiz-question-card">
                    <span class="quiz-type-badge {badge_class}">{type_label}</span>
                    <div style="color: #e0e0e0; font-size: 0.95rem; font-weight: 500; margin-top: 4px;">
                        Q{i+1}. {q.get('question', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Answer input
                if q_type == "mcq":
                    options = q.get("options", [])
                    if options:
                        answer = st.radio(
                            f"Select answer for Q{i+1}",
                            options,
                            key=f"quiz_q_{i}",
                            label_visibility="collapsed"
                        )
                        if answer:
                            st.session_state.quiz_answers[i] = answer

                elif q_type == "true_false":
                    answer = st.radio(
                        f"Select for Q{i+1}",
                        ["True", "False"],
                        key=f"quiz_q_{i}",
                        label_visibility="collapsed",
                        horizontal=True
                    )
                    if answer:
                        st.session_state.quiz_answers[i] = answer

                elif q_type in ("short_answer", "fill_blank"):
                    answer = st.text_input(
                        f"Your answer for Q{i+1}",
                        key=f"quiz_q_{i}",
                        label_visibility="collapsed",
                        placeholder="Type your answer..."
                    )
                    if answer:
                        st.session_state.quiz_answers[i] = answer

                # Reveal answer button
                if st.button("💡 Reveal Answer", key=f"reveal_{i}"):
                    st.session_state.quiz_revealed.add(i)

                if i in st.session_state.quiz_revealed:
                    correct = q.get("answer", "N/A")
                    explanation = q.get("explanation", "")
                    exp_html = f"<br><span style='color:#a29bfe; font-size:0.82rem;'>→ {explanation}</span>" if explanation else ""
                    st.markdown(f"""
                    <div class="correct-answer">
                        ✅ <strong>Answer:</strong> {correct}{exp_html}
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

            # Export quiz
            st.markdown("---")
            quiz_lines = []
            quiz_lines.append("=" * 50)
            quiz_lines.append("QUIZ QUESTIONS")
            quiz_lines.append("=" * 50 + "\n")
            for qi, qq in enumerate(quiz, 1):
                quiz_lines.append(f"Q{qi}. [{qq.get('type', 'unknown').upper()}] {qq.get('question', '')}")
                if qq.get('type') == 'mcq':
                    for opt in qq.get('options', []):
                        quiz_lines.append(f"   {opt}")
                quiz_lines.append("")
            quiz_lines.append("\n" + "=" * 50)
            quiz_lines.append("ANSWER KEY")
            quiz_lines.append("=" * 50 + "\n")
            for qi, qq in enumerate(quiz, 1):
                quiz_lines.append(f"Q{qi}: {qq.get('answer', 'N/A')}")
                if 'explanation' in qq:
                    quiz_lines.append(f"   → {qq['explanation']}")
            quiz_text = "\n".join(quiz_lines)
            st.download_button(
                "📥 Download Quiz",
                quiz_text,
                file_name="quiz.txt",
                use_container_width=True
            )


    # ─── FLASHCARDS PAGE ──────────────────────────────────────
    elif st.session_state.page == "flashcards":
        cards = st.session_state.flashcards

        st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">Flashcards</span>
            <span class="ai-badge">AI Generated</span>
        </div>
        """, unsafe_allow_html=True)

        # On-demand flashcard generation
        if not cards:
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🗂️</div>
                <div style="color: #ffffff; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">Generate Flashcards</div>
                <div style="color: #8888aa; font-size: 0.88rem; margin-bottom: 1.5rem;">
                    AI will create 15 study flashcards — key terms, concepts, and important facts.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🧠 Generate Flashcards Now", use_container_width=True, key="gen_flash_btn"):
                summary_text = st.session_state.get("_summary_text", "")
                if not summary_text:
                    summary_text = st.session_state.extracted_text[:5000]
                with st.spinner("Creating Flashcards..."):
                    try:
                        cards_result = generate_flashcards(summary_text)
                        st.session_state.flashcards = cards_result if cards_result else []
                    except Exception as e:
                        st.error(f"❌ Flashcard generation failed: {e}")
                        st.session_state.flashcards = []
                st.rerun()

        if cards:
            total = len(cards)
            idx = st.session_state.flash_index

            # Clamp index
            if idx >= total:
                idx = total - 1
                st.session_state.flash_index = idx

            # Progress
            st.progress((idx + 1) / total)
            st.markdown(f"""
            <div style="text-align: center; color: #8888aa; font-size: 0.82rem; margin-bottom: 1.5rem;">
                Card {idx + 1} of {total}
            </div>
            """, unsafe_allow_html=True)

            # Card display
            card = cards[idx]
            flipped = st.session_state.flash_flipped

            if not flipped:
                st.markdown(f"""
                <div class="flashcard">
                    <div class="flashcard-label">QUESTION</div>
                    <div class="flashcard-front">{card.get('front', '')}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="flashcard" style="border-color: rgba(162, 155, 254, 0.4);">
                    <div class="flashcard-label" style="color: #a29bfe;">ANSWER</div>
                    <div class="flashcard-back">{card.get('back', '')}</div>
                </div>
                """, unsafe_allow_html=True)

            # Controls
            col_prev, col_flip, col_next = st.columns([1, 2, 1])

            with col_prev:
                if st.button("← Previous", use_container_width=True, disabled=(idx == 0)):
                    st.session_state.flash_index = max(0, idx - 1)
                    st.session_state.flash_flipped = False
                    st.rerun()

            with col_flip:
                flip_label = "🔄 Show Question" if flipped else "🔄 Flip Card"
                if st.button(flip_label, use_container_width=True):
                    st.session_state.flash_flipped = not flipped
                    st.rerun()

            with col_next:
                if st.button("Next →", use_container_width=True, disabled=(idx >= total - 1)):
                    st.session_state.flash_index = min(total - 1, idx + 1)
                    st.session_state.flash_flipped = False
                    st.rerun()

            # All cards overview
            with st.expander(f"📋 View All {total} Cards"):
                for j, c in enumerate(cards):
                    st.markdown(f"""
                    <div class="def-card" style="cursor: pointer;">
                        <div class="def-term">#{j+1} — {c.get('front', '')}</div>
                        <div class="def-meaning">{c.get('back', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)


    # ─── MIND MAP PAGE ────────────────────────────────────────
    elif st.session_state.page == "mindmap":
        st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">Mind Map</span>
            <span class="ai-badge">AI Generated</span>
        </div>
        """, unsafe_allow_html=True)

        mindmap = st.session_state.mindmap_data

        # On-demand mindmap generation
        if not mindmap or (isinstance(mindmap, dict) and not mindmap.get("children")):
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🧩</div>
                <div style="color: #ffffff; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">Generate Mind Map</div>
                <div style="color: #8888aa; font-size: 0.88rem; margin-bottom: 1.5rem;">
                    AI will create a visual hierarchical mind map of your document's key topics.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🧠 Generate Mind Map Now", use_container_width=True, key="gen_mm_btn"):
                summary_text = st.session_state.get("_summary_text", "")
                if not summary_text:
                    summary_text = st.session_state.extracted_text[:5000]
                with st.spinner("Building Mind Map..."):
                    try:
                        mm_result = generate_mindmap(summary_text)
                        st.session_state.mindmap_data = mm_result if mm_result else {"title": "Mind Map", "children": []}
                    except Exception as e:
                        st.error(f"❌ Mind map generation failed: {e}")
                        st.session_state.mindmap_data = {"title": "Mind Map", "children": []}
                st.rerun()

        if mindmap and isinstance(mindmap, dict) and mindmap.get("children"):
            # Build Graphviz graph
            dot = graphviz.Digraph(
                comment="Mind Map",
                graph_attr={
                    "bgcolor": "transparent",
                    "rankdir": "TB",
                    "splines": "ortho",
                    "nodesep": "0.6",
                    "ranksep": "0.8",
                    "pad": "0.5",
                },
                node_attr={
                    "shape": "box",
                    "style": "filled,rounded",
                    "fillcolor": "#1a1a2e",
                    "color": "#6c5ce7",
                    "fontcolor": "#e0e0e0",
                    "fontname": "Inter, Arial",
                    "fontsize": "11",
                    "penwidth": "1.5",
                    "margin": "0.2,0.1",
                },
                edge_attr={
                    "color": "#6c5ce755",
                    "arrowhead": "none",
                    "penwidth": "1.5",
                }
            )

            def add_nodes(node, parent_id=None, depth=0):
                node_id = str(id(node))
                title = node.get("title", "?")

                if depth == 0:
                    dot.node(node_id, title, fillcolor="#6c5ce7", fontcolor="white",
                             fontsize="14", penwidth="2")
                elif depth == 1:
                    dot.node(node_id, title, fillcolor="#16213e", fontsize="12",
                             color="#a29bfe")
                else:
                    dot.node(node_id, title, fillcolor="#12121f", fontsize="10",
                             color="#444466")

                if parent_id:
                    dot.edge(parent_id, node_id)

                for child in node.get("children", []):
                    add_nodes(child, node_id, depth + 1)

            add_nodes(mindmap)
            st.graphviz_chart(dot, use_container_width=True)

            # Expandable hierarchy
            with st.expander("📋 View Hierarchy as List"):
                def render_hierarchy(node, level=0):
                    indent = "&nbsp;" * (level * 6)
                    title = node.get("title", "?")
                    if level == 0:
                        st.markdown(f'<div class="mindmap-root">{title}</div>', unsafe_allow_html=True)
                    else:
                        bullet = "●" if level == 1 else "○"
                        color = "#a29bfe" if level == 1 else "#8888aa"
                        st.markdown(
                            f'<div style="padding: 3px 0; color: {color}; font-size: 0.88rem;">'
                            f'{indent}{bullet} {title}</div>',
                            unsafe_allow_html=True
                        )
                    for child in node.get("children", []):
                        render_hierarchy(child, level + 1)

                render_hierarchy(mindmap)


    # ─── PODCAST PAGE ─────────────────────────────────────────
    elif st.session_state.page == "podcast":
        st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">Podcast</span>
            <span class="ai-badge">AI Generated</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
            <div style="color: #c0c0d0; font-size: 0.92rem; line-height: 1.6;">
                Generate an AI podcast from your study material. Two hosts discuss the key topics
                in a conversational format — perfect for learning on the go.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.podcast_path and os.path.exists(st.session_state.podcast_path):
            st.audio(st.session_state.podcast_path, format="audio/mp3")
            with open(st.session_state.podcast_path, "rb") as f:
                st.download_button(
                    "🎧 Download Podcast",
                    f.read(),
                    file_name="podcast.mp3",
                    use_container_width=True
                )
        else:
            if st.session_state.processed:
                st.warning("⚠️ Podcast generation requires Kokoro TTS library and takes a few minutes.")
                if st.button("🎙️ Generate Podcast", use_container_width=True):
                    summary_text = st.session_state.get("_summary_text", "")
                    if summary_text:
                        with st.spinner("🎙️ Generating podcast — this may take a few minutes..."):
                            try:
                                mp3_path = create_podcast(summary_text)
                                st.session_state.podcast_path = mp3_path
                                st.rerun()
                            except Exception as e:
                                st.error(f"Podcast generation failed: {e}")
                    else:
                        st.error("No summary text available.")
            else:
                st.info("Process a PDF first to generate a podcast.")
