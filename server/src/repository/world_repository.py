from abc import ABC, abstractmethod
from typing import Optional

from server.db.models import WorldDB


class IWorldRepository(ABC):
    @abstractmethod
    def create_world(self, world: WorldDB) -> Optional[WorldDB]:
        pass

    