# Development Setup Guide

## Prerequisites

Before setting up the development environment, ensure you have the following installed:

- **Python 3.8+** (recommended: Python 3.11)
- **Docker** and **Docker Compose**
- **Git**
- **Make** (optional, for using Makefile commands)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd restaurant-seating-system
```

### 2. Environment Setup

```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

### 3. Start with Docker (Recommended)

```bash
# Start all services
make dev

# Or manually with Docker Compose
docker-compose up -d
```

### 4. Access the Application

- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:8501
- **Database**: localhost:3306

## Manual Setup (Without Docker)

### 1. Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Database Setup

#### Option A: Using Docker (Recommended)

```bash
# Start only the database
docker-compose up -d mariadb

# Wait for database to be ready
sleep 10
```

#### Option B: Local MariaDB Installation

```bash
# Install MariaDB (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install mariadb-server

# Start MariaDB
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Create database and user
sudo mysql -u root -p
```

```sql
CREATE DATABASE restaurant_seating;
CREATE USER 'restaurant_user'@'localhost' IDENTIFIED BY 'restaurant_password';
GRANT ALL PRIVILEGES ON restaurant_seating.* TO 'restaurant_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Database Migrations

```bash
# Run migrations
alembic upgrade head

# Or create tables directly
python -c "from backend.app.database.connection import create_tables; create_tables()"
```

### 4. Start the Backend

```bash
# Start the API server
cd backend
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Start the Frontend

```bash
# In a new terminal
cd frontend
streamlit run streamlit_app.py
```

## Development Workflow

### 1. Code Structure

```
restaurant-seating-system/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── database/       # Database setup
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic
│   ├── alembic/            # Database migrations
│   └── main.py             # Application entry point
├── frontend/               # Streamlit frontend
│   ├── pages/              # Page modules
│   ├── api_client.py       # API client
│   └── streamlit_app.py    # Main app
├── tests/                  # Test suite
├── docs/                   # Documentation
└── docker-compose.yml      # Docker configuration
```

### 2. Making Changes

#### Backend Changes

1. **Models**: Update `backend/app/models/`
2. **Services**: Update `backend/app/services/`
3. **API**: Update `backend/app/api/`
4. **Migrations**: Create new migration if database schema changes

```bash
# Create a new migration
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

#### Frontend Changes

1. **Pages**: Update `frontend/pages/`
2. **API Client**: Update `frontend/api_client.py`
3. **Styling**: Update CSS in `frontend/streamlit_app.py`

### 3. Testing

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=backend tests/

# Run tests in watch mode
pytest-watch tests/
```

### 4. Code Quality

```bash
# Format code
black backend/ frontend/ tests/

# Sort imports
isort backend/ frontend/ tests/

# Lint code
flake8 backend/ frontend/ tests/

# Type checking
mypy backend/
```

## Environment Variables

### Required Variables

```bash
# Database
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=restaurant_seating
DATABASE_USER=restaurant_user
DATABASE_PASSWORD=restaurant_password

# API
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Security
SECRET_KEY=your-secret-key-change-in-production
```

### Optional Variables

```bash
# CORS
ALLOWED_ORIGINS=["http://localhost:8501"]

# Logging
LOG_LEVEL=INFO

# Database
DATABASE_ECHO=false
```

## Database Management

### Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Show migration history
alembic history

# Show current revision
alembic current
```

### Database Reset

```bash
# Drop all tables and recreate
alembic downgrade base
alembic upgrade head

# Or manually
python -c "from backend.app.database.connection import engine, Base; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"
```

### Sample Data

```bash
# Load sample data (if available)
python scripts/load_sample_data.py
```

## Debugging

### Backend Debugging

```bash
# Run with debug logging
DEBUG=true python main.py

# Use Python debugger
python -m pdb main.py

# Use VS Code debugger
# Set breakpoints and use F5 to start debugging
```

### Frontend Debugging

```bash
# Run Streamlit with debug
streamlit run streamlit_app.py --logger.level debug

# Check browser console for errors
# Use Streamlit's built-in debugging features
```

### Database Debugging

```bash
# Connect to database
mysql -u restaurant_user -p restaurant_seating

# Check table structure
DESCRIBE restaurants;

# Check data
SELECT * FROM restaurants LIMIT 5;
```

## Common Issues

### 1. Database Connection Issues

**Problem**: Cannot connect to database
**Solutions**:
- Check if MariaDB is running: `sudo systemctl status mariadb`
- Verify connection details in `.env`
- Check firewall settings
- Ensure database exists and user has permissions

### 2. Port Already in Use

**Problem**: Port 8000 or 8501 already in use
**Solutions**:
- Change ports in `.env` file
- Kill existing processes: `lsof -ti:8000 | xargs kill -9`
- Use different ports: `uvicorn main:app --port 8001`

### 3. Import Errors

**Problem**: Module not found errors
**Solutions**:
- Ensure virtual environment is activated
- Install missing dependencies: `pip install -r requirements.txt`
- Check Python path: `export PYTHONPATH="${PYTHONPATH}:/path/to/project"`

### 4. Migration Issues

**Problem**: Migration fails or conflicts
**Solutions**:
- Check migration history: `alembic history`
- Resolve conflicts manually
- Reset migrations: `alembic downgrade base && alembic upgrade head`

## IDE Setup

### VS Code

1. **Install Extensions**:
   - Python
   - Pylance
   - Python Docstring Generator
   - SQLAlchemy Snippets

2. **Settings** (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"]
}
```

3. **Launch Configuration** (`.vscode/launch.json`):
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/backend/main.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

### PyCharm

1. **Project Setup**:
   - Open project root directory
   - Set Python interpreter to virtual environment
   - Mark `backend` and `frontend` as source roots

2. **Run Configurations**:
   - Backend: `backend/main.py`
   - Frontend: `streamlit run frontend/streamlit_app.py`

## Performance Optimization

### Database Optimization

```bash
# Enable query logging
DATABASE_ECHO=true

# Monitor slow queries
# Add to MariaDB configuration:
# slow_query_log = 1
# long_query_time = 2
```

### API Optimization

```bash
# Use production server
uvicorn main:app --workers 4

# Enable compression
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Next Steps

- [API Documentation](../api/overview.md)
- [Testing Guide](testing.md)
- [Deployment Guide](../deployment/overview.md)
- [Contributing Guide](contributing.md)
