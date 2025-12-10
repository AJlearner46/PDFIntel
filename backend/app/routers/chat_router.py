from fastapi import APIRouter

chat_router = APIRouter()

@chat_router.get("/history")
async def chat_history():
    return {"msg": "chat history endpoint"}

@chat_router.post("/ask")
async def ask_question():
    return {"msg": "ask question endpoint"}
