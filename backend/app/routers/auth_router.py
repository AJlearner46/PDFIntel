from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from app.models.user_model import UserCreate
from app.utils.auth import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.config import db

auth_router = APIRouter()

users_collection = db["users"]


async def check_mongodb_connection():
    """Helper function to check MongoDB connection and raise appropriate error"""
    try:
        await db.client.admin.command("ping")
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "MongoDB connection failed",
                "message": "Cannot connect to MongoDB. Please ensure MongoDB is running.",
                "hint": "Start MongoDB service or check your MONGO_URI in .env file"
            }
        ) from e


@auth_router.post("/register")
async def register(user: UserCreate):
    await check_mongodb_connection()
    
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    new_user = {
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "created_at": datetime.utcnow()
    }

    await users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}


@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    await check_mongodb_connection()
    
    db_user = await users_collection.find_one({"email": form_data.username})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(form_data.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(str(db_user["_id"]))
    return {
        "access_token": token,
        "token_type": "bearer"
    }
