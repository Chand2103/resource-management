import pytest
from fastapi.testclient import TestClient
from src.apis import app
from datetime import datetime, timedelta
from jose import jwt
from unittest.mock import patch

# Test client fixture
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

# Test token fixture
@pytest.fixture
def test_token():
    payload = {
        "user_id": "test_user_123",
        # Add other necessary claims
    }
    return jwt.encode(payload, "be14be2aaab20c580d07eb9fc5038b5f7d35ec59243caed20c130ff13ba06874", algorithm="HS256")

# Test resource fixture
@pytest.fixture
def test_resource():
    return {
        "name": "Test Room",
        "type": "Conference Room",
        "capacity": 10
    }

# Test booking fixture
@pytest.fixture
def test_booking_0():
    # Use a very future date to reduce chances of conflicts
    return {
        "booked_by": "test_user",
        "resource_name": "Test Room",
        "start": "09:00:00",
        "end": "10:00:00",
        "booked_date": "2030-05-10"  # Using a far future date to avoid conflicts
    }

@pytest.fixture
def test_booking_1():
    # Use a very future date to reduce chances of conflicts
    return {
        "booked_by": "test_user",
        "resource_name": "Test Room",
        "start": "09:00:00",
        "end": "10:00:00",
        "booked_date": "2026-05-10"  # Using a far future date to avoid conflicts
    }

@pytest.fixture
def mock_get_current_user():
    with patch("src.dependencies.auth.get_current_user") as mock:
        mock.return_value = {
            "user_id": "test_user_123",
            "role": "admin",
            "email": "test@example.com",
            "created_at": "2024-01-01T00:00:00Z"
        }
        yield mock

# Apply the mock to all endpoints that use get_current_user
@pytest.fixture(autouse=True)
def apply_mock_get_current_user(mock_get_current_user):
    pass