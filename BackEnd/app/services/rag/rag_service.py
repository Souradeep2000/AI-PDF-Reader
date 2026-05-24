from sqlalchemy.orm import Session
from app.services.rag.search_service import SearchService
from BackEnd.app.services.llm.llm_service import LLMService


class RAGService:

    @staticmethod
    def ask(db: Session, query: str, top_k: int = 5):

        # 1. Retrieve relevant chunks
        chunks = SearchService.semantic_search(db, query, top_k)

        if not chunks:
            return {
                "answer": "I couldn't find relevant information in your documents.",
                "sources": []
            }

        # 2. Build context
        context = "\n\n".join(
            [f"[Source {i+1}]\n{c['content']}" for i, c in enumerate(chunks)]
        )

        # 3. Prompt
        prompt = f"""
You are a helpful AI assistant. Use only the context below to answer.

Context:
{context}

Question:
{query}

Rules:
- If answer is not in context, say you don't know.
- Be precise and concise.
- Always base answer on sources.
"""

        # 4. Call LLM
        answer = LLMService.generate(prompt)

        return {
            "answer": answer,
            "sources": chunks
        }