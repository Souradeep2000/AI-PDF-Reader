# 🚀 AI Study Platform (PDF Q&A & Test Generator)

An AI-powered study platform that transforms PDFs into an interactive learning experience. Upload study material, ask contextual questions, generate tests, and gain study insights.

Built with a scalable architecture focused on intelligent document understanding, semantic retrieval, and production-oriented engineering practices.

---

## ✨ Features

### 📄 Intelligent PDF Processing

- Drag & drop PDF upload
- Text extraction from documents
- OCR support for scanned PDFs (planned)
- Background document processing pipeline

### 💬 Context-Aware Document Chat

- Ask questions directly from uploaded PDFs
- Contextual answers grounded in document content
- Streaming responses for real-time interaction
- Citation-based answer generation
- Retrieval-Augmented Generation (RAG)

### 🔍 Semantic Retrieval

- Meaning-based search using vector embeddings
- Faster and more relevant context retrieval
- Context ranking for improved answer quality

### 📝 AI Test Generation

- Generate quizzes from uploaded study material
- Topic-based question generation
- Smart assessment workflows

### 📊 Analytics Dashboard

- Study interaction insights
- Learning analytics
- Document usage tracking
- Progress visualization

---

## 🏗️ Architecture

```text
Angular Frontend (PWA)
        ↓
     FastAPI Backend
        ↓
 ┌─────────────────────────┐
 │ PostgreSQL + pgvector   │
 │ Redis Cache             │
 │ RabbitMQ Queue          │
 └─────────────────────────┘
        ↓
 Document Processing Pipeline
        ↓
 Embeddings + Semantic Retrieval + RAG
```

---

## 🚀 Running the Project Locally

### 1️⃣ Clone the Repository

```bash
git clone <my-repository-url>
cd <your-project-folder>
```

---

### 2️⃣ Frontend Setup (Angular)

Navigate to frontend:

```bash
cd FrontEnd
```

Install dependencies:

```bash
npm install
```

Start Angular development server:

```bash
ng serve
```

Frontend will run on:

```text
http://localhost:4200
```

---

### 3️⃣ Backend Setup (FastAPI)

Open a new terminal and navigate to backend:

```bash
cd Backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Mac / Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend server:

```bash
uvicorn main:app --reload
```

OR (if using app folder structure)

```bash
uvicorn app.main:app --reload
```

Backend will run on:

```text
http://localhost:8000
```
