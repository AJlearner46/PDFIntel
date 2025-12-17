from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers.auth_router import auth_router
from app.routers.pdf_router import pdf_router
from app.routers.chat_router import chat_router
from app.config import client, MONGO_URI
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="PDF Intel App Backend",
    description="Backend for local RAG system using Chroma, HF, Gemini",
    version="0.0.1"
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(pdf_router, prefix="/pdf", tags=["PDF"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])


@app.on_event("startup")
async def startup_event():
    """Verify MongoDB connection on startup"""
    try:
        # Ping the database to check connection
        await client.admin.command("ping")
        logger.info(f"✓ Successfully connected to MongoDB at {MONGO_URI}")
    except Exception as e:
        logger.error(f"✗ Failed to connect to MongoDB at {MONGO_URI}")
        logger.error(f"Error: {str(e)}")
        logger.error(
            "\nTo fix this:\n"
            "1. Make sure MongoDB is running (check with: Get-Service MongoDB)\n"
            "2. Start MongoDB service: Start-Service MongoDB\n"
            "3. Or set MONGO_URI in .env file to your MongoDB connection string\n"
            "4. For cloud MongoDB: Use MongoDB Atlas connection string"
        )


@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    client.close()
    logger.info("MongoDB connection closed")


@app.get("/")
def root():
    return {"message": "RAG Backend Running!"}


@app.get("/health")
async def health_check():
    """Health check endpoint that verifies MongoDB connection"""
    try:
        await client.admin.command("ping")
        return {
            "status": "healthy",
            "mongodb": "connected",
            "mongodb_uri": MONGO_URI
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "mongodb": "disconnected",
                "error": str(e),
                "mongodb_uri": MONGO_URI
            }
        )
