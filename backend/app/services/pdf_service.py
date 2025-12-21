from pypdf import PdfReader
from app.utils.text_splitter import split_text

def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)
    full_text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"

    return split_text(full_text)
