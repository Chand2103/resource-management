# Quick Start Guide

This guide provides a streamlined set of instructions to get you up and running with the Resource Management System quickly.

## Getting Started

### 1. Clone the Repository and Set Up Environment

```bash
# Clone repository
git clone https://github.com/yourusername/resource-management.git
cd resource-management

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
# Start the FastAPI server
uvicorn src.apis:app --reload
```

The API will now be running at http://localhost:8000

### 3. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Quick Tests

Run a quick test to ensure everything is working:

```bash
pytest tests/test_resources.py
```

## Common Endpoints

Here are some endpoints you can try right away:

### Get All Resources
```
GET http://localhost:8000/get-resources
```

### Check Resource Availability
```
GET http://localhost:8000/check-availability?resource_name=Test%20Room&booking_date=2023-06-01
```

### Create a Booking (requires authentication)
```json
POST http://localhost:8000/create-booking
Content-Type: application/json

{
  "booked_by": "user123",
  "resource_name": "Test Room",
  "start": "09:00:00",
  "end": "10:00:00",
  "booked_date": "2023-06-01"
}
```

## Common Issues and Solutions

### Authentication Issues
If you're getting 401 or 403 errors, ensure:
- You've included a valid JWT token in the Authorization header
- The user exists in the Resource_Management_Admins table

### Database Connection
If you're having trouble connecting to Supabase:
- Verify the Supabase URL and key in the `src/apis.py` file
- Ensure your Supabase database is running and accessible

### Testing Issues
For testing issues:
- Make sure your test fixtures in `conftest.py` match your database schema
- Use the mock authentication for testing protected endpoints 