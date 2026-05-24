from pydantic import BaseModel

class AskRequest(BaseModel):
    query: str
    top_k: int = 5
    document_id: int | None = None

class AskResponse(BaseModel):
    answer: str
    sources: list[dict]