from pydantic import BaseModel

class PDFDocument(BaseModel):
    user_id: str
    doc_id: str
    filename: str
    original_text: str
    chunks: list
