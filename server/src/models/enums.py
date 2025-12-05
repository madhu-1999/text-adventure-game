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