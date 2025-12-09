from fastapi import APIRouter, Depends, HTTPException, status

from server.src.dependencies import get_current_user, get_story_service
from server.src.models.story import CreateStoryDTO, StorySettingsDTO, TagsResponseDTO


story_router = APIRouter(prefix="/story", tags=["story"])

@story_router.get(path="/tags", summary="Get available story tags", response_model=TagsResponseDTO)
async def get_tags(story_service = Depends(get_story_service)):
    try:
        tags = await story_service.get_tags()
        if tags is None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="No tags found"
            )
        return tags
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )
    
@story_router.post(path="/create", summary="Start a new story", response_model=StorySettingsDTO)
async def create_story_settings(create_story: CreateStoryDTO, user = Depends(get_current_user), story_service = Depends(get_story_service)):
    try:
        if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid user or password"
                )
        return await story_service.create_story(create_story, user.id)
    except HTTPException as e:
         raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )