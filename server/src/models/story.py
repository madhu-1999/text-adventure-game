from typing import List, Optional
from pydantic import BaseModel

class TagDTO(BaseModel):
    id: Optional[int]
    tag: str

    class Config:
        from_attributes = True

class TagsResponseDTO(BaseModel):
    tags: List[TagDTO]
    