from sqlalchemy.orm import Session
from sqlalchemy import text

from app.services.embeddings.embedding_service import (
    EmbeddingService
)


class SearchService:

    @staticmethod
    def semantic_search(
        db: Session,
        query: str,
        top_k: int = 5
    ):

        query_embedding = (
            EmbeddingService.generate_embedding(
                f"Represent this sentence for searching relevant passages: {query}"
            )
        )

        sql = text("""
            SELECT
                chunk_index,
                content,
                -(
                    embedding <#> CAST(
                        :query_embedding AS vector
                    )
                ) AS score
            FROM document_chunks
            ORDER BY embedding <#> CAST(
                :query_embedding AS vector
            )
            LIMIT :top_k
        """)

        results = db.execute(
            sql,
            {
                "query_embedding": str(
                    query_embedding
                ),
                "top_k": top_k
            }
        ).fetchall()

        return [
            {
                "chunk_index": row.chunk_index,
                "score": float(row.score),
                "content": row.content
            }
            for row in results
        ]
    

#     What this does
# Embeds user query
# Uses pgvector similarity:
# embedding <=> query_embedding

# Smaller distance = more similar.