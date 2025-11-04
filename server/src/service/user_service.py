import re
from email_validator import validate_email
from server.src.exceptions import InvalidPasswordException, UsernameOrEmailExistsException
from server.src.models.user import UserDTO, UserResponseDTO
from server.src.repository.user_repository import IUserRepository
from server.src.utils import get_hashed_password

def is_password_valid(password: str) -> bool:
    """
    Checks the strength of a password using a regex pattern.

    Criteria:
    - Minimum 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character from @#$%^&+=
    
    Args:
        password (str) : User password
    
    Returns:
        bool: True if password meets security requirements, otherwise False
    """

    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$"
    if re.fullmatch(regex, password):
        return True
    return False

class UserService():
    def __init__(self, repository: IUserRepository) -> None:
        self.repository = repository

    async def register_user(self, user: UserDTO) -> UserResponseDTO:
        """
        Register a new user

        Args:
            user (UserDTO): User DTO object

        Raises:
            UsernameOrEmailExistsException: If the username or email already exists
            InvalidPasswordException: If the password doesn't meet the security requirements
            EmailNotValidError: If the email format is invalid

        Returns:
            UserDTO: The newly created user DTO object
        """
        try:
             # Check if email is valid
            valid = validate_email(user.email)
       
            # Check if username or email exists
            if self.repository.check_if_username_or_email_exists(username=user.username, email=user.email):
                raise UsernameOrEmailExistsException(f"Username or email exists!")
            
            # Check if password is valid
            if not is_password_valid(user.password):
                raise InvalidPasswordException(f'Password is invalid!')
            
            # Hash password
            hashed_pwd = get_hashed_password(user.password)
            user.password = hashed_pwd

            # save to database
            created_user : UserDTO = self.repository.add(user)
            return UserResponseDTO.model_validate(created_user)
        except Exception as e: 
            raise e
        