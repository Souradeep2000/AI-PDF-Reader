---
title: AI Docs Reader Backend
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
dockerfile: BackEnd/Dockerfile.hf
---

# 🚀 AI DOCS READER Platform (PDF/DOCX/ANY FILES Q&A & Test Generator)

An AI-powered study platform that transforms all Documents into an interactive learning or Q&A experience. Upload study/work material, ask contextual questions, generate tests, and gain study insights.

Built with a scalable architecture focused on intelligent document understanding, semantic retrieval, and production-oriented engineering practices.

---

## ✨ Features

### 📄 Intelligent FILES Processing

- Drag & drop FILE upload
- Text extraction from documents
- OCR support for scanned Files
- Background document processing pipeline

```
PDF     → PyMuPDF
Image   → OCR (Teserract ocr)
DOCX    → python-docx
TXT     → direct read
PPTX    → python-pptx
```

### 💬 Context-Aware Document Chat

- Ask questions directly from uploaded Files
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
 │ Redis Cache             │
 │ RabbitMQ Queue          │
 └─────────────────────────┘
        ↓
 detect file type
        ↓
 route to parser
        ↓
Text Extraction (PDF/DOCX/TXT/Image OCR)
        ↓
Text Cleaning
        ↓
     chunking
        ↓
   Embeddings
        ↓
 ┌─────────────────────────┐
 │ PostgreSQL + pgvector   │
 └─────────────────────────┘
        ↓
  Semantic Retrieval
        ↓
    RAG Q&A ( Ollama local LLM/Gemini Prod LLM)
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

### 3️⃣ Backend Setup (FastAPI) Docker

Open a new terminal and navigate to backend:

```bash
cd Backend
```

For 1st time build For docker: delete docker desktop image first

```bash
docker compose down
docker compose up --build
```

---

To run server:

```bash
docker compose up
```

Backend will run on:

```text
http://localhost:8000
```

Check logs :

```bash
docker logs pdf-qna-backend
```

check postgres db on startup:

```bash
docker exec -it pdf-qna-postgres psql -U postgres
```

```sql
\l
\dt
```

You should finally see:

```text
documents
document_chunks
```

---

### 3️⃣ Without Docker (FastAPI)

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

#### Windows

```bash
source venv/Scripts/activate
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
PYTHONPATH=. uvicorn app.main:app --reload
```

OR (if using app folder structure)

```bash
uvicorn app.main:app --reload
```

Backend will run on:

```text
http://localhost:8000
```

---

# Why Semantic Search + pgvector is Required

A natural question while building a document-based AI platform is:

> Why do we need semantic search and a vector database like pgvector?
>
> Why not simply upload the document and send the entire file to the LLM?

A simpler implementation could look like this:

1. Upload document
2. Extract full text
3. Send the entire document to the LLM
4. Ask the model to answer only from the uploaded content

Example:

```text
User uploads a 5-page PDF

Prompt:

"Here is the uploaded document:

<entire document text>

Answer only from this document."
```

For **small files**, this approach can work reasonably well.

So why introduce additional complexity with:

- chunking
- embeddings
- semantic search
- pgvector
- Retrieval-Augmented Generation (RAG)

The answer is **scalability, performance, and reliability**.

---

## Problem 1: Large Documents Break the Prompting Approach

LLMs cannot process unlimited text efficiently.

For example:

```text
5-page PDF → manageable
200-page study notes → inefficient
Multiple PDFs → impractical
```

Sending the **entire document** for every question quickly becomes problematic.

Imagine a student uploads:

- Operating Systems notes
- DBMS notes
- Computer Networks notes
- Machine Learning notes

Now suppose they ask:

> "Explain deadlock prevention"

Sending **all uploaded content** into the prompt for every question would be extremely inefficient.

Instead, our system retrieves **only the relevant sections**.

Example:

```text
Question:
"What is deadlock prevention?"

Retrieved Context:
OS Chapter 7 → Deadlock Prevention
OS Chapter 8 → Resource Allocation
```

Only relevant chunks are sent to the LLM.

This keeps the system scalable.

---

## Problem 2: Better Accuracy Through Focused Context

More information does **not always mean better answers**.

When an LLM receives a massive document, it may:

- miss relevant sections
- mix unrelated concepts
- generate inaccurate responses

Example:

A relevant explanation may exist on:

```text
Page 173
```

inside a 300-page document.

The model must search through everything.

Instead, semantic retrieval narrows the context first.

The system retrieves:

```text
Only chunks related to deadlock prevention
```

Then the LLM answers using focused context.

Result:

```text
More grounded and accurate responses
```

---

## Problem 3: Semantic Understanding vs Keyword Matching

Traditional keyword search is limited.

Example:

Document says:

```text
Workers process delayed jobs.
```

User asks:

```text
How are postponed jobs executed?
```

Keyword search fails because:

```text
postponed ≠ delayed
```

Semantic search succeeds because embeddings understand meaning.

The system recognizes:

```text
postponed ≈ delayed
executed ≈ process
```

This makes retrieval significantly smarter.

---

## Problem 4: Faster Responses

Without retrieval:

```text
Entire document
→ huge prompt
→ slower inference
```

With semantic search:

```text
Top relevant chunks
→ smaller prompt
→ faster responses
```

This becomes especially important for local inference using Ollama.

---

## Problem 5: Lower Cost in Production

Cloud LLMs charge based on tokens.

Without retrieval:

```text
Every query = full document
```

With retrieval:

```text
Every query = only relevant chunks
```

This drastically reduces token usage and inference cost.

---

## Our Solution: Retrieval-Augmented Generation (RAG)

Instead of prompting with the full document, our system uses a **RAG pipeline**.

Flow:

```text
Upload Document
        ↓
OCR / Text Extraction
        ↓
Text Cleaning
        ↓
Chunking
        ↓
Embedding Generation
(BAAI/bge-small-en-v1.5)
        ↓
pgvector Storage
        ↓
User Question
        ↓
Query Embedding
        ↓
Semantic Search
(Top-K Relevant Chunks)
        ↓
LLM (Gemini / Ollama)
        ↓
Grounded Answer + Citations
```

This architecture transforms the platform from:

```text
"Ask an AI model"
```

into:

```text
"Ask questions over YOUR uploaded study materials"
```

---

## Why pgvector?

We chose **pgvector** because:

- integrates directly with PostgreSQL
- avoids maintaining a separate vector database
- production-friendly
- efficient similarity search
- simple deployment with Docker

This allows us to store document embeddings and perform semantic retrieval efficiently.

---

## Conclusion

Using semantic search + pgvector is not unnecessary complexity.

It solves real engineering problems:

- scalable document understanding
- faster inference
- lower cost
- better answer quality
- multi-document support
- semantic retrieval

This makes the platform suitable for real-world document question answering instead of simple prompt-based querying.
