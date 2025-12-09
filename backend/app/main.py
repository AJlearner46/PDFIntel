from fastapi import FastAPI
from app.api.health import router as health_router

app = FastAPI(
    title="PDF Intel App Backend",
    description="Backend for local RAG system using Chroma, HF, Gemini",
    version="0.0.1"
)

app.include_router(health_router, prefix="/api")
