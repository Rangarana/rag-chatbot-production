# 🤖 RAG Chatbot — Production-Ready AI Document Q&A System

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-005571?style=flat&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-0.1-1C3C3C?style=flat)
![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-0467DF?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

> **Built by [Rangaswamy Challa](https://github.com/Rangarana) — AI Developer | Open to Freelance & Remote**

---

## 📌 What This Does

A **production-ready RAG (Retrieval-Augmented Generation)** system that lets any business
chat with their own documents using AI.

```
Upload PDF/TXT/CSV  →  Ask any question  →  Get precise answers in ~1.2 seconds
```

✅ Answers only from YOUR documents — zero hallucinations  
✅ Full REST API with Swagger docs  
✅ Beautiful Streamlit chat UI  
✅ Supports PDF, TXT, CSV  
✅ FAISS vector search for fast retrieval  

---

## 🏗️ Architecture

```
┌─────────────┐   ┌──────────────┐   ┌─────────────────┐
│  Documents  │──▶│  Chunking &  │──▶│  Vector Store   │
│ PDF/TXT/CSV │   │  Embeddings  │   │  FAISS Index    │
└─────────────┘   └──────────────┘   └────────┬────────┘
                                               │ Similarity Search
┌─────────────┐   ┌──────────────┐   ┌────────▼────────┐
│  User Query │──▶│  GPT-3.5/4   │◀──│  Top-K Context  │
│  via API    │   │  LangChain   │   │    Retrieved    │
└─────────────┘   └──────┬───────┘   └─────────────────┘
                         │
                  ┌──────▼───────┐
                  │   Response   │
                  │  via FastAPI │
                  └──────────────┘
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Clone the repository
```bash
git clone https://github.com/Rangarana/rag-chatbot-production
cd rag-chatbot-production
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
```bash
cp .env.example .env
# Open .env and add your OpenAI API key
```

### 4a. Run the Streamlit UI (Easiest)
```bash
streamlit run streamlit_app.py
# Open http://localhost:8501
```

### 4b. Run the FastAPI Backend
```bash
uvicorn src.app:app --reload
# Open http://localhost:8000/docs
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | API info & available endpoints |
| `GET`  | `/health` | Check if index is ready |
| `POST` | `/upload` | Upload a document (PDF/TXT/CSV) |
| `POST` | `/ingest` | Index all uploaded documents |
| `POST` | `/query` | Ask a question, get an answer |

### Example Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What services do you offer?"}'
```

### Example Response
```json
{
  "question": "What services do you offer?",
  "answer": "We offer RAG systems, LLM API development, and custom AI chatbots...",
  "sources": ["sample_knowledge_base.txt"],
  "response_time_seconds": 1.18,
  "status": "success"
}
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend API | FastAPI + Python 3.10 |
| LLM | OpenAI GPT-3.5/GPT-4 |
| Orchestration | LangChain |
| Vector Database | FAISS |
| Embeddings | OpenAI text-embedding-ada-002 |
| UI | Streamlit |
| Document Loading | PyPDF, TextLoader, CSVLoader |

---

## 📁 Project Structure

```
rag-chatbot-production/
│
├── src/
│   ├── app.py              ← FastAPI backend
│   └── rag_engine.py       ← Core RAG logic
│
├── data/
│   └── sample_docs/        ← Put your documents here
│
├── streamlit_app.py        ← Chat UI
├── requirements.txt
├── .env.example            ← Copy to .env and add API key
├── .gitignore
└── README.md
```

---

## 💼 Use Cases

- 🏢 **Businesses** — Chat with company knowledge bases, SOPs, manuals
- ⚖️ **Law Firms** — Query thousands of case files instantly
- 🏥 **Healthcare** — Search medical documents and protocols
- 🛒 **E-commerce** — AI support on product manuals
- 👥 **HR Teams** — Instant answers from policy documents

---

## 👨‍💻 About the Developer

Built by **Rangaswamy Challa** — AI Developer specializing in production-grade
Generative AI systems, RAG pipelines, and LLM applications.

📧 challarangaswami@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/rangaswamy-challa-63b822241)  
💼 **Available for freelance projects globally**

---

## 📄 License

MIT License — free to use, modify, and distribute.
