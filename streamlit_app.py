"""
Streamlit UI — RAG Chatbot Demo
Author: Rangaswamy Challa | github.com/Rangarana
"""

import streamlit as st
import time
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from rag_engine import RAGEngine

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Chatbot | Rangaswamy Challa",
    page_icon="🤖",
    layout="wide"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0D1117; }
    .stApp { background-color: #0D1117; color: #E6EDF3; }
    .title-text {
        font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(90deg, #58A6FF, #3FB950);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .subtitle { color: #8B949E; font-size: 1rem; margin-bottom: 2rem; }
    .answer-box {
        background: #161B22; border: 1px solid #30363D;
        border-left: 4px solid #3FB950;
        padding: 1.2rem; border-radius: 8px; margin: 1rem 0;
    }
    .source-tag {
        background: #21262D; border: 1px solid #30363D;
        padding: 3px 10px; border-radius: 100px;
        font-size: 0.75rem; color: #8B949E;
        display: inline-block; margin: 2px;
    }
    .metric-card {
        background: #161B22; border: 1px solid #30363D;
        border-radius: 8px; padding: 1rem; text-align: center;
    }
    .stButton > button {
        background: #238636; color: white;
        border: none; border-radius: 6px;
        padding: 0.5rem 1.5rem; font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover { background: #2ea043; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "rag" not in st.session_state:
    st.session_state.rag = RAGEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed" not in st.session_state:
    st.session_state.indexed = False
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0
if "avg_time" not in st.session_state:
    st.session_state.avg_time = 0.0

# ─── HEADER ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p class="title-text">🤖 RAG Chatbot</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Production-ready · Chat with your documents · Built by <a href="https://github.com/Rangarana" style="color:#58A6FF;">Rangaswamy Challa</a></p>', unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="text-align:right; padding-top:10px;">
        <a href="https://github.com/Rangarana" style="color:#58A6FF; text-decoration:none; font-size:0.85rem;">
            ⭐ GitHub
        </a> &nbsp;|&nbsp;
        <a href="https://linkedin.com/in/rangaswamy-challa-63b822241" style="color:#58A6FF; text-decoration:none; font-size:0.85rem;">
            💼 LinkedIn
        </a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─── LAYOUT ───────────────────────────────────────────────────────────────────
sidebar, chat_col = st.columns([1, 2])

# ─── SIDEBAR: UPLOAD & STATS ──────────────────────────────────────────────────
with sidebar:
    st.markdown("### 📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF, TXT, or CSV",
        type=["pdf", "txt", "csv"],
        accept_multiple_files=True
    )

    if uploaded_files:
        os.makedirs("data/sample_docs", exist_ok=True)
        for f in uploaded_files:
            with open(f"data/sample_docs/{f.name}", "wb") as out:
                out.write(f.read())
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")

    st.markdown("")
    if st.button("⚡ Build Index & Start Chatting"):
        with st.spinner("Chunking & embedding documents..."):
            result = st.session_state.rag.build_index("data/sample_docs")
            if result["status"] == "success":
                st.session_state.indexed = True
                st.success(f"✅ Indexed {result['documents_loaded']} docs → {result['chunks_created']} chunks")
            else:
                st.error(result.get("message", "Error building index"))

    st.divider()
    st.markdown("### 📊 Stats")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Queries", st.session_state.total_queries)
    with c2:
        st.metric("Avg Time", f"{st.session_state.avg_time:.1f}s")

    st.markdown("")
    status_color = "🟢" if st.session_state.indexed else "🔴"
    st.markdown(f"{status_color} Index: **{'Ready' if st.session_state.indexed else 'Not built'}**")

    st.divider()
    st.markdown("### 🛠️ Tech Stack")
    for tech in ["Python 3.10+", "LangChain", "FAISS", "OpenAI", "FastAPI", "Streamlit"]:
        st.markdown(f"`{tech}`", unsafe_allow_html=True)

# ─── CHAT INTERFACE ───────────────────────────────────────────────────────────
with chat_col:
    st.markdown("### 💬 Chat with your Documents")

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "sources" in msg:
                if msg["sources"]:
                    st.markdown("**Sources:** " + " ".join(
                        [f'<span class="source-tag">📄 {s.split("/")[-1]}</span>'
                         for s in msg["sources"]]
                    ), unsafe_allow_html=True)
                st.caption(f"⏱ Response time: {msg.get('time', 0):.2f}s")

    # Chat input
    if prompt := st.chat_input("Ask anything about your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if not st.session_state.indexed:
                answer = "⚠️ Please upload documents and click **Build Index** first!"
                sources = []
                elapsed = 0
            else:
                with st.spinner("Searching documents..."):
                    start = time.time()
                    answer, sources = st.session_state.rag.query(prompt)
                    elapsed = round(time.time() - start, 2)

                # Update stats
                st.session_state.total_queries += 1
                n = st.session_state.total_queries
                st.session_state.avg_time = (
                    (st.session_state.avg_time * (n - 1) + elapsed) / n
                )

            st.markdown(answer)
            if sources:
                st.markdown("**Sources:** " + " ".join(
                    [f'<span class="source-tag">📄 {s.split("/")[-1]}</span>'
                     for s in sources]
                ), unsafe_allow_html=True)
            if elapsed:
                st.caption(f"⏱ Response time: {elapsed:.2f}s")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "time": elapsed
        })
