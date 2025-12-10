from fastapi import APIRouter, Depends, status, HTTPException

from server.src.dependencies import get_chat_service, get_current_user
from server.src.models.chat import ChatMessage, ChatSession
from server.src.models.user import UserResponseDTO
from server.src.service.chat_service import ChatService


chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.post("/create", summary="User Registration", response_model=ChatMessage, status_code=status.HTTP_201_CREATED)
async def create_chat(create_data: ChatSession, user: UserResponseDTO = Depends(get_current_user), chat_service: ChatService = Depends(get_chat_service)):
    try:
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user or password"
            )
        if user.id and user.id == create_data.user_id:
            return await chat_service.start_session(create_data.story_id, create_data.user_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        ) 