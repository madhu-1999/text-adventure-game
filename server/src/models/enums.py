from enum import StrEnum

class Tags(StrEnum):
    FANTASY = "Fantasy"
    ROMANCE = "Romance"
    MYSTERY = "Mystery"

class LocationPrompt(StrEnum):
    FANTASY = """
Create 3 different locations for a fantasy world.
For each location generate a description based on the world it's in. \
Describe important leaders, cultures, history of the location.\
If location is down in heirarchy like city ensure respective country/state is also generated.
for a location high in the hierarchy you may generate between 1-3 additional lower hierarchy locations
world data: {world_data}
"""
    MYSTERY = """Create 3 different locations for a mystery world.
For each location generate a description based on the world it's in. \
For each location generate a list of clues/evidence left by the either the criminal or another suspect
world data: {world_data}"""

class CharacterPrompt(StrEnum):
    FANTASY = """
Create 9 different characters for a fantasy world including the protagonist, based on the world they're in.
For each character, describe their personality, desires, major conflicts and any abilities they have, based on 
the power systems of the world they're in.
You may associate the character (except protagonist) with one or more locations in the world they're in.
world_data: {world_data}
locations_data:{locations_data}
"""
    ROMANCE = """
Create 9 different characters for a romance world including the protagonist, based on the world they're in.
For each character, describe their personality, desires, major conflicts.
For the love interests, briefly mention their dating/marriage history (if any)
world_data: {world_data}
"""
    MYSTERY = """Create 9 different characters for a mystery world including the protagonist and criminal.
For each character, describe their personality, desires, major conflicts, potential motive and plausible alibi.
You may associate the character with one or more locations in the world they're in.
For the criminal, ensure that events leading up to discovery of the crime and the other character's alibis and 
testimonies are consistent with how the criminal committed the crime.
world data: {world_data}
locations_data:{locations_data}
"""

class ChatPrompt:
    INITIAL_SYSTEM_PROMPT = """
You are an AI Game master. Your job is to write what 
happens next in a player's adventure game.

=== World context ===
world_info {world_info}
locations {locations}
characters {characters}
protagonist {protagonist}

===Your task for this first message===
Create an engaging introduction that:
1. Briefly describe the world (description, power systems, societal norms, events)
2. Describe the protagonist (name, appearance, motives) in second person present tense. Ex. (You are...)
3. Present a initial hook: where the protagonist is, the current situation and end 
with a question or prompt for action

Instructions: 
1. Keep the message under 150 words 
3. Use ONLY the world context provided above
"""

class Config:
    MEMORY_THRESHOLD = 50
    CHAT_HISTORY_SIZE = 10