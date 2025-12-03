from typing import Optional
from server.src.models.story import TagDTO, TagsResponseDTO
from server.src.repository.story_repository import IStoryRepository


class StoryService:
    def __init__(self, repository: IStoryRepository) -> None:
        self.repository = repository

    async def get_tags(self) -> Optional[TagsResponseDTO]:
        try:
            tags = self.repository.get_tags()
            if tags:
                response_tags = [TagDTO.model_validate(tag) for tag in tags]
                return TagsResponseDTO(tags=response_tags)
            return None
        except Exception as e:
            raise e