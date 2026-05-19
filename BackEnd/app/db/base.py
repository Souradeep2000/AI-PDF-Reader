from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models here
from app.db.models.document import Document
from app.db.models.document_chunk import DocumentChunk