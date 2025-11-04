import pytest
from fastapi import status

class TestUserRouter:
    """Integration tests for User router"""
    
    def test_register_user_success(self, client, sample_user_data):
        """Test successful user registration endpoint"""
        # Act
        response = client.post("/users/register", json=sample_user_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == sample_user_data["username"]
        assert data["email"] == sample_user_data["email"]
        assert "password" not in data  # Password should not be returned
        assert "id" in data
    
    def test_register_duplicate_username(self, client, sample_user_db):
        """Test registration with duplicate username returns 400"""
        # Arrange
        duplicate_data = {
            "id":None,
            "username": sample_user_db.username,
            "email": "different@gmail.com",
            "password": "Test1234@"
        }
        
        # Act
        response = client.post("/users/register", json=duplicate_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "exists" in response.json()["detail"].lower()
    
    def test_register_duplicate_email(self, client, sample_user_db):
        """Test registration with duplicate email returns 400"""
        # Arrange
        duplicate_data = {
            "id": None,
            "username": "differentuser",
            "email": sample_user_db.email,
            "password": "Test1234@"
        }
        
        # Act
        response = client.post("/users/register", json=duplicate_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email returns 422"""
        # Arrange
        invalid_data = {
            "id": None,
            "username": "testuser",
            "email": "not-an-email",
            "password": "Test1234@"
        }
        
        # Act
        response = client.post("/users/register", json=invalid_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_weak_password(self, client):
        """Test registration with weak password returns 400"""
        # Arrange
        weak_password_data = {
            "id": None,
            "username": "testuser",
            "email": "test@email.com",
            "password": "weak"
        }
        
        # Act
        response = client.post("/users/register", json=weak_password_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.json()["detail"].lower()
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields returns 422"""
        # Arrange
        incomplete_data = {
            "username": "testuser"
            # Missing email and password
        }
        
        # Act
        response = client.post("/users/register", json=incomplete_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY