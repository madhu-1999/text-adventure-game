import json
from typing import Any, List, Optional, Set, Tuple, Type, Union, cast

from pydantic import BaseModel, Field, create_model

from server.db.models import WorldDB
from server.src.models.enums import CharacterPrompt, LocationPrompt, Tags


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

class BaseWorldSettingDTO(BaseModel):
    name: str = Field(description="Name of the fictional world")
    description: str = Field(description="A brief description of the world")

class Ability(BaseModel):
    name: str = Field(description="Name of the ability")
    description: str = Field(description="Brief description of what the ability does")
    cost: str = Field(description="What cost one must pay to use this ability ex: mana/hp/stamina")

class PowerSystem(BaseModel):
    name: str = Field(description="Name of power system")
    description: str = Field(description="Brief description of the power system")
    rules: List[str] = Field(description="List of 3 rules of the power system")
    limitations: List[str] = Field(description="List of 3 limitations of the power system")
    abilities: List[Ability] = Field(description="List of 3 abilities (low cost/medium cost/ high cost) belonging to the power system")

class FantasyWorldSettingDTO(BaseWorldSettingDTO):
    power_systems: List[PowerSystem] = Field(description=" 3 different power systems that exist in this world")

class RomanceWorldSettingDTO(BaseWorldSettingDTO):
    time_period: str = Field(description="Time period in which story is set ex: 1950s, 1700s")
    location: str = Field(description="Location where story is set ex: Tokyo, London")
    tone: str = Field(description="One word identifier for tone ex: sweet/steamy/angsty/emotional")
    societal_norms: List[str] = Field(description="3 norms related to dating or society in the story setting")

class MysteryWorldSettingDTO(BaseWorldSettingDTO):
    type: str = Field(description="Mystery subgenre ex: noir/cozy/medical")
    time_period: str = Field(description="Time period in which story is set ex: 1950s, 1700s")
    location: str = Field(description="Location where story is set ex: Tokyo, London")
    crime: str = Field(description="Type of crime ex: murder/embezzlement/fraud")
    events: str = Field(description="Brief description of events that lead up to the discovery of the crime.")

WorldSettingDTO = Union[FantasyWorldSettingDTO, RomanceWorldSettingDTO, MysteryWorldSettingDTO]

class LocationDTO(BaseModel):
    name: str = Field(description="Name of location, can be descriptive")
    description: str = Field(description="Brief description of the location")

class FantasyLocationDTO(LocationDTO):
    type: str = Field(description="Type of location ex: kingdom/town/city/country")
    government_type: str = Field(description="Type of government ex: monarchy/dictatorship/democracy/communism")

class MysteryLocationDTO(LocationDTO):
    type: str = Field(description="Type of location ex: crime scene/business/public space")
    clues: List[str] = Field(description="A list of physical clues or evidence found at the location")

Locations = Union[FantasyLocationDTO, MysteryLocationDTO]

class LocationsDTO(BaseModel):
    locations: List[Locations] = Field(description="List of locations relevant to the world")

class CharacterDTO(BaseModel):
    name: str = Field(description="Name of character")
    personality: str = Field(description="Brief description of character's personality") 
    backstory: str = Field(description="Brief description of a character's background/hopes/conflicts")
    age: str = Field(description="Character's age")
    appearance: str = Field(description="Brief description of the characters appearance ex:height, build, hair, eyes, style")
    occupation: str = Field(description="Character's occupation")
    race: str = Field(description="Race of character ex: human/orc/elf/alien")
    gender: str = Field(description="Gender of character ex: male/female")
    is_protagonist: bool = Field(description="True if this character is protagonist else False")

class FantasyCharacterDTO(CharacterDTO):
    role: str = Field(description="Role of the character in the story ex: protagonist/friend/mentor/villain")
    abilities: List[str] = Field(description="List of abilities the character has, can be a ability described in world data")


class RomanceCharacterDTO(CharacterDTO):
    role: str = Field(description="Role of the character in the story ex: protagonist/friend/family/love interest")
    is_love_interest: str = Field(description="True if character is a love interest else False")

