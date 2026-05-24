from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.db.session import init_db
from app.db.base import Base
from app.db.session import engine



Base.metadata.create_all(bind=engine)

app = FastAPI()

app = FastAPI(
    title="AI Study Platform API",
    version="1.0.0"
)

from app.core.config import ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(api_router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def health_check():
    return {
        "message": "Backend is running 🚀"
    }