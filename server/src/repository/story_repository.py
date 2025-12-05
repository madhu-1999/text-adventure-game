from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from server.db.models import TagsDB, UserStoryDB, WorldDB


class IStoryRepository(ABC):
    @abstractmethod
    def get_tags(self) -> Optional[List[TagsDB]]:
        pass

    @abstractmethod
    def get_tag_by_id(self, id) -> Optional[TagsDB]:
        pass

    @abstractmethod
    def add_story_and_world(self, user_story: UserStoryDB, world: WorldDB) -> Tuple[UserStoryDB, WorldDB]:
        pass