from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from server.src.exceptions import DatabaseError
from sqlalchemy import insert, select

from server.db.models import TagsDB, UserStoryDB, WorldDB
from .story_repository import IStoryRepository


class StoryRepository(IStoryRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_tags(self) -> Optional[List[TagsDB]]:
        try:
            stmt = select(TagsDB)
            rows = self.session.execute(stmt)
            if rows:
                tags = list(rows.scalars().all())
                return tags
            return None
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve user by id {id}: {str(e)}") from e
    
    def get_tag_by_id(self, id) -> Optional[TagsDB]:
        try:
            stmt = select(TagsDB).where(TagsDB.id == id)
            tag =  self.session.execute(stmt).first()
            if tag:
                return tag[0]
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve user by id {id}: {str(e)}") from e
        
    def add_story_and_world(self, user_story: UserStoryDB, world: WorldDB) -> Tuple[UserStoryDB, WorldDB]:
        try:
            # Save world
            stmt = insert(WorldDB).values(
                world=world.world
            ).returning(
                WorldDB
            )
            saved_world = self.session.execute(stmt).first()
            if not saved_world:
                self.session.rollback()
                raise DatabaseError("Could not insert world!")
            
            # Set world_id
            user_story.id = saved_world[0].id

            # Save user story
            stmt = insert(UserStoryDB).values(
                user_id=user_story.user_id,
                title=user_story.title,
                tag_id=user_story.tag_id, 
                prompt=user_story.prompt, 
                world_id=user_story.world_id
            ).returning(
                UserStoryDB
            )
            saved_user_story = self.session.execute(stmt).first()
            if not saved_user_story:
                self.session.rollback()
                raise DatabaseError("Could not insert story:")
            self.session.commit()
            return (saved_user_story[0], saved_world[0])
        except IntegrityError as e:
            self.session.rollback()
            raise DatabaseError(f"Could not insert story: {str(e)}") from e
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve user by id {id}: {str(e)}") from e