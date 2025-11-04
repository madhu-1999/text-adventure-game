# tests/e2e/test_user_flow.py
import pytest
from fastapi import status

class TestUserE2E:
    """End-to-end tests for complete user flows"""
    
    def test_complete_user_registration_flow(self, client):
        """Test complete user registration and verification flow"""
        # Step 1: Register new user
        user_data = {
            "id": None,
            "username": "e2euser",
            "email": "e2e@email.com",
            "password": "E2eTest1234@"
        }
        
        register_response = client.post("/users/register", json=user_data)
        assert register_response.status_code == status.HTTP_201_CREATED
        
        user_id = register_response.json()["id"]
        assert user_id is not None
        
        # Step 2: Verify user cannot register again
        duplicate_response = client.post("/users/register", json=user_data)
        assert duplicate_response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_multiple_user_registration(self, client):
        """Test registering multiple users"""
        users = [
            {"id": None,"username": "user1", "email": "user1@email.com", "password": "Pass1234@"},
            {"id": None,"username": "user2", "email": "user2@email.com", "password": "Pass1234@"},
            {"id": None,"username": "user3", "email": "user3@email.com", "password": "Pass1234@"},
        ]
        
        for user_data in users:
            response = client.post("/users/register", json=user_data)
            assert response.status_code == status.HTTP_201_CREATED
            assert response.json()["username"] == user_data["username"]