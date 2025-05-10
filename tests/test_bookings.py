import pytest
from datetime import datetime, timedelta

def test_create_booking(client, test_booking_0):
    response = client.post("/create-booking", json=test_booking_0)
    assert response.status_code == 200
    # Note: The actual response might vary based on your implementation
    # You might want to check for specific success messages or data

def test_create_booking_invalid_data(client):
    invalid_booking = {
        "booked_by": "test_user",
        "resource_name": "Test Room",
        "start": "09:00:00"
        # Missing end and booked_date
    }
    response = client.post("/create-booking", json=invalid_booking)
    assert response.status_code == 422  # Validation error

def test_get_bookings_unauthorized(client):
    response = client.get("/get-bookings")
    assert response.status_code == 401  # Unauthorized

def test_get_bookings_authorized(client, test_token, mock_get_current_user):
    headers = {
        "Authorization": f"Bearer {test_token}",
        "Content-Type": "application/json"
    }
    response = client.get("/get-bookings", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_check_availability(client, test_booking_0):
    params = {
        "resource_name": test_booking_0["resource_name"],
        "booking_date": test_booking_0["booked_date"]
    }
    response = client.get("/check-availability", params=params)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_booking(client, test_booking_1, mock_get_current_user):
    # First create a booking
    create_response = client.post("/create-booking", json=test_booking_1)
        
    assert create_response.status_code == 200
    assert "booking_id" in create_response.json()
    
    # Get the booking ID from the response
    booking_id = create_response.json()["booking_id"]

    # Delete the booking
    delete_response = client.request(
        "DELETE", 
        "/delete-booking", 
        json={"booking_id": booking_id}
    )
    assert delete_response.status_code == 200
    assert "status" in delete_response.json()
    assert delete_response.json()["status"] == "success"