# Social Support AI (SSA) – Local LLM Document Intelligence & Eligibility System

[![Built with FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi)]()
[![Powered by Ollama](https://img.shields.io/badge/Local%20LLM-Ollama-000000?logo=ollama)]()
[![GPU Enabled](https://img.shields.io/badge/NVIDIA-GPU%20Accelerated-76B900?logo=nvidia)]()
[![LangGraph Agents](https://img.shields.io/badge/Agent%20Orchestration-LangGraph-blue)]()
[![Qdrant Vector DB](https://img.shields.io/badge/Vector%20DB-Qdrant-FF4F8B)]()

Social Support AI automates **document intelligence**, **OCR parsing**, **data extraction**, **eligibility scoring** and **AI-powered justification** for **government welfare screening**—fully **offline** with **local LLMs** and **GPU acceleration** using Ollama.

✅ **End-to-end production-grade AI system**
✅ **Local-first GenAI with Ollama (GPU)**
✅ **Document understanding via OCR + RAG + Vector Search**
✅ **Explainable ML eligibility decision pipeline**
✅ **Agentic orchestration for reasoning pipeline**
✅ **FastAPI backend + Streamlit UI**
✅ **Langfuse observability + Dockerized microservices**

---

## 👨‍💻 Author
**Ahsanullah MRM**
Senior Python & Generative AI Engineer
🔗 LinkedIn: https://www.linkedin.com/in/ahsanullah-mrm-3623789b/

---

## 🚀 Project Overview

The **Social Support AI** system automates eligibility decisions for social welfare applications using **documents + ML + LLM-based reasoning**.

**Citizens upload:**
- ✅ Emirates ID (Front + Back)
- ✅ Bank Statements
- ✅ Salary Certificates
- ✅ Utility Bills (optional)

**The system then:**
1. Extracts text/tables using **PDF/Image/Tesseract OCR**
2. Embeds chunks → stores them in **Qdrant Vector DB**
3. Uses **RAG search** for citations
4. Runs **GenAI reasoning with Ollama LLM (GPU)**
5. Applies **Rule-based + ML eligibility scoring**
6. Generates **human-readable justification**
7. **Agents orchestrate** extraction → validation → eligibility → explanation

---

## 🎯 Key Features
✅ Upload & parse ID cards, salary slips, bank statements
✅ OCR for PDF/JPG/PNG + Excel table extraction
✅ Vector search (RAG) with Qdrant + embeddings
✅ LangGraph agents: extraction → validation → eligibility → reasoning
✅ GPU-powered LLM decision explanation via **Ollama**
✅ Hybrid backend: PostgreSQL + MongoDB + Qdrant
✅ Streamlit UI + FastAPI Backend
✅ Secure JWT authentication
✅ Audit logging + explainability
✅ **ReAct Prompting** framework for agent reasoning

---

## 🧱 System Architecture

```
Streamlit UI  →  FastAPI Backend  →  LangGraph Agent Orchestrator
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   PostgreSQL      MongoDB          Qdrant
(metadata + audit) (parsed docs)  (embeddings)
        │               │               │
        └───────────────┼───────────────┘
                        ↓
                  Ollama LLM (GPU)
                        ↓
                   Langfuse (Tracing)
```

---

## 🔧 Tech Stack Summary

| Category | Tools |
|-----------|-------|
| Programming Language | Python 3.11 |
| Server Framework | FastAPI |
| Frontend | Streamlit |
| Agent Orchestration | LangGraph |
| Local AI Runtime | Ollama (GPU enabled) |
| Embeddings | BAAI/bge-small-en-v1.5 (Sentence Transformers) |
| Vector DB | Qdrant |
| Relational DB | PostgreSQL |
| NoSQL DB | MongoDB |
| Optional Graph DB | Neo4j (planned extension) |
| OCR | PDFPlumber + Tesseract + Pandas (XLSX) |
| ML Scoring | Scikit-learn (Logistic Regression) |
| Reasoning Framework | ReAct Prompting |
| Observability | Langfuse |
| Deployment | Docker Compose |
| Dev Quality | Ruff, Black, Mypy, Pre-commit |
| Version Control | GitHub + pre-commit hooks |
| Architecture Style | Modular Microservice inside Monorepo |

---

## 📦 System Components

| Service | Description |
|----------|-------------|
| **FastAPI (API)** | Serves ingestion, RAG, ML scoring, LLM justification |
| **Streamlit (UI)** | Web interface for application intake |
| **Ollama** | Runs local LLM **on GPU** (llama3.2:3b) |
| **Qdrant** | Vector DB for semantic retrieval |
| **PostgreSQL** | Stores applications + audit logs |
| **MongoDB** | Stores parsed artifacts |
| **Langfuse** | Observability: traces every LLM call |
| **Agent Runner** | Orchestrates reasoning pipeline using LangGraph |

---

## ⚡ GPU + Local LLM Strategy

| Component | Runtime | Hardware |
|-----------|---------|----------|
| Ollama LLM Inference | ✅ GPU | NVIDIA RTX 3050 4GB |
| Embedding Model (BAAI/bge-small-en-v1.5) | ✅ CPU | Light embedding model |
| OCR (PDF/Image Parsing) | ✅ CPU | Fast processing |
| ML Classifier | ✅ CPU | Scikit-learn |
| LangGraph Agents | ✅ CPU | Orchestration |
| API + UI Backend | ✅ CPU | FastAPI + Streamlit |
| Vector DB + Databases | ✅ CPU | Qdrant + Postgres + MongoDB |

✅ **Privacy First** – No cloud APIs.
✅ **Runs offline** – Works locally using Docker Compose.
✅ **Production modular design** – Built for extensibility.
✅ **GPU enabled** via NVIDIA Container Toolkit on WSL2.

---

## ✅ Prerequisites

| Requirement | Version/Details |
|-------------|-----------------|
| Python | 3.11+ |
| Docker & Docker Compose | Latest |
| WSL2 + Ubuntu | Recommended for Windows |
| NVIDIA GPU | RTX 3050 or better (4GB+ VRAM) |
| NVIDIA GPU Drivers | Required |
| NVIDIA Container Toolkit | Required for Docker GPU access |
| Git | Latest |

---

## 🔧 Local Setup (Step-by-Step)

### 1️⃣ Clone & Enter Repository

```bash
git clone https://github.com/your-username/social-support-ai.git
cd social-support-ai
```

---

### 2️⃣ Install NVIDIA Container Toolkit (WSL2/Linux)

```bash
sudo apt update
sudo apt install nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo service docker restart
```

---

### 3️⃣ Setup Project Environment

```bash
make setup
```

---

### 4️⃣ Start All Services

```bash
make up
make logs
```

---

### ✅ Health Check

| Service | URL |
|---------|-----|
| FastAPI Backend | [http://localhost:8080/healthz](http://localhost:8080/healthz) |
| Document UI | [http://localhost:8501](http://localhost:8501) |
| Ollama (LLM Runtime) | [http://localhost:11434](http://localhost:11434) |
| Langfuse Dashboard | [http://localhost:3100](http://localhost:3100) |

---

## 🔥 Quick Demo Commands

### Create Application

```bash
APP_ID=$(curl -s -X POST http://localhost:8080/applications \
  -H "Content-Type: application/json" \
  -d '{"applicant_full_name": "John Doe"}' | jq -r .id)
```

### Upload Document

```bash
curl -s -F "doc_type=bank_statement" \
     -F "file=@sample.pdf" \
     http://localhost:8080/applications/$APP_ID/documents
```

### Parse Document

```bash
curl -X POST http://localhost:8080/documents/$DOC_ID/parse
```

### Evaluate Eligibility

```bash
curl -X POST http://localhost:8080/applications/$APP_ID/evaluate
```

### Generate LLM Justification

```bash
curl -X POST http://localhost:8080/applications/$APP_ID/justify
```

### Semantic Search

```bash
curl "http://localhost:8080/applications/$APP_ID/search?q=salary"
```

---

## 📂 Project Structure

```
social-support-ai/
├── apps/
│   ├── api/              # FastAPI backend
│   └── ui/               # Streamlit UI
├── services/
│   ├── agents/           # LangGraph workflows
│   ├── rag/              # Chunk + Embed + Search
│   ├── ocr/              # PDF/Image/XLSX parsers
│   ├── eligibility/      # ML model + rules
│   ├── llm/              # Ollama client
│   └── observability/    # Langfuse tracing
├── infra/
│   ├── compose/          # Docker Compose setup
│   └── db/               # SQL migrations
├── scripts/
│   └── infra_bootstrap.sh # Pull Ollama model helper
├── eval/
│   ├── unit/             # Unit tests
│   └── integration/      # End-to-end tests
└── docs/                 # Architecture & decisions
```

---

## 🛣️ Roadmap

- [ ] Add GitHub Actions CI/CD
- [ ] Deploy optional cloud variant
- [ ] Add Neo4j knowledge graph expansion
- [ ] Multi-language OCR support
- [ ] Advanced fraud detection models
- [ ] Enhanced agent reasoning patterns
- [ ] Real-time document streaming

---

## 🧪 Testing

```bash
# Run unit tests
make test-unit

# Run integration tests
make test-integration

# Run all tests
make test
```

---

## 📊 Monitoring & Observability

The system uses **Langfuse** for comprehensive observability:
- ✅ Trace every LLM call
- ✅ Monitor agent execution paths
- ✅ Track token usage and latency
- ✅ Debug reasoning chains
- ✅ Audit all decisions

Access Langfuse dashboard at: [http://localhost:3100](http://localhost:3100)

---

## 🔒 Security Features

- JWT authentication for API access
- Audit logging for all operations
- Document encryption at rest
- Role-based access control
- Privacy-first local processing
- No external API dependencies

---

## 📄 License

This is a **private project** – not for public or commercial redistribution.

---

## 🤝 Contributing

This is a private portfolio project. For inquiries, please contact the author directly.

---

**Built with ❤️ for intelligent, privacy-preserving social welfare automation**
