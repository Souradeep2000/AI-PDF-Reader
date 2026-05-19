from fastapi import APIRouter
from app.api.endpoints import (
    upload,
    test_embedding
)

api_router = APIRouter()

api_router.include_router(
    test_embedding.router,
    prefix="/api",
    tags=["Embedding"]
)

api_router.include_router(
    upload.router,
    prefix="/api",
    tags=["Upload"]
)