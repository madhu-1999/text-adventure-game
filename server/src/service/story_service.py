from typing import Optional
import uuid

from fastapi import HTTPException, status
from server.src.models.story import CreateStoryDTO, StorySettingsDTO, TagDTO, TagsResponseDTO, WorldDTO
from server.src.repository.story_repository import IStoryRepository
from server.db.models import UserStoryDB
from server.src.exceptions import LLMResponseException
from server.src.service.llm_service import LLMService

def convert_user_story_to_story_settings(user_story: UserStoryDB, world: WorldDTO) -> StorySettingsDTO:
    return StorySettingsDTO(id=user_story.id, user_id=user_story.user_id, title=user_story.title, tag_id=user_story.tag_id, world=world, is_setup=user_story.is_setup) # type: ignore

class StoryService:
    def __init__(self, repository: IStoryRepository, llm_service: LLMService) -> None:
        self.repository = repository
        self.llm_service = llm_service

    async def get_tags(self) -> Optional[TagsResponseDTO]:
        """ Fetch all story tags

        Raises:
            Exception: If any error occurs

        Returns:
            Optional[TagsResponseDTO]: List of tag objects
        """
        try:
            tags = self.repository.get_tags()
            if tags:
                response_tags = [TagDTO.model_validate(tag) for tag in tags]
                return TagsResponseDTO(tags=response_tags)
            return None
        except Exception as e:
            raise e
    
    async def create_story(self, create_story: CreateStoryDTO, user_id: int) -> StorySettingsDTO:
        try:
            tag = self.repository.get_tag_by_id(create_story.tag_id)
            if tag:
                world: Optional[WorldDTO] = self.llm_service.create_world(tag=tag.tag, prompt=create_story.prompt) # type: ignore
                if not world:
                    raise LLMResponseException("Could not generate world!")
                title: str = f'world.name#{uuid.uuid4()}'
                user_story: UserStoryDB = UserStoryDB(user_id=user_id, title=title
                                        ,tag_id=create_story.tag_id, prompt=create_story.prompt, world_id=world.id)

                user_story = self.repository.add_story(user_story)
                if user_story:
                    return convert_user_story_to_story_settings(user_story, world)
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot create story")
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tag found")
        except Exception as e:
            raise e