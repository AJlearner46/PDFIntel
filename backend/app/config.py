from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

# MongoDB configuration with default fallback
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
CHROMA_DIR = os.getenv("CHROMA_DIR")
HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize MongoDB client with server selection timeout
client = AsyncIOMotorClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,  # 5 seconds timeout for faster failure detection
    connectTimeoutMS=5000
)
db = client["ragapp"]
