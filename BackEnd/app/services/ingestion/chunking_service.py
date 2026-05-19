from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class ChunkingService:

    @staticmethod
    def chunk_text(text: str):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            length_function=len
        )

        chunks = splitter.create_documents([text])

        return [
            {
                "chunk_index": idx,
                "content": chunk.page_content
            }
            for idx, chunk in enumerate(chunks)
        ]