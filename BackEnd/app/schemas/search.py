from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

# Question
# → Convert to embedding
# → Compare with stored chunk embeddings
# → Return top-k relevant chunks

# example query
# {
#   "query": "What is BullMQ?",
#   "top_k": 5
# }