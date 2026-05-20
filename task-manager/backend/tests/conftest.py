# ==============================
# Test fixtures and configuration
# ==============================
# Configure test environment variables for isolated database tests.
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_pytest.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, get_db
from main import app


@pytest.fixture
def db() -> Session:
    # Reset database before each test run.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db: Session):
    # Override the app database dependency for testing.
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def user_credentials():
    # Default user credentials used in tests.
    return {"email": "testuser@example.com", "password": "secret123"}


@pytest.fixture
def registered_user(client, user_credentials):
    # Register a user and confirm the endpoint works.
    response = client.post("/register", json=user_credentials)
    assert response.status_code == 201
    return user_credentials


@pytest.fixture
def auth_headers(client, registered_user):
    # Log in and return authentication headers for protected endpoints.
    response = client.post(
        "/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
