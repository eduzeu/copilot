import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_career_copilot.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient

import app.models  # noqa: F401
from app.db.base import Base
from app.db.session import engine
from app.main import app


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    client.post("/auth/register", json={"email": "user@example.com", "password": "password123"})
    response = client.post("/auth/login", json={"email": "user@example.com", "password": "password123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
