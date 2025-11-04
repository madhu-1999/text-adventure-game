from email_validator import EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException, status
from server.src.exceptions import InvalidPasswordException, UsernameOrEmailExistsException
from server.src.dependencies import get_user_service
from server.src.models import UserDTO
from server.src.models.user import UserResponseDTO

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def register(user: UserDTO, user_service = Depends(get_user_service)):
    try:
        return await user_service.register_user(user)
    except (InvalidPasswordException, UsernameOrEmailExistsException, EmailNotValidError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except:
        raise HTTPException(status_code=500, detail="Registration failed!") 

@router.post("/login")
async def login():
    return {"message": "Login"}