from abc import ABC, abstractmethod
from typing import Optional

from pydantic import EmailStr
from server.src.models.user import UserDTO

class IUserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserDTO]:
        pass 

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UserDTO]:
        pass

    @abstractmethod
    def check_if_username_or_email_exists(self, username: str, email: EmailStr) -> bool:
        pass

    @abstractmethod
    def add(self, user: UserDTO) -> UserDTO:
        pass