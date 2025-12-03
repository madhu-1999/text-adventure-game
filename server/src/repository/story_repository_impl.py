from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from server.src.exceptions import DatabaseError
from sqlalchemy import select

from server.db.models import TagsDB
from .story_repository import IStoryRepository


class StoryRepository(IStoryRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_tags(self) -> List[TagsDB] | None:
        try:
            stmt = select(TagsDB)
            rows = self.session.execute(stmt)
            if rows:
                tags = list(rows.scalars().all())
                return tags
            return None
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve user by id {id}: {str(e)}") from e
    