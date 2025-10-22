"""
Simplified pytest configuration and shared fixtures
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from datetime import datetime, date, time
import uuid
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Test database URL (in-memory SQLite for testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    # Import here to avoid circular imports
    from app.database.connection import Base
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    # Import here to avoid circular imports
    from app.main import app
    from app.database.connection import get_db
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_restaurant_data():
    """Sample restaurant data for testing."""
    return {
        "name": "Test Restaurant",
        "address": "123 Test Street, Test City, TC 12345",
        "phone": "+1-555-0123",
        "opening_time": "09:00:00",
        "closing_time": "22:00:00",
        "max_capacity": 100
    }


@pytest.fixture
def sample_restaurant(db_session: Session, sample_restaurant_data):
    """Create a sample restaurant in the database."""
    from app.models.database import Restaurant
    
    restaurant = Restaurant(**sample_restaurant_data)
    db_session.add(restaurant)
    db_session.commit()
    db_session.refresh(restaurant)
    return restaurant


@pytest.fixture
def sample_section_data(sample_restaurant):
    """Sample section data for testing."""
    return {
        "restaurant_id": sample_restaurant.id,
        "name": "Main Dining",
        "description": "Main dining area",
        "capacity": 50,
        "is_active": True
    }


@pytest.fixture
def sample_section(db_session: Session, sample_section_data):
    """Create a sample section in the database."""
    from app.models.database import Section
    
    section = Section(**sample_section_data)
    db_session.add(section)
    db_session.commit()
    db_session.refresh(section)
    return section


@pytest.fixture
def sample_table_data(sample_restaurant, sample_section):
    """Sample table data for testing."""
    return {
        "restaurant_id": sample_restaurant.id,
        "table_number": "T-01",
        "capacity": 4,
        "location": "Near window",
        "status": "AVAILABLE",
        "is_active": True
    }


@pytest.fixture
def sample_table(db_session: Session, sample_table_data):
    """Create a sample table in the database."""
    from app.models.database import Table
    
    table = Table(**sample_table_data)
    db_session.add(table)
    db_session.commit()
    db_session.refresh(table)
    return table


@pytest.fixture
def sample_party_data():
    """Sample party data for testing."""
    return {
        "name": "Test Party",
        "phone": "+1-555-0123",
        "email": "test@example.com",
        "size": 4,
        "status": "WAITING"
    }


@pytest.fixture
def sample_party(db_session: Session, sample_party_data):
    """Create a sample party in the database."""
    from app.models.database import Party
    
    party = Party(**sample_party_data)
    db_session.add(party)
    db_session.commit()
    db_session.refresh(party)
    return party


@pytest.fixture
def sample_reservation_data(sample_restaurant, sample_party):
    """Sample reservation data for testing."""
    return {
        "restaurant_id": sample_restaurant.id,
        "party_id": sample_party.id,
        "reservation_time": datetime(2025, 10, 20, 19, 0, 0),
        "party_size": 4,
        "customer_name": "Test Customer",
        "customer_phone": "+1-555-0123",
        "customer_email": "test@example.com",
        "status": "CONFIRMED",
        "special_requests": "Window table preferred"
    }


@pytest.fixture
def sample_reservation(db_session: Session, sample_reservation_data):
    """Create a sample reservation in the database."""
    from app.models.database import Reservation
    
    reservation = Reservation(**sample_reservation_data)
    db_session.add(reservation)
    db_session.commit()
    db_session.refresh(reservation)
    return reservation


@pytest.fixture
def sample_server_data(sample_restaurant):
    """Sample server data for testing."""
    return {
        "restaurant_id": sample_restaurant.id,
        "first_name": "John",
        "last_name": "Server",
        "employee_id": "EMP001",
        "phone": "+1-555-0199",
        "email": "john@test.com",
        "is_active": True
    }


@pytest.fixture
def sample_server(db_session: Session, sample_server_data):
    """Create a sample server in the database."""
    from app.models.database import Server
    
    server = Server(**sample_server_data)
    db_session.add(server)
    db_session.commit()
    db_session.refresh(server)
    return server
