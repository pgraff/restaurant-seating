# Testing Guide

## Overview

The Restaurant Seating System includes a comprehensive test suite covering unit tests, integration tests, and API tests. The testing framework uses pytest with additional plugins for coverage, mocking, and database testing.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Test configuration and fixtures
├── test_api.py              # API endpoint tests
├── test_models.py           # Data model tests
├── test_services.py         # Service layer tests
├── test_complex_operations.py # Complex business logic tests
├── test_simple.py           # Basic functionality tests
├── test_main.py             # Application entry point tests
└── run_tests.py             # Test runner script
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run specific test function
pytest tests/test_api.py::test_create_restaurant

# Run tests matching a pattern
pytest -k "test_create"
```

### Test Coverage

```bash
# Run tests with coverage
pytest --cov=backend tests/

# Generate HTML coverage report
pytest --cov=backend --cov-report=html tests/

# Show coverage in terminal
pytest --cov=backend --cov-report=term-missing tests/
```

### Test Database

```bash
# Run tests with test database
pytest --test-db

# Use in-memory SQLite for faster tests
pytest --test-db=sqlite:///:memory:
```

## Test Configuration

### Pytest Configuration (`pytest.ini`)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=backend
    --cov-report=term-missing
    --cov-report=html
markers =
    unit: Unit tests
    integration: Integration tests
    api: API tests
    slow: Slow running tests
    database: Tests requiring database
```

### Test Fixtures (`conftest.py`)

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from backend.app.database.connection import Base, get_db
from backend.main import app

# Test database setup
@pytest.fixture(scope="session")
def test_db_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    SessionLocal = sessionmaker(bind=test_db_engine)
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="function")
def test_client(test_db_session):
    def override_get_db():
        yield test_db_session
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# Sample data fixtures
@pytest.fixture
def sample_restaurant():
    return {
        "name": "Test Restaurant",
        "address": "123 Test St",
        "phone": "+1234567890",
        "opening_time": "09:00:00",
        "closing_time": "22:00:00",
        "max_capacity": 100
    }

@pytest.fixture
def sample_party():
    return {
        "name": "Test Party",
        "size": 4,
        "phone": "+1234567890",
        "email": "test@example.com"
    }
```

## Test Categories

### 1. Unit Tests

Test individual functions and methods in isolation.

```python
# tests/test_services.py
import pytest
from backend.app.services.restaurant_service import RestaurantService
from backend.app.models.schemas import RestaurantCreate

def test_create_restaurant(test_db_session, sample_restaurant):
    service = RestaurantService(test_db_session)
    restaurant_data = RestaurantCreate(**sample_restaurant)
    
    restaurant = service.create_restaurant(restaurant_data)
    
    assert restaurant.name == sample_restaurant["name"]
    assert restaurant.address == sample_restaurant["address"]
    assert restaurant.id is not None

def test_get_restaurant_not_found(test_db_session):
    service = RestaurantService(test_db_session)
    restaurant = service.get_restaurant("non-existent-id")
    
    assert restaurant is None
```

### 2. Integration Tests

Test interactions between different components.

```python
# tests/test_complex_operations.py
import pytest
from backend.app.services.restaurant_service import RestaurantService
from backend.app.services.party_service import PartyService
from backend.app.services.assignment_service import AssignmentService

def test_table_assignment_workflow(test_db_session, sample_restaurant, sample_party):
    # Create restaurant
    restaurant_service = RestaurantService(test_db_session)
    restaurant = restaurant_service.create_restaurant(sample_restaurant)
    
    # Create table
    table = restaurant_service.create_table({
        "table_number": "T1",
        "capacity": 4,
        "location": "Main Dining",
        "restaurant_id": restaurant.id
    })
    
    # Create party
    party_service = PartyService(test_db_session)
    party = party_service.create_party(sample_party)
    
    # Create server
    server = restaurant_service.create_server({
        "first_name": "John",
        "last_name": "Doe",
        "employee_id": "EMP001",
        "restaurant_id": restaurant.id
    })
    
    # Assign table to party
    assignment_service = AssignmentService(test_db_session)
    assignment = assignment_service.create_table_assignment({
        "table_id": table.id,
        "party_id": party.id,
        "server_id": server.id
    })
    
    assert assignment.id is not None
    assert assignment.status == "ACTIVE"
    
    # Verify table status updated
    updated_table = restaurant_service.get_table(table.id)
    assert updated_table.status == "OCCUPIED"
    
    # Verify party status updated
    updated_party = party_service.get_party(party.id)
    assert updated_party.status == "SEATED"
