from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.services.query_service import retrieve_context

chat_router = APIRouter()

# @chat_router.get("/protected")
# def protected_route(user_id: str = Depends(get_current_user)):
#     return {"message": "Access granted", "user_id": user_id}

@chat_router.post("/search")
async def search_context(
    chat_id: str,
    question: str,
    user_id: str = Depends(get_current_user)
):
    context = retrieve_context(question, chat_id)
    return {"context": context}