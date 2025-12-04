import json
from typing import Any, List, Optional, Type, Union

from pydantic import BaseModel, Field

from server.db.models import WorldDB
from server.src.models.enums import Tags


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

class BaseWorldDTO(BaseModel):
    id: int = Field(description="A unique integer identifier for the world")
    name: str = Field(description="Name of the fictional world")
    description: str = Field(description="A brief description of the world")

class PowerSystem(BaseModel):
    name: str = Field(description="Name of power system")
    description: str = Field(description="Brief description of the power system")
    rules: List[str] = Field(description="List of 3 rules of the power system")
    limitations: List[str] = Field(description="List of 3 limitations of the power system")

class FantasyWorldDTO(BaseWorldDTO):
    power_systems: List[PowerSystem] = Field(description=" 3 different power systems that exist in this world")

class RomanceWorldDTO(BaseWorldDTO):
    time_period: str = Field(description="Time period in which story is set ex: 1950s, 1700s")
    location: str = Field(description="Location where story is set ex: Tokyo, London")
    tone: str = Field(description="One word identifier for tone ex: sweet/steamy/angsty/emotional")
    societal_norms: List[str] = Field(description="3 norms related to dating or society in the story setting")

class MysteryWorldDTO(BaseWorldDTO):
    type: str = Field(description="Mystery subgenre ex: noir/cozy/medical")
    time_period: str = Field(description="Time period in which story is set ex: 1950s, 1700s")
    location: str = Field(description="Location where story is set ex: Tokyo, London")
    role: str = Field(description="Role the human assumes ex:PI/detective/forensic scientist/lawyer")
    crime: str = Field(description="Type of crime ex: murder/embezzlement/fraud")

WorldDTO = Union[FantasyWorldDTO, RomanceWorldDTO, MysteryWorldDTO]

class StorySettingsDTO(BaseModel):
    id: int
    user_id: int
    title: str
    tag_id: int
    world : WorldDTO
    is_setup: bool

def get_target_world_schema(tag: str) -> Type[WorldDTO]:
    match tag:
        case Tags.FANTASY: 
            return FantasyWorldDTO
        case Tags.ROMANCE:
            return RomanceWorldDTO
        case Tags.MYSTERY:
            return MysteryWorldDTO
        case _:
            return FantasyWorldDTO
        
def convert_world_db_to_world_dto(world: WorldDB, target_schema: Type[WorldDTO]) -> WorldDTO:
    if isinstance(world.world, str):
        properties: dict[str, Any] = json.loads(world.world) # type: ignore
    else:
        properties: dict[str, Any] = world.world # type: ignore
    properties['id'] = world.id
    return target_schema.model_validate(properties)
