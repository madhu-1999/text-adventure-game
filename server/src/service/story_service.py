from importlib import metadata
from typing import Optional, Set
import uuid

from fastapi import HTTPException, status
from pydantic import BaseModel
from server.db.vector_store import VectorStore
from server.src.models.story import CreateStoryDTO, StorySettingsDTO, TagDTO, TagsResponseDTO, WorldDTO
from server.src.repository.story_repository import IStoryRepository
from server.db.models import UserStoryDB, WorldDB
from server.src.exceptions import LLMResponseException
from server.src.repository.world_repository import IWorldRepository
from server.src.service.llm_service import LLMService

def convert_user_story_to_story_settings(user_story: UserStoryDB, world: WorldDTO) -> StorySettingsDTO:
    return StorySettingsDTO(id=user_story.id, user_id=user_story.user_id, title=user_story.title, tag_id=user_story.tag_id, world=world) # type: ignore

def convertToJson(obj: BaseModel, include_attributes: Optional[Set[str]] = None, exclude_attributes: Optional[Set[str]] = None):
        return obj.model_dump_json(include=include_attributes, exclude=exclude_attributes, indent=4)

class StoryService:
    def __init__(self, repository: IStoryRepository, world_repository: IWorldRepository, llm_service: LLMService, vector_store: VectorStore) -> None:
        self.story_repository = repository
        self.world_repository = world_repository
        self._llm_service = llm_service
        self._vector_store = vector_store

    async def get_tags(self) -> Optional[TagsResponseDTO]:
        """ Fetch all story tags

        Raises:
            Exception: If any error occurs

        Returns:
            Optional[TagsResponseDTO]: List of tag objects
        """
        try:
            tags = self.story_repository.get_tags()
            if tags:
                response_tags = [TagDTO.model_validate(tag) for tag in tags]
                return TagsResponseDTO(tags=response_tags)
            return None
        except Exception as e:
            raise e
    
    async def create_story(self, create_story: CreateStoryDTO, user_id: int) -> StorySettingsDTO:
        """
        Creates a new user story by generating a fictional world using an LLM,
        saving the world and story settings to the database, and returning the configuration.

        Args:
            create_story (CreateStoryDTO): Data transfer object containing tag_id and prompt.
            user_id (int): The ID of the user creating the story.

        Returns:
            StorySettingsDTO: The newly created story's settings, including world details.

        Raises:
            HTTPException: If the tag is not found or the story/world cannot be saved.
            LLMResponseException: If the LLM fails to generate the world data.
            Exception: Propagates other unexpected exceptions.
        """
        try:
            tag = self.story_repository.get_tag_by_id(create_story.tag_id)
            if tag:
                # Fenerate world data based on the tag and user prompt
                world: Optional[WorldDTO] = self._llm_service.create_world(tag=tag.tag, prompt=create_story.prompt) # type: ignore
                if not world:
                    raise LLMResponseException("Could not generate world!")
                world_to_save: WorldDB = WorldDB(world=convertToJson(world, exclude_attributes={"id"}))
                
                title: str = f'world.name#{uuid.uuid4()}'
                user_story: UserStoryDB = UserStoryDB(user_id=user_id, title=title
                                        ,tag_id=create_story.tag_id, prompt=create_story.prompt, world_id=-1)

                (user_story, saved_world) = self.story_repository.add_story_and_world(user_story, world_to_save)
                if user_story and saved_world:
                    world.id = saved_world.id # type: ignore
                    story_settings: StorySettingsDTO = convert_user_story_to_story_settings(user_story, world)
                    story_settings_text = story_settings.model_dump_json(indent=2)
                    metadata = {"user_id": str(story_settings.user_id), "title": story_settings.title}
                    self._vector_store.add_story_settings(story_id=str(story_settings.id), text=story_settings_text, metadata=metadata)
                    return story_settings
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot create story")
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tag found")
        except Exception as e:
            raise e