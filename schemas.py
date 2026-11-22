import re
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

class DataItem(BaseModel):
    date: str = Field(..., description="학습 날짜 (YYYY-MM-DD 형식)")
    value: int = Field(..., ge=0, le=1440, description="학습 시간 (0~1440분)")
    memo: str = Field(default="", max_length=200, description="학습 메모 (최대 200자)")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError("날짜는 YYYY-MM-DD 형식이어야 합니다.")
        return v

    @field_validator("memo")
    @classmethod
    def sanitize_memo(cls, v: str) -> str:
        return v.strip()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="사용자 질문 (1~1000자)")
    conversation_id: Optional[str] = Field(default=None, max_length=100)

    @field_validator("message")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("질문 내용은 공백일 수 없습니다.")
        return cleaned

class ConversationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    messages: List[dict] = Field(default_factory=list)