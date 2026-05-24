import json

from sqlalchemy.orm import Session

from app.services.rag.search_service import (
    SearchService
)
from app.services.llm.llm_service import (
    LLMService
)


class RAGService:

    @staticmethod
    def ask(
        db: Session,
        query: str,
        top_k: int = 5
    ):

        # 1. Retrieve relevant chunks
        chunks = SearchService.semantic_search(
            db,
            query,
            top_k
        )

        # 2. Filter weak matches
        relevant_chunks = [
            chunk
            for chunk in chunks
            if chunk["score"] > 0.65
        ]

        if not relevant_chunks:
            return {
                "answer":
                "I couldn't find relevant information in your uploaded documents.",
                "sources": []
            }

        # 3. Build context
        context = "\n\n".join(
            [
                f"Source {i+1}:\n{c['content']}"
                for i, c in enumerate(
                    relevant_chunks
                )
            ]
        )

        # 4. Prompt
        prompt = f"""
You are an AI study assistant.

You MUST answer ONLY from the provided context.

Rules:
- Do NOT use outside knowledge.
- If the answer is not explicitly present in the context,
  say:
  "I don't know based on the uploaded document."
- Keep the answer concise.
- Cite concepts from retrieved content.

Context:
{context}

Question:
{query}

Answer:
"""

        # 5. Generate response
        answer = LLMService.generate(
            prompt
        )

        return {
            "answer": answer,
            "sources": relevant_chunks
        }
    

    @staticmethod
    def stream_ask(
        db: Session,
        query: str,
        top_k: int = 5
    ):

        # 1. Retrieve relevant chunks
        chunks = SearchService.semantic_search(
            db,
            query,
            top_k
        )

        # 2. Filter weak matches
        relevant_chunks = [
            chunk
            for chunk in chunks
            if chunk["score"] > 0.65
        ]

        if not relevant_chunks:

            yield {
                "event": "done",
                "data": json.dumps({
                    "answer":
                    "I couldn't find relevant information in your uploaded documents.",
                    "sources": []
                })
            }

            return

        # 3. Build context
        context = "\n\n".join(
            [
                f"Source {i+1}:\n{c['content']}"
                for i, c in enumerate(
                    relevant_chunks
                )
            ]
        )

        # 4. Prompt
        prompt = f"""
You are an AI study assistant.

You MUST answer ONLY from the provided context.

Rules:
- Do NOT use outside knowledge.
- If the answer is not explicitly present in the context,
  say:
  "I don't know based on the uploaded document."
- Keep the answer concise.
- Cite concepts from retrieved content.

Context:
{context}

Question:
{query}

Answer:
"""

        # 5. Stream response
        full_answer = ""

        for token in (
            LLMService.stream_generate(
                prompt
            )
        ):

            full_answer += token

            yield {
                "event": "token",
                "data": token
            }

        # 6. Final response
        yield {
            "event": "done",
            "data": json.dumps({
                "answer": full_answer,
                "sources":
                relevant_chunks
            })
        }