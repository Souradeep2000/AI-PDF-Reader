class ChunkingService:

    @staticmethod
    def chunk_text(text: str):
        # Step 1: Split the text cleanly by major lines/paragraphs first
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        
        chunks = []
        current_chunk = ""
        chunk_idx = 0
        
        for paragraph in paragraphs:
            # Group rows together logically into chunks up to ~600 characters
            if len(current_chunk) + len(paragraph) < 600:
                current_chunk += paragraph + "\n"
            else:
                if current_chunk:
                    chunks.append({
                        "chunk_index": chunk_idx,
                        "content": current_chunk.strip()
                    })
                    chunk_idx += 1
                current_chunk = paragraph + "\n"
                
        # Catch remaining text trailing block
        if current_chunk:
            chunks.append({
                "chunk_index": chunk_idx,
                "content": current_chunk.strip()
            })
            
        return chunks