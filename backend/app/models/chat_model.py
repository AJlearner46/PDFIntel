from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    sender: str  # "user" or "bot"
    text: str

class Chat(BaseModel):
    user_id: str
    chat_id: str
    messages: List[ChatMessage]
