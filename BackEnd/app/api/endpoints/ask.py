from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ask import AskRequest, AskResponse
from app.services.rag.rag_service import RAGService

from sse_starlette.sse import (
    EventSourceResponse
)

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest, db: Session = Depends(get_db)):

    result = RAGService.ask(db, req.query, req.top_k)

    return result

@router.post("/ask-stream")
async def ask_stream(
    request: AskRequest,
    db: Session = Depends(get_db)
):

    def event_generator():
        for event in (
            RAGService.stream_ask(
                db=db,
                query=request.query,
                top_k=request.top_k
            )
        ):
            yield event

    return EventSourceResponse(
        event_generator(),
        ping=30
    )