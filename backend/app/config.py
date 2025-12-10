from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
CHROMA_DIR = os.getenv("CHROMA_DIR")
HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = AsyncIOMotorClient(MONGO_URI)
db = client["ragapp"]
