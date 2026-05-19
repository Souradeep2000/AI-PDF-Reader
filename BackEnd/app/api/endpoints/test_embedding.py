from fastapi import APIRouter

from app.services.embeddings.embedding_service import (
    EmbeddingService
)

router = APIRouter()


@router.get("/test-embedding")
def test_embedding():

    text = (
        "Machine learning is a subset "
        "of artificial intelligence."
    )

    embedding = (
        EmbeddingService.generate_embedding(
            text
        )
    )

    return {
        "embedding_dimension": len(
            embedding
        ),
        "preview": embedding[:5]
    }