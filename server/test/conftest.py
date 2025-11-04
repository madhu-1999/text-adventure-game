import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from server.src.app import app
from server.db.db import get_db
from server.db.models import UserDB, Base

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db_engine():
    """Create a test database engine"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db(test_db_engine):
    """Create a test database session"""
    TestingSessionLocal = sessionmaker(
        autocommit=False, 
        bind=test_db_engine
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with test database"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user_data():
    """Sample user data for tests"""
    return {
        "id":None,
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "Test1234@"
    }

@pytest.fixture
def sample_user_db(test_db, sample_user_data):
    """Create a user in the test database"""
    from server.src.utils import get_hashed_password
    
    user = UserDB(
        username=sample_user_data["username"],
        email=sample_user_data["email"],
        password=get_hashed_password(sample_user_data["password"])
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user