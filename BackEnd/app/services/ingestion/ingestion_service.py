from sqlalchemy.orm import Session

from app.db.models.document import Document
from app.db.models.document_chunk import (
    DocumentChunk
)
from app.services.embeddings.embedding_service import (
    EmbeddingService
)
from app.services.llm.llm_service import (
    LLMService
)


class IngestionService:

    @staticmethod
    def save_document_chunks(
        db: Session,
        filename: str,
        original_filename: str,
        file_type: str,
        chunks: list
    ):

        # Create document entry
        document = Document(
            filename=filename,
            original_filename=original_filename,
            file_type=file_type
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        chunk_objects = []

        for chunk in chunks:

            chunk_purpose = LLMService.generate(f"Describe what section of a document this text represents in 10 words: {chunk['content']}")
            
            # Combine the purpose with the raw content for a highly resilient embedding vector
             
            embedding_text = f"This section covers: {chunk_purpose}. Data: {chunk['content']}"

            embedding = (
                EmbeddingService.generate_embedding(
                    embedding_text
                )
            )

            chunk_obj = DocumentChunk(
                document_id=document.id,
                chunk_index=chunk["chunk_index"],
                content=chunk["content"],
                embedding=embedding
            )

            chunk_objects.append(
                chunk_obj
            )

        db.add_all(
            chunk_objects
        )

        db.commit()

        return {
            "document_id": document.id,
            "chunks_saved": len(
                chunk_objects
            )
        }