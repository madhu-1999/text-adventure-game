import pytest
from sqlalchemy import null
from server.src.exceptions import DatabaseError
from server.src.repository import UserRepository
from server.src.models import UserDTO
from server.db.models import UserDB

class TestUserRepository:
    """Unit Tests for UserRepository"""

    def test_add_user_success(self, test_db):
        """Test adding a user successfully"""

        repo = UserRepository(test_db)
        user_data = UserDTO(
            id=None,
            username="newuser",
            email="new@example.com",
            password="NewEx123#"
        )

        result = repo.add(user=user_data)

        assert result.id is not None
        assert result.username == "newuser"
        assert result.email == "new@example.com"

    def test_add_duplicate_username_fails(self, test_db, sample_user_db):
        """Test that adding duplicate username raises error"""

        repo = UserRepository(test_db)
        duplicate_user = UserDTO(
            id=None,
            username=sample_user_db.username,
            email="different@example.com",
            password="hashed_password"
        )
        
        with pytest.raises(DatabaseError):
            repo.add(duplicate_user)
    
    def test_check_username_exists(self, test_db, sample_user_db):
        """Test checking if username exists"""
        repo = UserRepository(test_db)
        
        exists = repo.check_if_username_or_email_exists(
            username=sample_user_db.username,
            email="other@example.com"
        )
        
        assert exists is True
    
    def test_check_username_not_exists(self, test_db):
        """Test checking if username doesn't exist"""
        # Arrange
        repo = UserRepository(test_db)
        
        # Act
        exists = repo.check_if_username_or_email_exists(
            username="nonexistent",
            email="none@example.com"
        )
        
        # Assert
        assert exists is False

    def test_get_user_by_username(self, test_db, sample_user_db):
        """Test retrieving user by username"""
        # Arrange
        repo = UserRepository(test_db)
        
        # Act
        user = repo.get_by_username(sample_user_db.username)
        
        # Assert
        assert user is not None
        assert user.username == sample_user_db.username
        assert user.email == sample_user_db.email

    def test_get_user_by_id(self, test_db, sample_user_db):
        repo = UserRepository(test_db)

        user = repo.get_by_id(sample_user_db.id)

        assert user is not None
