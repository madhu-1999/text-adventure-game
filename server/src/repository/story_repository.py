from abc import ABC, abstractmethod
from typing import List, Optional

from server.db.models import TagsDB, UserStoryDB


class IStoryRepository(ABC):
    @abstractmethod
    def get_tags(self) -> Optional[List[TagsDB]]:
        pass

    @abstractmethod
    def get_tag_by_id(self, id) -> Optional[TagsDB]:
        pass

    @abstractmethod
    def add_story(self, user_story: UserStoryDB) -> UserStoryDB:
        pass