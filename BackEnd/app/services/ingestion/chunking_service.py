from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class ChunkingService:

    @staticmethod
    def chunk_text(text: str):
        splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=150,
                length_function=len
            )
        )

        chunks = splitter.split_text(text)

        return chunks