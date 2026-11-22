from pydantic import BaseModel
from typing import List, Optional

class DataItem(BaseModel):
    date: str          # 예: "2026-11-22"
    value: float       # 예: 120
    memo: str = ""     # 예: "FastAPI 공부"

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ConversationCreate(BaseModel):
    title: str
    messages: List[dict]
