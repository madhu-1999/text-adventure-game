from typing import Annotated
from email_validator import EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from server.src.dependencies import get_current_user, get_user_service
from server.src.exceptions import InvalidPasswordException, UsernameOrEmailExistsException
from server.src.models import UserDTO, Token, UserResponseDTO
from server.src.utils import create_access_token

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/register", summary="User Registration", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def register(user: UserDTO, user_service = Depends(get_user_service)):
    try:
        return await user_service.register_user(user)
    except (InvalidPasswordException, UsernameOrEmailExistsException, EmailNotValidError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed!") 

@user_router.post("/login", summary="Create access and refresh token for the user", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_service = Depends(get_user_service)):
    try:
        user = await user_service.authenticate_user(form_data.username, form_data.password)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )
        return {
            "access_token": create_access_token(subject=user.id)
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )
    
@user_router.get('/me', summary='Get details of currently logged in user', response_model=UserResponseDTO)
async def get_me(user_id: int = Depends(get_current_user), user_service = Depends(get_user_service)):
    try:
        user =  await user_service.get_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user or password"
            )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )
     