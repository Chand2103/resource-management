# Resource Management System

A comprehensive system for managing and booking resources within an organization. The application integrates with IoT devices and offers a RESTful API for resource reservation, availability checking, and user management.

## Features

- Resource booking and management
- Resource availability checking
- User authentication and authorization
- IoT device integration
- Admin dashboard for resource allocation
- People management system

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: JWT-based authentication
- **Optimization**: Google OR-Tools for availability algorithms
- **IoT Communication**: MQTT Protocol (Paho MQTT)
- **Testing**: Pytest

## Project Structure

```
resource-management/
├── src/                     # Source code
│   ├── apis.py              # API endpoints
│   ├── or_tools.py          # Resource scheduling algorithms
│   ├── dependencies/        # FastAPI dependencies
│   │   └── auth.py          # Authentication handling
│   ├── utils/               # Utilities
│   │   └── token.py         # JWT token handling
│   └── IoT_system/          # IoT device integration
│       ├── publisher.py     # MQTT message publisher
│       └── subscriber.py    # MQTT message subscriber
├── tests/                   # Test files
│   ├── conftest.py          # Test fixtures
│   ├── test_auth.py         # Authentication tests
│   ├── test_bookings.py     # Booking functionality tests
│   ├── test_or_tools.py     # Algorithm tests
│   └── test_resources.py    # Resource management tests
├── requirements.txt         # Python dependencies
└── pytest.ini              # Pytest configuration
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Supabase account (for database)
- MQTT broker (for IoT functionality)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/resource-management.git
   cd resource-management
   ```

2. Create and activate a virtual environment
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (optional - currently hardcoded in the application)
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   JWT_SECRET_KEY=your_jwt_secret
   ```

### Database Setup

1. Create a Supabase project
2. Set up the following tables:
   - Resources
   - Bookings
   - Resource_Management_Admins
   - People

### Running the Application

Start the FastAPI server:
```bash
uvicorn src.apis:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

- `POST /create-booking`: Create a new resource booking
- `GET /get-bookings`: Get all bookings (requires authentication)
- `GET /check-availability`: Check resource availability
- `DELETE /delete-booking`: Delete a booking
- `GET /get-resources`: Get all resources
- `POST /resource-insert`: Add a new resource
- `GET /get-people`: Get all people in the system
- `POST /add-people`: Add a new person
- `PUT /assign-people`: Assign a person to a resource

## Testing

Run the tests using pytest:
```bash
pytest
```

You can also run specific test files:
```bash
pytest tests/test_bookings.py
pytest tests/test_auth.py
```

## IoT Integration

The system integrates with IoT devices using MQTT protocol:

- `publisher.py`: Sends commands to IoT devices
- `subscriber.py`: Receives status updates from IoT devices

To use the IoT functionality, ensure you have a running MQTT broker (like Mosquitto).

