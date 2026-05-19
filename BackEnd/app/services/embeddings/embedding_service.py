from sentence_transformers import SentenceTransformer


class EmbeddingService:

    model = SentenceTransformer(
        "BAAI/bge-small-en-v1.5"
    )

    @staticmethod
    def generate_embedding(text: str):
        embedding = (
            EmbeddingService.model.encode(
                text,
                normalize_embeddings=True
            )
        )

        return embedding.tolist()

    @staticmethod
    def generate_embeddings(chunks: list[str]):
        embeddings = (
            EmbeddingService.model.encode(
                chunks,
                normalize_embeddings=True
            )
        )

        return embeddings.tolist()