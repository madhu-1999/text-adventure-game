import json
from typing import Any, Optional, Set, Type
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from server.db.models import WorldDB
from server.src.repository.story_repository import IStoryRepository
from server.src.repository.world_repository import IWorldRepository
from server.src.models.story import WorldDTO, get_target_world_schema, convert_world_db_to_world_dto

def convertToJson(obj: BaseModel, include_attributes: Optional[Set[str]] = None, exclude_attributes: Optional[Set[str]] = None):
        return obj.model_dump_json(include=include_attributes, exclude=exclude_attributes, indent=4)

class LLMService:
    def __init__(self, story_repository: IStoryRepository, world_repository: IWorldRepository) -> None:
        self.story_repository = story_repository
        self.world_repository = world_repository
        self.model = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0.7, max_retries=2)

    def create_world(self, tag: str, prompt: str) -> Optional[WorldDTO]:
        system_prompt = f"""
Your job is to help create interesting {tag} worlds that 
players would love to play in.
Instructions:
- Only generate in plain text without formatting.
- Use simple clear language without being flowery.
- You must stay below 3-5 sentences for each description.
"""
        world_prompt = f"""
Generate a creative description for a unique {tag} world based on this prompt: {prompt}"""
        
        # Get the target schema
        target_schema: Type[WorldDTO] = get_target_world_schema(tag)
        #Define output schema
        llm = self.model.with_structured_output(target_schema)

        # Define prompt
        final_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", world_prompt)
        ])

        chain = final_prompt | llm
        response = chain.invoke({"topic": "fictional worlds"})
        if isinstance(response, WorldDTO):
            world: WorldDB = WorldDB(world=convertToJson(response, exclude_attributes={"id"}))
            world = self.world_repository.create_world(world=world)
            if world:
                return convert_world_db_to_world_dto(world, target_schema)
        return None
        