class MysteryCharacterDTO(CharacterDTO):
    role: str = Field(description="Role of the character in the story ex: protagonist/friend/family/love interest")
    alibi: str = Field(description="Alibi the character provides at the time of the crime")
    motive: str = Field(description="The character's potential reason for committing the crime (e.g., 'financial debt', 'revenge', 'jealousy').")
    connection_to_victim: str = Field(description="How this character knew the victim.")
    secrets: List[str] = Field(description="1-2 hidden secrets the detective can uncover during investigation.")

Characters = Union[FantasyCharacterDTO, RomanceCharacterDTO, MysteryCharacterDTO]
class CharactersDTO(BaseModel):
    characters: List[Characters] = Field(description="List of characters relevant to the world")

class WorldDTO(BaseModel):
    id: int
    setting: WorldSettingDTO
    locations: Optional[LocationsDTO]
    characters: CharactersDTO

class StorySettingsDTO(BaseModel):
    id: int
    user_id: int
    title: str
    tag_id: int
    world : WorldDTO
    is_setup: bool

def get_target_character_schema(tag: str) -> Tuple[str, Type[CharactersDTO]]:
    """
    Generates a specific Pydantic Model at runtime
    """
    match tag:
        case Tags.FANTASY:
            dynamic_class = FantasyCharacterDTO
            prompt = CharacterPrompt.FANTASY
        case Tags.MYSTERY:
            dynamic_class = MysteryCharacterDTO
            prompt = CharacterPrompt.MYSTERY
        case Tags.ROMANCE:
            dynamic_class = RomanceCharacterDTO
            prompt = CharacterPrompt.ROMANCE
        case _:
            dynamic_class = FantasyCharacterDTO
            prompt = CharacterPrompt.FANTASY
    
    model = create_model(
        'CharactersDTO',
        characters=(List[dynamic_class], Field(description="List of characters relevant to the world"))
    )

    return (prompt, cast(Type[CharactersDTO], model))

def get_target_location_schema(tag: str) -> Optional[Tuple[str, Type[LocationsDTO]]]:
    """
    Generates a specific Pydantic Model at runtime
    """
    match tag:
        case Tags.FANTASY:
            dynamic_class = FantasyLocationDTO
            prompt = LocationPrompt.FANTASY
        case Tags.MYSTERY:
            dynamic_class = MysteryLocationDTO
            prompt = LocationPrompt.MYSTERY
        case Tags.ROMANCE:
            return None
        case _:
            dynamic_class = FantasyLocationDTO
            prompt = LocationPrompt.FANTASY
    
    model = create_model(
        'LocationsDTO',
        locations=(List[dynamic_class], Field(description="List of locations relevant to the world"))
    )

    return (prompt, cast(Type[LocationsDTO], model))
def get_target_world_schema(tag: str) -> Type[WorldSettingDTO]:
    match tag:
        case Tags.FANTASY: 
            return FantasyWorldSettingDTO
        case Tags.ROMANCE:
            return RomanceWorldSettingDTO
        case Tags.MYSTERY:
            return MysteryWorldSettingDTO
        case _:
            return FantasyWorldSettingDTO
        
def convertToJson(obj: BaseModel, include_attributes: Optional[Set[str]] = None, exclude_attributes: Optional[Set[str]] = None):
        return json.loads(obj.model_dump_json(include=include_attributes, exclude=exclude_attributes, indent=4))

def convert_to_world_dto(world_data: dict[str, Any]):
    locations = None
    if 'locations_data' in world_data:
        locations = convertToJson(world_data['locations_data'])
    characters = convertToJson(world_data['characters_data'])
    return WorldDTO(id=-1, setting=world_data['world_data'], locations=locations, characters=characters)
   
def convert_world_db_to_world_dto(world: WorldDB, target_schema: Type[WorldSettingDTO]) -> WorldSettingDTO:
    if isinstance(world.world, str):
        properties: dict[str, Any] = json.loads(world.world) # type: ignore
    else:
        properties: dict[str, Any] = world.world # type: ignore
    properties['id'] = world.id
    return target_schema.model_validate(properties)
