from abc import ABC, abstractmethod
from typing import List, Optional

from server.db.models import ChatMessageDB
from server.src.models.chat import ChatMessage, ChatSession


class IChatRespository(ABC):
    @abstractmethod
    def create_session(self, story_id: int, user_id: int) -> ChatSession:
        pass

    @abstractmethod
    def get_session(self, session_id: int) -> Optional[ChatSession]:
        pass

    @abstractmethod
    def save_message(self, message: ChatMessageDB) -> Optional[ChatMessage]:
        pass 

    @abstractmethod
    def get_messages(self, session_id: int, limit: int, skip: int, order_desc: bool) -> List[ChatMessage]:
        pass

    @abstractmethod
    def get_message_count(self, session_id: int) -> int:
        pass
    
    @abstractmethod
    def update_has_started_for_chat_session(self, session_id: int):
        pass