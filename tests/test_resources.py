import pytest
from fastapi.testclient import TestClient

def test_get_resources(client):
    response = client.get("/get-resources")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_insert_resource(client, test_resource):
    response = client.post("/resource-insert", json=test_resource)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    assert data["data"][0]["resource_name"] == test_resource["name"]

def test_insert_resource_invalid_data(client):
    invalid_resource = {
        "name": "Test Room",
        "type": "Conference Room"
        # Missing capacity field
    }
    response = client.post("/resource-insert", json=invalid_resource)
    assert response.status_code == 422  # Validation error

def test_get_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "data" in response.json() 