import pytest
from src.utils.token import decode_token

def test_decode_token(test_token):
    user_id = decode_token(test_token)
    assert user_id == "test_user_123"

def test_decode_invalid_token():
    invalid_token = "invalid.token.here"
    user_id = decode_token(invalid_token)
    assert user_id is None

def test_get_current_user_unauthorized(client):
    response = client.get("/get-bookings")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_current_user_invalid_token(client):
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = client.get("/get-bookings", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token" 