from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

chat_router = APIRouter()

@chat_router.get("/protected")
def protected_route(user_id: str = Depends(get_current_user)):
    return {"message": "Access granted", "user_id": user_id}
