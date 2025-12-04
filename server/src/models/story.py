from typing import List, Optional
from pydantic import BaseModel, Field

class TagDTO(BaseModel):
    id: Optional[int]
    tag: str

    class Config:
        from_attributes = True

class TagsResponseDTO(BaseModel):
    tags: List[TagDTO]
    
class CreateStoryDTO(BaseModel):
    tag_id: int
    prompt: str

class WorldDTO(BaseModel):
    id: int = Field(description="A unique integer identifier for the world")
    name: str = Field(description="Name of the fictional world")
    description: str = Field(description="A brief description of the world")

class StorySettingsDTO(BaseModel):
    id: int
    user_id: int
    title: str
    tag_id: int
    world : WorldDTO
    is_setup: bool