```

### 3. API Tests

Test HTTP endpoints and request/response handling.

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient

def test_create_restaurant_api(test_client, sample_restaurant):
    response = test_client.post("/api/v1/restaurants", json=sample_restaurant)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_restaurant["name"]
    assert data["id"] is not None

def test_get_restaurants_api(test_client, sample_restaurant):
    # Create a restaurant first
    test_client.post("/api/v1/restaurants", json=sample_restaurant)
    
    # Get all restaurants
    response = test_client.get("/api/v1/restaurants")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 1

def test_create_restaurant_validation_error(test_client):
    invalid_data = {
        "name": "",  # Empty name should fail validation
        "address": "123 Test St",
        "phone": "+1234567890",
        "opening_time": "09:00:00",
        "closing_time": "22:00:00",
        "max_capacity": 100
    }
    
    response = test_client.post("/api/v1/restaurants", json=invalid_data)
    
    assert response.status_code == 422
    assert "validation error" in response.json()["message"].lower()
```

## Test Data Management

### Fixtures for Common Data

```python
# tests/conftest.py
@pytest.fixture
def restaurant_with_tables(test_db_session):
    """Create a restaurant with sample tables"""
    restaurant_service = RestaurantService(test_db_session)
    
    # Create restaurant
    restaurant = restaurant_service.create_restaurant({
        "name": "Test Restaurant",
        "address": "123 Test St",
        "phone": "+1234567890",
        "opening_time": "09:00:00",
        "closing_time": "22:00:00",
        "max_capacity": 100
    })
    
    # Create tables
    tables = []
    for i in range(5):
        table = restaurant_service.create_table({
            "table_number": f"T{i+1}",
            "capacity": 4,
            "location": f"Section {i//2 + 1}",
            "restaurant_id": restaurant.id
        })
        tables.append(table)
    
    return {"restaurant": restaurant, "tables": tables}

@pytest.fixture
def active_servers(test_db_session, restaurant_with_tables):
    """Create active servers for testing"""
    server_service = ServerService(test_db_session)
    restaurant_id = restaurant_with_tables["restaurant"].id
    
    servers = []
    for i in range(3):
        server = server_service.create_server({
            "first_name": f"Server{i+1}",
            "last_name": "Test",
            "employee_id": f"EMP{i+1:03d}",
            "restaurant_id": restaurant_id,
            "is_active": True
        })
        servers.append(server)
    
    return servers
```

### Database State Management

```python
@pytest.fixture(autouse=True)
def clean_database(test_db_session):
    """Clean database before each test"""
    # This runs before each test
    yield
    # This runs after each test
    test_db_session.rollback()
    test_db_session.close()
```

## Mocking and Stubbing

### External Service Mocking

```python
# tests/test_services.py
from unittest.mock import patch, MagicMock

@patch('backend.app.services.restaurant_service.send_notification')
def test_restaurant_creation_sends_notification(mock_send_notification, test_db_session):
    service = RestaurantService(test_db_session)
    restaurant_data = RestaurantCreate(**sample_restaurant)
    
    restaurant = service.create_restaurant(restaurant_data)
    
    # Verify notification was sent
    mock_send_notification.assert_called_once_with(
        f"New restaurant created: {restaurant.name}"
    )

@patch('backend.app.services.assignment_service.calculate_wait_time')
def test_assignment_calculates_wait_time(mock_calculate_wait_time, test_db_session):
    mock_calculate_wait_time.return_value = 15
    
    service = AssignmentService(test_db_session)
    wait_time = service.get_estimated_wait_time("restaurant-id")
    
    assert wait_time == 15
    mock_calculate_wait_time.assert_called_once_with("restaurant-id")
```

### Database Mocking

```python
@pytest.fixture
def mock_db_session():
    """Mock database session for unit tests"""
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    return mock_session

def test_service_with_mock_db(mock_db_session):
    service = RestaurantService(mock_db_session)
    # Test service logic without database
    pass
```

## Performance Testing

### Load Testing

```python
# tests/test_performance.py
import pytest
import time
from concurrent.futures import ThreadPoolExecutor

def test_concurrent_restaurant_creation(test_client, sample_restaurant):
    """Test creating multiple restaurants concurrently"""
    
    def create_restaurant(i):
        data = sample_restaurant.copy()
        data["name"] = f"Restaurant {i}"
        response = test_client.post("/api/v1/restaurants", json=data)
        return response.status_code == 201
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_restaurant, i) for i in range(50)]
        results = [future.result() for future in futures]
    
    end_time = time.time()
    
    assert all(results)
    assert end_time - start_time < 10  # Should complete within 10 seconds
```

