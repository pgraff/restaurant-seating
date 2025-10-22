"""
Unit tests for Pydantic models and SQLAlchemy models
"""
import pytest
import uuid
from datetime import datetime, date, time
from pydantic import ValidationError

from app.models.schemas import (
    Restaurant, RestaurantCreate, RestaurantUpdate,
    Section, SectionCreate, SectionUpdate,
    Table, TableCreate, TableUpdate,
    Party, PartyCreate, PartyUpdate,
    Reservation, ReservationCreate, ReservationUpdate,
    Server, ServerCreate, ServerUpdate,
    TableAssignment, TableAssignmentCreate, TableAssignmentUpdate,
    TableStatus, PartyStatus, ReservationStatus, AssignmentStatus
)
from app.models.database import (
    Restaurant as RestaurantModel,
    Section as SectionModel,
    Table as TableModel,
    Party as PartyModel,
    Reservation as ReservationModel,
    Server as ServerModel,
    TableAssignment as TableAssignmentModel
)


class TestPydanticModels:
    """Test Pydantic model validation and serialization."""
    
    def test_restaurant_create_validation(self):
        """Test RestaurantCreate model validation."""
        # Valid data
        valid_data = {
            "name": "Test Restaurant",
            "address": "123 Test St",
            "phone": "+1-555-0123",
            "opening_time": "09:00:00",
            "closing_time": "22:00:00",
            "max_capacity": 100
        }
        restaurant = RestaurantCreate(**valid_data)
        assert restaurant.name == "Test Restaurant"
        assert restaurant.max_capacity == 100
        
        # Invalid data - missing required field
        with pytest.raises(ValidationError):
            RestaurantCreate(name="Test Restaurant")
    
    def test_restaurant_update_validation(self):
        """Test RestaurantUpdate model validation."""
        # All fields optional
        update_data = {"name": "Updated Restaurant"}
        restaurant = RestaurantUpdate(**update_data)
        assert restaurant.name == "Updated Restaurant"
        assert restaurant.address is None
        
        # Empty update
        empty_update = RestaurantUpdate()
        assert empty_update.name is None
    
    def test_table_status_enum(self):
        """Test TableStatus enum values."""
        assert TableStatus.AVAILABLE == "AVAILABLE"
        assert TableStatus.OCCUPIED == "OCCUPIED"
        assert TableStatus.RESERVED == "RESERVED"
        assert TableStatus.OUT_OF_ORDER == "OUT_OF_ORDER"
        assert TableStatus.CLEANING == "CLEANING"
    
    def test_party_status_enum(self):
        """Test PartyStatus enum values."""
        assert PartyStatus.WAITING == "WAITING"
        assert PartyStatus.SEATED == "SEATED"
        assert PartyStatus.FINISHED == "FINISHED"
        assert PartyStatus.CANCELLED == "CANCELLED"
    
    def test_reservation_status_enum(self):
        """Test ReservationStatus enum values."""
        assert ReservationStatus.PENDING == "PENDING"
        assert ReservationStatus.CONFIRMED == "CONFIRMED"
        assert ReservationStatus.CANCELLED == "CANCELLED"
        assert ReservationStatus.NO_SHOW == "NO_SHOW"
        assert ReservationStatus.COMPLETED == "COMPLETED"
    
    def test_table_create_validation(self):
        """Test TableCreate model validation."""
        valid_data = {
            "restaurant_id": "123e4567-e89b-12d3-a456-426614174000",
            "table_number": "T-01",
            "capacity": 4,
            "location": "Near window",
            "status": "AVAILABLE"
        }
        table = TableCreate(**valid_data)
        assert table.table_number == "T-01"
        assert table.capacity == 4
        assert table.status == TableStatus.AVAILABLE
        
        # Invalid status
        with pytest.raises(ValidationError):
            TableCreate(
                restaurant_id="123e4567-e89b-12d3-a456-426614174000",
                table_number="T-01",
                capacity=4,
                location="Near window",
                status="INVALID_STATUS"
            )
    
    def test_party_create_validation(self):
        """Test PartyCreate model validation."""
        valid_data = {
            "name": "Test Party",
            "phone": "+1-555-0123",
            "email": "test@example.com",
            "size": 4,
            "status": "WAITING"
        }
        party = PartyCreate(**valid_data)
        assert party.name == "Test Party"
        assert party.size == 4
        assert party.status == PartyStatus.WAITING
    
    def test_reservation_create_validation(self):
        """Test ReservationCreate model validation."""
        valid_data = {
            "restaurant_id": "123e4567-e89b-12d3-a456-426614174000",
            "reservation_time": datetime(2025, 10, 20, 19, 0, 0),
            "party_size": 4,
            "customer_name": "Test Customer",
            "customer_phone": "+1-555-0123",
            "customer_email": "test@example.com",
            "special_requests": "Window table"
        }
        reservation = ReservationCreate(**valid_data)
        assert reservation.customer_name == "Test Customer"
        assert reservation.party_size == 4
        assert reservation.restaurant_id == "123e4567-e89b-12d3-a456-426614174000"
    
    def test_server_create_validation(self):
        """Test ServerCreate model validation."""
        valid_data = {
            "restaurant_id": "123e4567-e89b-12d3-a456-426614174000",
            "first_name": "John",
            "last_name": "Server",
            "employee_id": "EMP001",
            "phone": "+1-555-0199",
            "email": "john@test.com",
            "is_active": True
        }
        server = ServerCreate(**valid_data)
        assert server.first_name == "John"
        assert server.last_name == "Server"
        assert server.employee_id == "EMP001"
    
    def test_table_assignment_create_validation(self):
        """Test TableAssignmentCreate model validation."""
        valid_data = {
            "restaurant_id": "123e4567-e89b-12d3-a456-426614174000",
            "table_id": "123e4567-e89b-12d3-a456-426614174002",
            "party_id": "123e4567-e89b-12d3-a456-426614174001",
            "server_id": "123e4567-e89b-12d3-a456-426614174003",
            "assigned_at": datetime(2025, 10, 20, 19, 0, 0)
        }
        assignment = TableAssignmentCreate(**valid_data)
        assert assignment.table_id == "123e4567-e89b-12d3-a456-426614174002"
        assert assignment.party_id == "123e4567-e89b-12d3-a456-426614174001"


