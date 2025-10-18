# Restaurant Seating System API

A comprehensive FastAPI-based backend system for managing restaurant seating, reservations, and table assignments.

## Features

- **Restaurant Management**: CRUD operations for restaurants, sections, and tables
- **Party Management**: Handle customer parties and their status
- **Reservation System**: Create, update, and manage reservations
- **Waiting List**: Manage walk-in customers and waiting lists
- **Server Management**: Track restaurant staff and their assignments
- **Table Assignments**: Assign tables to parties and reservations
- **Analytics**: Occupancy analytics and reporting
- **Real-time Availability**: Check table availability in real-time

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: SQL toolkit and ORM
- **MariaDB**: Relational database
- **Alembic**: Database migration tool
- **Docker & Docker Compose**: Containerization and orchestration

## Project Structure

```
backend/
├── app/
│   ├── api/                 # API route handlers
│   │   ├── restaurants.py
│   │   ├── parties.py
│   │   ├── reservations.py
│   │   ├── waiting_list.py
│   │   ├── servers.py
│   │   └── assignments.py
│   ├── core/               # Core configuration
│   │   └── config.py
│   ├── database/           # Database configuration
│   │   └── connection.py
│   ├── models/             # Data models
│   │   ├── schemas.py      # Pydantic models
│   │   └── database.py     # SQLAlchemy models
│   └── services/           # Business logic
│       ├── restaurant_service.py
│       ├── party_service.py
│       ├── reservation_service.py
│       ├── waiting_list_service.py
│       ├── server_service.py
│       └── assignment_service.py
├── alembic/                # Database migrations
├── main.py                 # FastAPI application entry point
└── requirements.txt        # Python dependencies
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd restaurant-seating-system
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Local Development

1. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database configuration
   ```

4. **Run database migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

5. **Start the development server**
   ```bash
   python main.py
   ```

## API Endpoints

### Restaurants
- `GET /api/v1/restaurants` - List all restaurants
- `POST /api/v1/restaurants` - Create a new restaurant
- `GET /api/v1/restaurants/{id}` - Get restaurant by ID
- `PUT /api/v1/restaurants/{id}` - Update restaurant
- `DELETE /api/v1/restaurants/{id}` - Delete restaurant

### Complex Restaurant Operations
- `POST /api/v1/restaurants/{id}/seating/assign-table` - Assign table to party
- `GET /api/v1/restaurants/{id}/seating/check-availability` - Check table availability
- `GET /api/v1/restaurants/{id}/analytics/occupancy` - Get occupancy analytics

### Parties
- `GET /api/v1/parties` - List all parties
- `POST /api/v1/parties` - Create a new party
- `GET /api/v1/parties/{id}` - Get party by ID
- `PUT /api/v1/parties/{id}` - Update party
- `DELETE /api/v1/parties/{id}` - Delete party

### Reservations
- `GET /api/v1/reservations` - List all reservations
- `POST /api/v1/reservations` - Create a new reservation
- `GET /api/v1/reservations/{id}` - Get reservation by ID
- `PUT /api/v1/reservations/{id}` - Update reservation
- `DELETE /api/v1/reservations/{id}` - Cancel reservation

### Waiting List
- `GET /api/v1/waiting-list` - List all waiting list entries
- `POST /api/v1/waiting-list` - Add party to waiting list
- `GET /api/v1/waiting-list/restaurants/{id}/next` - Get next party from waiting list

### Servers
- `GET /api/v1/servers` - List all servers
- `POST /api/v1/servers` - Create a new server
- `GET /api/v1/servers/{id}` - Get server by ID
- `PUT /api/v1/servers/{id}` - Update server
- `DELETE /api/v1/servers/{id}` - Delete server

### Assignments
- `GET /api/v1/assignments/table-assignments` - List table assignments
- `POST /api/v1/assignments/table-assignments` - Create table assignment
- `PUT /api/v1/assignments/table-assignments/{id}/complete` - Complete table assignment

## Database Schema

The system uses a relational database with the following main entities:

- **Restaurants**: Restaurant information and settings
- **Sections**: Restaurant sections/areas
- **Tables**: Individual tables with capacity and status
- **Parties**: Customer groups
- **Reservations**: Scheduled dining reservations
- **Waiting List**: Walk-in customers waiting for tables
- **Servers**: Restaurant staff
- **Table Assignments**: Active table assignments
- **Reservation Assignments**: Reservation-to-table assignments

## Configuration

The application can be configured through environment variables:

```bash
# Database Configuration
DATABASE_URL=mysql+pymysql://user:password@host:port/database
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=restaurant_seating
DATABASE_USER=restaurant_user
DATABASE_PASSWORD=restaurant_password

# API Configuration
APP_NAME=Restaurant Seating System API
APP_VERSION=1.0.0
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-secret-key-change-in-production
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black backend/
isort backend/
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.