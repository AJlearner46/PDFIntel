from fastapi import FastAPI
from routers.auth_router import auth_router
from routers.pdf_router import pdf_router
from routers.chat_router import chat_router

app = FastAPI(
    title="PDF Intel App Backend",
    description="Backend for local RAG system using Chroma, HF, Gemini",
    version="0.0.1"
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(pdf_router, prefix="/pdf", tags=["PDF"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "RAG Backend Running!"}
