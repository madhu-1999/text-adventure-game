from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from server.db.db import get_db
from server.src.models import TokenData
from server.src.repository import IUserRepository, UserRepository
from server.src.repository.story_repository import IStoryRepository
from server.src.repository.story_repository_impl import StoryRepository
from server.src.service import UserService
from server.src.service.story_service import StoryService
from server.src.utils import ALGORITHM, JWT_SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login', scheme_name='JWT')

async def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    return UserRepository(db)

async def get_story_repository(db: Session = Depends(get_db)) -> IStoryRepository:
    return StoryRepository(db)

async def get_user_service(repository: IUserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)

async def get_story_service(repository: IStoryRepository = Depends(get_story_repository)) -> StoryService:
    return StoryService(repository)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    """Gets user id of currently logged in user by decoding access token

    Args:
        token (str): Access token of currently logged in user.

    Raises:
        HTTP_401_UNAUTHORIZED : If token has expired or could not be decoded properly

    Returns:
        int: user id of currently logged in user
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)

        # Check if access token expired
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        
        return token_data.sub
    except (JWTError, ValidationError) as e:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
    