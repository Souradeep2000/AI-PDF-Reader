from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.search import (
    SearchRequest
)
from app.services.rag.search_service import (
    SearchService
)

router = APIRouter()


@router.post("/search")
def semantic_search(
    request: SearchRequest,
    db: Session = Depends(get_db)
):

    results = (
        SearchService.semantic_search(
            db=db,
            query=request.query,
            top_k=request.top_k
        )
    )

    return {
        "query": request.query,
        "matches": results
    }