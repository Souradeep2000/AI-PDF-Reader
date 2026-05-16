from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints.upload import (
    router as upload_router
)

app = FastAPI(
    title="AI Study Platform API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(
    upload_router,
    prefix="/api",
    tags=["Upload"]
)


@app.get("/")
def health_check():
    return {
        "message": "Backend is running 🚀"
    }