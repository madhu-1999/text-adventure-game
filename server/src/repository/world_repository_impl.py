from typing import Optional
from sqlalchemy import insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from server.src.exceptions import DatabaseError
from server.db.models import WorldDB
from .world_repository import IWorldRepository


class WorldRepository(IWorldRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_world(self, world: WorldDB) -> Optional[WorldDB]:
        try:
            stmt = insert(WorldDB).values(
                world=world.world
            ).returning(
                WorldDB
            )

            result = self.session.execute(stmt).first()
            self.session.commit()
            if result:
                return result[0]
        except IntegrityError as e:
            self.session.rollback()
            raise DatabaseError(f"Could not insert world: {str(e)}") from e
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve user by id {id}: {str(e)}") from e

    