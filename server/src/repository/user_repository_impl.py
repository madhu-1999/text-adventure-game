
from typing import Optional
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import insert, select, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from server.db.models import UserDB
from server.src.exceptions import DatabaseError
from server.src.models import UserDTO
from .user_repository import IUserRepository

class UserRepository(IUserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id: int) -> Optional[UserDTO]:
        try:
            user = self.session.get(UserDB, id)
            if user:
                return UserDTO.model_validate(user)
            return None
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve user by id {id}: {str(e)}") from e
    
    def get_by_username(self, username: str) -> Optional[UserDTO]:
        try:
            user = self.session.query(UserDB).filter(UserDB.username == username).first()
            if user:
                return UserDTO.model_validate(user)
            return None
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve user by username '{username}': {str(e)}") from e

    def check_if_username_or_email_exists(self, username: str, email: EmailStr) -> bool:
        try:
            stmt = select(UserDB).where(
                or_(
                    UserDB.username == username,
                    UserDB.email == email
                )
            )
            result = self.session.execute(stmt).first()
            return result is not None
        except SQLAlchemyError as e:
            raise DatabaseError(f'Failed to check if username: {username} or email: {email} exists') from e
    
    def add(self, user: UserDTO) -> UserDTO:
        try:
            new_user = UserDB(**user.model_dump())
            stmt = insert(UserDB).values(
                username=new_user.username, 
                email=new_user.email, 
                password=new_user.password
                ).returning(
                    UserDB.id, 
                    UserDB.username, 
                    UserDB.email,
                    UserDB.password
                )
            result = self.session.execute(stmt)
            row = result.first()
            self.session.commit()
            print(row)
            if not row:
                raise HTTPException(status_code=500, detail="User creation failed")
            return UserDTO.model_validate(row)
        except IntegrityError as e:
            self.session.rollback()
            raise DatabaseError(f"User already exists or constraint violation: {str(e)}") from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseError(f"Failed to add user: {str(e)}") from e