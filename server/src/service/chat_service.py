from typing import Any, Dict, List, Optional
from fastapi import BackgroundTasks, HTTPException, status
from server.db.models import ChatMessageDB
from server.db.vector_store import VectorStore
from server.src.models.chat import ChatMessage, ChatSession
from server.src.models.story import StorySettingsDTO, process_story
from server.src.repository.chat_repository import IChatRespository
from server.src.repository.story_repository import IStoryRepository
from server.src.service.llm_service import LLMService
from server.src.models.enums import Config

def _convert_chat_message_to_db_object(user_msg: ChatMessage) -> ChatMessageDB:
    return ChatMessageDB(story_id=user_msg.story_id, user_id=user_msg.user_id, session_id=user_msg.session_id, role=user_msg.role, content=user_msg.content)

def _construct_chat_message(llm_response_content: str, story_id: int, user_id: int, session_id: int) -> ChatMessageDB:
    return ChatMessageDB(story_id=story_id, user_id=user_id, session_id=session_id, role='ai', content=llm_response_content)

class ChatService:
    def __init__(self, story_repository: IStoryRepository, chat_repository: IChatRespository, llm_service: LLMService, vector_store: VectorStore) -> None:
        self._story_repository = story_repository
        self._chat_repository = chat_repository
        self._llm_service = llm_service
        self._vector_store = vector_store

    def _create_session(self, story_id: int, user_id: int) -> ChatSession:
        try:
            return self._chat_repository.create_session(story_id=story_id, user_id=user_id)
        except Exception as e:
            raise e
        
    async def get_session(self, session_id: int) -> Optional[ChatSession]:
        try:
            return self._chat_repository.get_session(session_id=session_id)
        except Exception as e:
            raise e
    async def start_session(self, story_id: int, user_id: int) -> Optional[ChatMessage]:
        try:
            # Create session
            chat_session: ChatSession = self._create_session(story_id, user_id)

            # Get story
            story: Optional[StorySettingsDTO] = self._story_repository.get_story(chat_session.story_id)

            if story and chat_session.id:
                world: dict[str, Any] = process_story(story)
                
                # Get llm response
                llm_response_content : str = self._llm_service.start_chat(world)
                if len(llm_response_content) > 0:
                    llm_response = _construct_chat_message(llm_response_content, story_id=chat_session.story_id, user_id=chat_session.user_id, session_id=chat_session.id)
                    
                    # Save llm chat message
                    saved_msg =  self._chat_repository.save_message(llm_response)

                    # Update has_started flag for chat session
                    self._chat_repository.update_has_started_for_chat_session(chat_session.id)
                    return saved_msg
                else:
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="LLM response in incorrect format!")
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Story not found!")
        except Exception as e:
            raise e
    async def _embed_messages(self, session_id: int, limit: int, skip: int):
        messages: List[ChatMessage] = self._chat_repository.get_messages(session_id=session_id, limit=limit, skip=skip, order_desc=False)
        if len(messages) > 0:
            for message in messages:
                self._vector_store.add_chat_message(message_id=str(message.id), story_id=str(message.story_id), content=message.content, role=message.role, session_id=str(message.session_id))

    async def send_message(self, user_msg: ChatMessage, background_tasks: BackgroundTasks):
        """Chat loop with RAG context"""
        try:
            # Save user message to db and vector store
            self._chat_repository.save_message(_convert_chat_message_to_db_object(user_msg))
            message_count: int = self._chat_repository.get_message_count(session_id=user_msg.session_id)

            # For every 50 messages, embed older messages in vector_store asynchronously
            if message_count % Config.MEMORY_THRESHOLD == 0:
                background_tasks.add_task(self._embed_messages, session_id=user_msg.session_id, limit=Config.MEMORY_THRESHOLD, skip=message_count-Config.MEMORY_THRESHOLD)
            
            # Retrieve RAG context
            context: Dict[str, Any] = self._vector_store.retrieve_context(story_id=str(user_msg.story_id), session_id=str(user_msg.session_id), query=user_msg.content)

            # Get chat history for context
            messages = self._chat_repository.get_messages(user_msg.session_id, limit=Config.CHAT_HISTORY_SIZE, skip=0, order_desc=True)

            # Get response from LLM
            llm_response_content = self._llm_service.send_message(context, messages, user_msg)
            llm_response = _construct_chat_message(llm_response_content, story_id=user_msg.story_id, user_id=user_msg.user_id, session_id=user_msg.session_id)
            
            # Save llm chat message
            saved_llm_response = self._chat_repository.save_message(llm_response)
            return saved_llm_response
        except Exception as e:
            raise e