from fastapi import APIRouter, UploadFile

pdf_router = APIRouter()

@pdf_router.post("/upload")
async def upload_pdf(file: UploadFile):
    return {"msg": "upload PDF endpoint"}

@pdf_router.get("/list")
async def list_pdfs():
    return {"msg": "list PDFs endpoint"}
