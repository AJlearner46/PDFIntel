import os
import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends
from app.dependencies import get_current_user
from app.services.pdf_service import extract_text_from_pdf
from app.config import db

pdf_router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

pdf_collection = db["pdf_documents"]
chunk_collection = db["pdf_chunks"]

@pdf_router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    chat_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    chunks = extract_text_from_pdf(file_path)

    # Store chunks
    chunk_docs = []
    for idx, chunk in enumerate(chunks):
        chunk_docs.append({
            "user_id": user_id,
            "chat_id": chat_id,
            "chunk_index": idx,
            "content": chunk,
            "created_at": datetime.utcnow()
        })

    if chunk_docs:
        await chunk_collection.insert_many(chunk_docs)

    # Store metadata
    await pdf_collection.insert_one({
        "user_id": user_id,
        "chat_id": chat_id,
        "filename": file.filename,
        "total_chunks": len(chunks),
        "uploaded_at": datetime.utcnow()
    })

    return {
        "message": "PDF uploaded and processed successfully",
        "chat_id": chat_id,
        "chunks_created": len(chunks)
    }
