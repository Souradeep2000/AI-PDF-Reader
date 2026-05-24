from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ask import AskRequest, AskResponse
from app.services.rag.rag_service import RAGService

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest, db: Session = Depends(get_db)):

    result = RAGService.ask(db, req.query, req.top_k)

    return result