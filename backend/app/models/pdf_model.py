from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PDFDocument(BaseModel):
    user_id: str
    chat_id: str
    filename: str
    total_chunks: int
    uploaded_at: datetime
