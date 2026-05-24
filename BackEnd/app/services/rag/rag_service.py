import json
from sqlalchemy.orm import Session
from app.services.rag.search_service import SearchService
from app.services.llm.llm_service import LLMService

class RAGService:

    # Cleaned up prompt: No hidden trap rules that make the LLM panic
    SYSTEM_PROMPT_TEMPLATE = """You are an AI study assistant.

You must answer the user's question using ONLY the facts and info mentioned in the provided context below.

INSTRUCTIONS:
1. Rely only on clear facts directly mentioned in the context.
2. Do not use outside knowledge or make ungrounded assumptions.
3. You are explicitly encouraged to compare, synthesize, summarize, and paraphrase details from the context to fully answer the query.
4. Keep the answer factual, direct, and concise.

Context:
----------------
{context}
----------------

Question:
{query}

Answer:
"""

    @staticmethod
    def ask(db: Session, query: str, top_k: int = 5):
        chunks = SearchService.semantic_search(db, query, top_k)
        relevant_chunks = [c for c in chunks if c["score"] >= 0.55]

        #  If vector database finds nothing, handle it here safely
        if not relevant_chunks:
            return {
                "answer": "I don't know based on the uploaded document.",
                "sources": []
            }

        context = "\n\n".join([f"Source {i+1}:\n{c['content']}" for i, c in enumerate(relevant_chunks)])
        prompt = RAGService.SYSTEM_PROMPT_TEMPLATE.format(context=context, query=query)

        answer = LLMService.generate(prompt)
        return {
            "answer": answer,
            "sources": relevant_chunks
        }

    @staticmethod
    def stream_ask(db: Session, query: str, top_k: int = 5):
        chunks = SearchService.semantic_search(db, query, top_k)
        relevant_chunks = [c for c in chunks if c["score"] >= 0.55]

        #  Handles empty contexts cleanly before hitting the stream loop
        if not relevant_chunks:
            yield {
                "event": "done",
                "data": json.dumps({
                    "answer": "I don't know based on the uploaded document.",
                    "sources": []
                })
            }
            return

        context = "\n\n".join([f"Source {i+1}:\n{c['content']}" for i, c in enumerate(relevant_chunks)])
        prompt = RAGService.SYSTEM_PROMPT_TEMPLATE.format(context=context, query=query)

        full_answer = ""
        for token in LLMService.stream_generate(prompt):
            full_answer += token
            yield {
                "event": "token",
                "data": token
            }

        yield {
            "event": "done",
            "data": json.dumps({
                "answer": full_answer,
                "sources": relevant_chunks
            })
        }