### Database Performance

```python
def test_database_query_performance(test_db_session):
    """Test database query performance"""
    service = RestaurantService(test_db_session)
    
    # Create test data
    for i in range(100):
        service.create_restaurant({
            "name": f"Restaurant {i}",
            "address": f"Address {i}",
            "phone": f"+123456789{i:02d}",
            "opening_time": "09:00:00",
            "closing_time": "22:00:00",
            "max_capacity": 100
        })
    
    start_time = time.time()
    restaurants = service.get_restaurants(limit=50, offset=0)
    end_time = time.time()
    
    assert len(restaurants) == 50
    assert end_time - start_time < 1  # Should complete within 1 second
```

## Test Utilities

### Custom Assertions

```python
# tests/utils.py
def assert_restaurant_valid(restaurant_data, expected_data):
    """Custom assertion for restaurant data validation"""
    assert restaurant_data["name"] == expected_data["name"]
    assert restaurant_data["address"] == expected_data["address"]
    assert restaurant_data["phone"] == expected_data["phone"]
    assert restaurant_data["max_capacity"] == expected_data["max_capacity"]
    assert "id" in restaurant_data
    assert "created_at" in restaurant_data
    assert "updated_at" in restaurant_data

def assert_error_response(response, expected_status_code, expected_message=None):
    """Custom assertion for error responses"""
    assert response.status_code == expected_status_code
    data = response.json()
    assert "message" in data
    if expected_message:
        assert expected_message in data["message"]
```

### Test Data Builders

```python
# tests/builders.py
class RestaurantBuilder:
    def __init__(self):
        self.data = {
            "name": "Default Restaurant",
            "address": "123 Default St",
            "phone": "+1234567890",
            "opening_time": "09:00:00",
            "closing_time": "22:00:00",
            "max_capacity": 100
        }
    
    def with_name(self, name):
        self.data["name"] = name
        return self
    
    def with_capacity(self, capacity):
        self.data["max_capacity"] = capacity
        return self
    
    def build(self):
        return self.data.copy()

# Usage in tests
def test_restaurant_creation():
    restaurant_data = (RestaurantBuilder()
                      .with_name("Special Restaurant")
                      .with_capacity(200)
                      .build())
    
    # Use restaurant_data in test
    pass
```

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mariadb:
        image: mariadb:10.6
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: restaurant_seating_test
          MYSQL_USER: test_user
          MYSQL_PASSWORD: test_password
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: |
        pytest --cov=backend --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

## Test Best Practices

### 1. Test Naming

```python
# Good: Descriptive test names
def test_create_restaurant_with_valid_data_returns_201():
    pass

def test_create_restaurant_with_empty_name_returns_422():
    pass

def test_get_restaurant_by_id_returns_correct_data():
    pass

# Bad: Vague test names
def test_restaurant():
    pass

def test_api():
    pass
```

### 2. Test Organization

```python
class TestRestaurantAPI:
    """Group related tests in classes"""
    
    def test_create_restaurant_success(self):
        pass
    
    def test_create_restaurant_validation_error(self):
        pass
    
    def test_get_restaurant_success(self):
        pass
    
    def test_get_restaurant_not_found(self):
        pass
```

### 3. Test Data Management

```python
# Use fixtures for common data
@pytest.fixture
def valid_restaurant_data():
    return {
        "name": "Test Restaurant",
        "address": "123 Test St",
        "phone": "+1234567890",
        "opening_time": "09:00:00",
        "closing_time": "22:00:00",
        "max_capacity": 100
    }

# Use builders for complex data
def test_complex_scenario():
    restaurant = RestaurantBuilder().with_name("Complex").build()
    party = PartyBuilder().with_size(6).build()
    # ... test logic
```

### 4. Assertion Best Practices

```python
# Good: Specific assertions
def test_restaurant_creation():
    response = client.post("/api/v1/restaurants", json=data)
    
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == data["name"]
    assert result["id"] is not None
    assert "created_at" in result

# Bad: Generic assertions
def test_restaurant_creation():
    response = client.post("/api/v1/restaurants", json=data)
    assert response.status_code == 201  # Too generic
```

## Next Steps

- [Development Setup](setup.md)
- [API Documentation](../api/overview.md)
- [Deployment Guide](../deployment/overview.md)
