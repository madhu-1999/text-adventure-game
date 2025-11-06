from urllib import response
import pytest
from fastapi import HTTPException, status

from server.src.dependencies import get_current_user

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

    def test_login_success(self, client, sample_user_data, sample_user_db):
        """Test login success"""
        
        data = {
            "username": sample_user_data["username"],
            "password": sample_user_data["password"],
        }
       
        response = client.post("/users/login", data=data)

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_failure(self, client, sample_user_data, sample_user_db):
        """Test login failure due to incorrect password"""
        
        data = {
            "username": sample_user_data["username"],
            "password": "wrongpassword"
        }
       
        response = client.post("/users/login", data=data)

        assert response.status_code == 400
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client, sample_user_data, sample_user_db):
        """Test login failure due to incorrect password"""
        
        data = {
            "username": "nonexistent",
            "password": sample_user_data["password"]
        }
       
        response = client.post("/users/login", data=data)

        assert response.status_code == 400
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_missing_username(self, client):
        """Test login without username"""
        response = client.post(
            "/users/login",
            data={
                "password": "somepassword"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_missing_password(self,client):
        """Test login without password"""
        response = client.post(
            "/users/login",
            data={
                "username": "testuser"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_access_token_success(self, client, sample_user_data, sample_user_db):
        """Test access token contains correct data"""
        
        data = {
            "username": sample_user_data["username"],
            "password": sample_user_data["password"],
        }
       
        response = client.post("/users/login", data=data)
        user_id = await get_current_user(response.json()['access_token'])
        assert response.status_code == 200
        assert user_id == sample_user_db.id

    @pytest.mark.asyncio
    async def test_access_token_failure(self):
        """Test access token contains incorrect data"""
        
        with pytest.raises(HTTPException):
           await get_current_user('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30')

    def test_get_current_user_details_success(self, client, sample_user_data, sample_user_db):
        """Test successful fetching of logged in user details"""
        
        data = {
            "username": sample_user_data["username"],
            "password": sample_user_data["password"],
        }
       
        response = client.post("/users/login", data=data)

        assert response.status_code == 200
        assert "access_token" in response.json()

        details_response = client.get("/users/me", headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer {response.json()['access_token']}"
        })

        assert details_response.json()["id"] == sample_user_db.id
        assert details_response.json()["username"] == sample_user_db.username
        assert details_response.json()["email"] == sample_user_db.email


    def test_get_current_user_details_failure(self, client):
        """Test failure due to expired token"""
        
        # Access token: id = 1 exp = 1762414310
        details_response = client.get("/users/me", headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTc2MjQxNDMxMH0.A1hRQaVAFk-m1iU1M-ZwEngmgKeKucYoNO_w5YWyXEc"
        })

        assert details_response.status_code == 401