class TestSQLAlchemyModels:
    """Test SQLAlchemy model creation and relationships."""
    
    def test_restaurant_model_creation(self, db_session):
        """Test Restaurant model creation."""
        restaurant = RestaurantModel(
            name="Test Restaurant",
            address="123 Test St",
            phone="+1-555-0123",
            opening_time="09:00:00",
            closing_time="22:00:00",
            max_capacity=100
        )
        db_session.add(restaurant)
        db_session.commit()
        db_session.refresh(restaurant)
        
        assert restaurant.id is not None
        assert restaurant.name == "Test Restaurant"
        assert restaurant.max_capacity == 100
        assert restaurant.created_at is not None
        assert restaurant.updated_at is not None
    
    def test_section_model_creation(self, db_session, sample_restaurant):
        """Test Section model creation."""
        section = SectionModel(
            restaurant_id=sample_restaurant.id,
            name="Main Dining",
            description="Main dining area",
            capacity=50,
            is_active=True
        )
        db_session.add(section)
        db_session.commit()
        db_session.refresh(section)
        
        assert section.id is not None
        assert section.name == "Main Dining"
        assert section.restaurant_id == sample_restaurant.id
        assert section.is_active is True
    
    def test_table_model_creation(self, db_session, sample_restaurant):
        """Test Table model creation."""
        table = TableModel(
            restaurant_id=sample_restaurant.id,
            table_number="T-01",
            capacity=4,
            location="Near window",
            status="AVAILABLE",
            is_active=True
        )
        db_session.add(table)
        db_session.commit()
        db_session.refresh(table)
        
        assert table.id is not None
        assert table.table_number == "T-01"
        assert table.capacity == 4
        assert table.status == "AVAILABLE"
    
    def test_party_model_creation(self, db_session):
        """Test Party model creation."""
        party = PartyModel(
            name="Test Party",
            phone="+1-555-0123",
            email="test@example.com",
            size=4,
            status="WAITING"
        )
        db_session.add(party)
        db_session.commit()
        db_session.refresh(party)
        
        assert party.id is not None
        assert party.name == "Test Party"
        assert party.size == 4
        assert party.status == "WAITING"
        assert party.arrival_time is not None
    
    def test_reservation_model_creation(self, db_session, sample_restaurant, sample_party):
        """Test Reservation model creation."""
        reservation = ReservationModel(
            restaurant_id=sample_restaurant.id,
            party_id=sample_party.id,
            reservation_time=datetime(2025, 10, 20, 19, 0, 0),
            party_size=4,
            customer_name="Test Customer",
            customer_phone="+1-555-0123",
            customer_email="test@example.com",
            status="CONFIRMED",
            special_requests="Window table"
        )
        db_session.add(reservation)
        db_session.commit()
        db_session.refresh(reservation)
        
        assert reservation.id is not None
        assert reservation.customer_name == "Test Customer"
        assert reservation.party_size == 4
        assert reservation.status == "CONFIRMED"
    
    def test_server_model_creation(self, db_session, sample_restaurant):
        """Test Server model creation."""
        server = ServerModel(
            id=str(uuid.uuid4()),
            restaurant_id=sample_restaurant.id,
            first_name="John",
            last_name="Server",
            employee_id="EMP001",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(server)
        db_session.commit()
        db_session.refresh(server)
        
        assert server.id is not None
        assert server.first_name == "John"
        assert server.last_name == "Server"
        assert server.employee_id == "EMP001"
        assert server.is_active is True
    
    def test_table_assignment_model_creation(self, db_session, sample_restaurant, sample_party, sample_table, sample_server):
        """Test TableAssignment model creation."""
        assignment = TableAssignmentModel(
            id=str(uuid.uuid4()),
            table_id=sample_table.id,
            party_id=sample_party.id,
            server_id=sample_server.id,
            assigned_at=datetime(2025, 10, 20, 19, 0, 0),
            status="ACTIVE",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(assignment)
        db_session.commit()
        db_session.refresh(assignment)
        
        assert assignment.id is not None
        assert assignment.table_id == sample_table.id
        assert assignment.party_id == sample_party.id
        assert assignment.server_id == sample_server.id
        assert assignment.status == "ACTIVE"
    
    def test_model_relationships(self, db_session, sample_restaurant, sample_section, sample_table):
        """Test model relationships."""
        # Test restaurant -> sections relationship
        sections = db_session.query(SectionModel).filter_by(restaurant_id=sample_restaurant.id).all()
        assert len(sections) == 1
        assert sections[0].name == "Main Dining"
        
        # Test restaurant -> tables relationship
        tables = db_session.query(TableModel).filter_by(restaurant_id=sample_restaurant.id).all()
        assert len(tables) == 1
        assert tables[0].table_number == "T-01"
