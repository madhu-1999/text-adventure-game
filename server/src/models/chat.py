from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    id: Optional[int] = None
    story_id: int
    user_id: int
    session_id: int
    role: Literal['human', 'ai']
    content: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ChatSession(BaseModel):
    id: Optional[int] = None
    story_id: int
    user_id: int
    messages: List[ChatMessage] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
