import os
from uuid import uuid4
from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from app.services.ingestion.text_extractor import TextExtractor
from app.services.ingestion.text_cleaner import TextCleaner
from app.services.ingestion.chunking_service import ChunkingService


router = APIRouter()

UPLOAD_DIR = "uploads"

ALLOWED_TYPES = {
    "application/pdf",

    "image/png",
    "image/jpeg",

    "text/plain",

    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".txt",
    ".docx"
}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if (
        file.content_type not in ALLOWED_TYPES
        or extension not in ALLOWED_EXTENSIONS
    ):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    unique_filename = (
        f"{uuid4()}_{file.filename}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        # 1. Extract text
        extracted_text = (
            TextExtractor.extract_text(
                file_path
            )
        )

        # 2. Clean text
        cleaned_text = (
            TextCleaner.clean(
                extracted_text
            )
        )

        # 3. Chunk text
        chunks = (
            ChunkingService.chunk_text(
                cleaned_text
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

    return {
        "message": "File uploaded successfully",
        "filename": unique_filename,
        "file_type": extension,
        "characters_extracted": len(
            cleaned_text
        ),
        "total_chunks": len(chunks),
        "preview_chunk": (
            chunks[0]["content"][:300]
            if chunks else ""
        )
    }