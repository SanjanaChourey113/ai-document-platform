from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
import datetime

class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    filepath = Column(String)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("uploaded_documents.id"))
    chunk_text = Column(String)
    
class AISummary(Base):
    __tablename__ = "ai_summaries"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("uploaded_documents.id"))
    summary_text = Column(String)


class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("uploaded_documents.id"))
    metadata_text = Column(String)
    
    
class EmbeddingStore(Base):
    __tablename__ = "embedding_store"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("uploaded_documents.id"))
    chunk_text = Column(String)
    embedding = Column(String) 