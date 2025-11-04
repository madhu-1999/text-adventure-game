import pytest
from unittest.mock import Mock, patch
from server.src.service import UserService
from server.src.models import UserDTO, UserResponseDTO
from server.src.exceptions import (
    InvalidPasswordException,
    UsernameOrEmailExistsException
)

class TestUserService:
    """Unit tests for UserService"""
    
    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return Mock()
    
    @pytest.fixture
    def user_service(self, mock_repository):
        """Create UserService with mock repository"""
        return UserService(mock_repository)
    
    @pytest.mark.asyncio
    async def test_register_user_success(self, user_service, mock_repository):
        """Test successful user registration"""
        # Arrange
        user_create = UserDTO(
            id=None,
            username="testuser",
            email="test@gmail.com",
            password="Test1234@"
        )
        
        mock_repository.check_if_username_or_email_exists.return_value = False
        mock_repository.add.return_value = UserResponseDTO(
            id=1,
            username="testuser",
            email="test@gmail.com",
        )
        
        # Act
        result = await user_service.register_user(user_create)
        
        # Assert
        assert result.username == "testuser"
        assert result.email == "test@gmail.com"
        mock_repository.add.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_register_user_duplicate_username(self, user_service, mock_repository):
        """Test registration with duplicate username fails"""
        # Arrange
        user_create = UserDTO(
            id=None,
            username="existing",
            email="test@gmail.com",
            password="Test1234@"
        )
        
        mock_repository.check_if_username_or_email_exists.return_value = True
        mock_repository.add.return_value = UserDTO(
            id=1,
            username="testuser",
            email="test@gmail.com",
            password="hashed_password"
        )
        
       # Act & Assert
        with pytest.raises(UsernameOrEmailExistsException):
            await user_service.register_user(user_create) 
        mock_repository.add.assert_not_called()
        
    @pytest.mark.asyncio
    async def test_register_user_invalid_password(self, user_service, mock_repository):
        """Test registration with invalid password fails"""
        # Arrange
        user_create = UserDTO(
            id=None,
            username="testuser",
            email="test@gmail.com",
            password="weak"
        )
        
        mock_repository.check_if_username_or_email_exists.return_value = False
        
        # Act & Assert
        with pytest.raises(InvalidPasswordException):
            await user_service.register_user(user_create)
        
        mock_repository.add.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_register_user_invalid_email(self, user_service, mock_repository):
        """Test registration with invalid email fails"""
        from email_validator import EmailNotValidError
        
        # Arrange
        user_create = UserDTO(
            id=None,
            username="testuser",
            email="invalid@example.com",
            password="Test1234@"
        )
        
        # Act & Assert
        with pytest.raises(EmailNotValidError):
            await user_service.register_user(user_create)
    
    @patch('server.src.service.user_service.get_hashed_password')
    @pytest.mark.asyncio
    async def test_password_is_hashed(self, mock_hash, user_service, mock_repository):
        """Test that password is hashed before saving"""
        # Arrange
        user_create = UserDTO(
            id=None,
            username="testuser",
            email="test@gmail.com",
            password="Test1234@"
        )
        
        mock_hash.return_value = "hashed_password"
        mock_repository.check_if_username_or_email_exists.return_value = False
        mock_repository.add.return_value = UserDTO(
            id=1,
            username="testuser",
            email="test@example.com",
            password="hashed_password"
        )
        
        # Act
        await user_service.register_user(user_create)
        
        # Assert
        mock_hash.assert_called_once_with("Test1234@")