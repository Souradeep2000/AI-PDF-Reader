from fastapi import APIRouter
from app.api.endpoints import (
    upload,
    test_embedding,
    search,
    ask
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

api_router.include_router(
    search.router,
    prefix="/api",
    tags=["Search"]
)

api_router.include_router(
    ask.router,
    prefix="/api",
    tags=["ask"]
)