from typing import  Any, Optional, Type
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableBranch, RunnableLambda

from server.src.models.enums import ChatPrompt
from server.src.models.story import WorldDTO, WorldSettingDTO, convert_to_world_dto, get_target_character_schema, get_target_location_schema, get_target_world_schema


class LLMService:
    def __init__(self): 
        self.model = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0.7, max_retries=2)

    def create_world(self, tag: str, prompt: str) -> Optional[WorldDTO]:
        """
    Create a unique world setting with optional locations based on a given tag and prompt.
    
    This method uses a multi-stage LLM pipeline to generate world settings and optionally
    generate locations within that world. The world and location schemas are dynamically
    determined based on the provided tag.
    
    Args:
        tag: The category or type of world to create (e.g., "fantasy", "sci-fi").
             Used to determine the appropriate world and location schemas.
        prompt: A creative prompt describing the desired world characteristics.
                Used as input for the LLM to generate the world description.
    
    Returns:
        Optional[WorldDTO]: A data transfer object containing the generated world data
                           and any locations, or None if generation fails.
    
    Pipeline stages:
        1. Generate world setting data using the tag-specific schema
        2. Optionally generate locations if the tag supports location generation
    """

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
        
        # Get the target world setting schema
        target_schema: Type[WorldSettingDTO] = get_target_world_schema(tag)
        
        #Define output schema
        world_llm = self.model.with_structured_output(target_schema)

        # Define intial prompt
        initial_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", world_prompt)
        ])

        # Define chain to generate world setting data
        world_chain = initial_prompt | world_llm

        # Get target location schema and prompt
        output = get_target_location_schema(tag)
        location_chain = None
        if output:
            # if locations should be generated
            (location_prompt_template, target_location_schema) = output

            # Define output schema
            location_llm = self.model.with_structured_output(target_location_schema)

            # Define location prompt
            location_prompt = ChatPromptTemplate.from_messages([
                ('human', location_prompt_template)
            ])

            # Define chain to generate locations using world setting data
            location_chain = location_prompt | location_llm

        # Get target character schema and prompt
        (character_prompt_template, target_character_schema) = get_target_character_schema(tag)

        # Define output schema
        character_llm = self.model.with_structured_output(target_character_schema)

        # Define character prompt
        character_prompt = ChatPromptTemplate.from_messages([
            ('human', character_prompt_template)
        ])

        # Define chain to generate characters from world settings and locations
        character_chain = character_prompt | character_llm

        # Generate world setting data
        # This also makes world setting data available as input variable
        world_data_chain = RunnablePassthrough.assign(
            world_data=world_chain
        )

        def generate_locations_if_applicable(input: dict):
            if location_chain:
                locations_data = location_chain.invoke(input)
                input['locations_data'] = locations_data
                return input
            return input
        
        # Chain to optionally generate locations
        optional_location_data_chain = RunnableBranch(
            (lambda x: location_chain is not None, 
             RunnableLambda(generate_locations_if_applicable)
            ),
            RunnablePassthrough()
        )

        # Chain to generate characters
        character_data_chain = RunnablePassthrough.assign(
            characters_data=character_chain
        )
        # Final chain
        pipeline = (
            world_data_chain
            | optional_location_data_chain
            | character_data_chain
        )
            
        result_dict = pipeline.invoke({"topic": "fictional worlds"})
        return convert_to_world_dto(result_dict)
        
    def start_chat(self, world: dict[str, Any]) -> str:
        # Define intial prompt
        initial_prompt = ChatPromptTemplate.from_messages([
            ("system", ChatPrompt.INITIAL_SYSTEM_PROMPT),
            ("human",  "Generate introduction")
        ])

         # Define chain to generate intro message
        chat_intro_chain = initial_prompt | self.model

        result = chat_intro_chain.invoke(world)
        if isinstance(result.content, str):
            return result.content
        return ''