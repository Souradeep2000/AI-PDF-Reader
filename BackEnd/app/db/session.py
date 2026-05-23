from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

# Import models so SQLAlchemy registers them
from app.db.models.document import Document
from app.db.models.document_chunk import DocumentChunk

from app.core.config import DATABASE_URL


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():

    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#         main.py
#    → startup()
#       → init_db()
#           → imports models
#           → create extension vector
#           → create tables