from abc import ABC, abstractmethod
from typing import List, Optional

from server.db.models import TagsDB


class IStoryRepository(ABC):
    @abstractmethod
    def get_tags(self) -> Optional[List[TagsDB]]:
        pass