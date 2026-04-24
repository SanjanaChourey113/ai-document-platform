from fastapi import FastAPI, UploadFile, File , Query , Body
from sqlalchemy.orm import Session
import shutil, os
import json
import numpy as np

from models.document import EmbeddingStore
from app.database import engine, Base, SessionLocal
from models.document import UploadedDocument, DocumentChunk
from services.text_extractor import extract_text
from services.chunker import chunk_text
from services.ai_service import generate_summary, extract_metadata
from models.document import AISummary, DocumentMetadata  
from services.embedding_service import generate_embedding
from services.ai_service import generate_answer
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = "uploads"

# Create uploads folder if not exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.get("/")
def home():
    return {"message": "AI Document Platform Running"}


@app.get("/search")
def semantic_search(query: str = Query(...)):
    db: Session = SessionLocal()

    query_embedding = generate_embedding(query)

    results = db.query(EmbeddingStore).all()

    best_score = -1
    best_chunk = ""

    for r in results:
        stored_embedding = json.loads(r.embedding)

        score = np.dot(query_embedding, stored_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(stored_embedding)
        )

        if score > best_score:
            best_score = score
            best_chunk = r.chunk_text

    db.close()

    return {
        "query": query,
        "best_match": best_chunk,
        "score": best_score
    }


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    extracted_text = extract_text(file_path)

    # Chunk text
    chunks = chunk_text(extracted_text)

    db: Session = SessionLocal()

    try:
        # Save document
        new_doc = UploadedDocument(
            filename=file.filename,
            filepath=file_path
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

        # Save chunks
        for chunk in chunks:
            embedding = generate_embedding(chunk)

            db_chunk = DocumentChunk(
                document_id=new_doc.id,
                chunk_text=chunk
            )
            db.add(db_chunk)

            db_embedding = EmbeddingStore(
                document_id=new_doc.id,
                chunk_text=chunk,
                embedding=json.dumps(embedding)
            )
            db.add(db_embedding)

        #  AI Processing (limit text to avoid cost)
        limited_text = extracted_text[:2000]

        summary = generate_summary(limited_text)
        metadata = extract_metadata(limited_text)

        # Save AI results
        ai_summary = AISummary(
            document_id=new_doc.id,
            summary_text=summary
        )

        doc_metadata = DocumentMetadata(
        document_id=new_doc.id,
        metadata_text=json.dumps(metadata)
        )

        db.add(ai_summary)
        db.add(doc_metadata)
        db.commit()

        return {
            "message": "File uploaded and fully processed",
            "chunks_created": len(chunks),
            "summary_preview": summary[:200]
        }

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()
        


@app.post("/ask")
def ask_question(data: dict = Body(...)):
    question = data.get("question")

    db: Session = SessionLocal()

    # Step 1: Convert question to embedding
    query_embedding = generate_embedding(question)

    results = db.query(EmbeddingStore).all()

    best_score = -1
    best_chunk = ""

    # Step 2: Find best chunk (same as search)
    for r in results:
        stored_embedding = json.loads(r.embedding)

        score = np.dot(query_embedding, stored_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(stored_embedding)
        )

        if score > best_score:
            best_score = score
            best_chunk = r.chunk_text

    # Step 3: Generate answer using AI
    answer = generate_answer(best_chunk, question)

    db.close()

    return {
        "question": question,
        "context_used": best_chunk,
        "answer": answer,
        "score": best_score
    }
    


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dashboard")
def get_dashboard():
    db: Session = SessionLocal()

    total_docs = db.query(UploadedDocument).count()
    total_chunks = db.query(DocumentChunk).count()

    db.close()

    return {
        "total_documents": total_docs,
        "total_chunks": total_chunks
    }