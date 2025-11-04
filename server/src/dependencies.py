from fastapi import Depends
from sqlalchemy.orm import Session
from server.db.db import get_db
from server.src.repository import IUserRepository, UserRepository
from server.src.service import UserService

def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    return UserRepository(db)

def get_user_service(repository: IUserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)