from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, insert, select, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from server.db.models import ChatMessageDB, ChatSessionDB
from server.src.exceptions import DatabaseError
from server.src.models.chat import ChatMessage, ChatSession
from server.src.repository.chat_repository import IChatRespository


class ChatRepository(IChatRespository):
    def __init__(self, session: Session):
        self.session = session 

    def create_session(self, story_id: int, user_id: int) -> ChatSession:
        try:
            # Save session
            stmt = insert(ChatSessionDB).values(
                story_id=story_id,
                user_id=user_id
            ).returning(
                ChatSessionDB
            )

            saved_session = self.session.execute(stmt).first()
            if not saved_session:
                self.session.rollback()
                raise DatabaseError("Could not insert session!")
            session = ChatSession.model_validate(saved_session[0])
            self.session.commit()
            return session
        except IntegrityError as e:
            self.session.rollback()
            raise DatabaseError(f"Could not insert session: {str(e)}") from e
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to insert session: {str(e)}") from e
        
    def get_session(self, session_id: int) -> Optional[ChatSession]:
        session = self.session.query(ChatSessionDB).filter(ChatSessionDB.id == session_id).first()
        if session:
            return ChatSession.model_validate(session)
        return None
    
    def save_message(self, message: ChatMessageDB) -> Optional[ChatMessage]:
        try:
            stmt = insert(ChatMessageDB).values(
            story_id=message.story_id,
            user_id=message.user_id,
            session_id=message.session_id,
            role=message.role,
            content=message.content
            ).returning(
                ChatMessageDB
            )

            saved_message = self.session.execute(stmt).first()
            if not saved_message:
                self.session.rollback()
                raise DatabaseError("Could not insert session!")
            msg = ChatMessage.model_validate(saved_message[0])
            self.session.commit()
            return msg
        except IntegrityError as e:
            self.session.rollback()
            raise DatabaseError(f"Could not insert message: {str(e)}") from e
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to insert message: {str(e)}") from e
    
    def get_messages(self, session_id: int, limit: int, skip: int, order_desc: bool = False) -> List[ChatMessage]:
        if order_desc:
            messages = self.session.query(ChatMessageDB).filter(ChatMessageDB.session_id == session_id).order_by(ChatMessageDB.created_at.desc()).limit(limit).offset(skip).all()
        else: 
            messages = self.session.query(ChatMessageDB).filter(ChatMessageDB.session_id == session_id).order_by(ChatMessageDB.created_at).limit(limit).offset(skip).all()
        if messages:
            return [ChatMessage.model_validate(message) for message in messages]
        return []
    
    def get_message_count(self, session_id: int) -> int:
        stmt = select(func.count()).select_from(ChatMessageDB).where(ChatMessageDB.session_id == session_id)
        count = self.session.execute(stmt).scalar()
        if count:
            return count
        return 0
    
    def update_has_started_for_chat_session(self, session_id: int):
        stmt = update(ChatSessionDB).where(ChatSessionDB.id == session_id).values(
            has_started=True,
            updated_at=datetime.now(timezone.utc)
            )
        self.session.execute(stmt)
        self.session.commit()