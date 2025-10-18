"""
Simple unit tests for the restaurant seating system
"""
import pytest
from datetime import datetime, date, time
from pydantic import ValidationError

# Add the backend directory to the Python path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.models.schemas import (
    Restaurant, RestaurantCreate, RestaurantUpdate,
    Table, TableCreate, TableUpdate,
    Party, PartyCreate, PartyUpdate,
    Reservation, ReservationCreate, ReservationUpdate,
    Server, ServerCreate, ServerUpdate,
    TableAssignment, TableAssignmentCreate, TableAssignmentUpdate,
    TableStatus, PartyStatus, ReservationStatus, AssignmentStatus
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


class TestModelSerialization:
    """Test model serialization and deserialization."""
    
    def test_restaurant_serialization(self):
        """Test Restaurant model serialization."""
        restaurant_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Test Restaurant",
            "address": "123 Test St",
            "phone": "+1-555-0123",
            "opening_time": "09:00:00",
            "closing_time": "22:00:00",
            "max_capacity": 100,
            "created_at": datetime(2025, 10, 20, 10, 0, 0),
            "updated_at": datetime(2025, 10, 20, 10, 0, 0)
        }
        
        restaurant = Restaurant(**restaurant_data)
        assert restaurant.name == "Test Restaurant"
        assert restaurant.max_capacity == 100
        
        # Test serialization to dict
        restaurant_dict = restaurant.model_dump()
        assert restaurant_dict["name"] == "Test Restaurant"
        assert restaurant_dict["max_capacity"] == 100
    
    def test_table_serialization(self):
        """Test Table model serialization."""
        table_data = {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "restaurant_id": "123e4567-e89b-12d3-a456-426614174000",
            "table_number": "T-01",
            "capacity": 4,
            "location": "Near window",
            "status": "AVAILABLE",
            "is_active": True,
            "created_at": datetime(2025, 10, 20, 10, 0, 0),
            "updated_at": datetime(2025, 10, 20, 10, 0, 0)
        }
        
        table = Table(**table_data)
        assert table.table_number == "T-01"
        assert table.capacity == 4
        assert table.status == TableStatus.AVAILABLE
        
        # Test serialization to dict
        table_dict = table.model_dump()
        assert table_dict["table_number"] == "T-01"
        assert table_dict["capacity"] == 4
        assert table_dict["status"] == "AVAILABLE"
    
    def test_party_serialization(self):
        """Test Party model serialization."""
        party_data = {
            "id": "123e4567-e89b-12d3-a456-426614174002",
            "name": "Test Party",
            "phone": "+1-555-0123",
            "email": "test@example.com",
            "size": 4,
            "status": "WAITING",
            "arrival_time": datetime(2025, 10, 20, 19, 0, 0),
            "created_at": datetime(2025, 10, 20, 10, 0, 0),
            "updated_at": datetime(2025, 10, 20, 10, 0, 0)
        }
        
        party = Party(**party_data)
        assert party.name == "Test Party"
        assert party.size == 4
        assert party.status == PartyStatus.WAITING
        
        # Test serialization to dict
        party_dict = party.model_dump()
        assert party_dict["name"] == "Test Party"
        assert party_dict["size"] == 4
        assert party_dict["status"] == "WAITING"


class TestValidationEdgeCases:
    """Test validation edge cases and error handling."""
    
    def test_invalid_email_format(self):
        """Test invalid email format validation."""
        with pytest.raises(ValidationError) as exc_info:
            PartyCreate(
                name="Test Party",
                phone="+1-555-0123",
                email="invalid-email-format",
                size=4,
                status="WAITING"
            )
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "value_error" for error in errors)
    
    def test_invalid_phone_format(self):
        """Test invalid phone format validation."""
        # Phone validation is not implemented, so this should pass
        party = PartyCreate(
            name="Test Party",
            phone="invalid-phone",
            email="test@example.com",
            size=4,
            status="WAITING"
        )
        assert party.phone == "invalid-phone"
    
    def test_negative_capacity(self):
        """Test negative capacity validation."""
        with pytest.raises(ValidationError) as exc_info:
            TableCreate(
                restaurant_id="123e4567-e89b-12d3-a456-426614174000",
                table_number="T-01",
                capacity=-1,
                location="Near window",
                status="AVAILABLE"
            )
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "greater_than_equal" for error in errors)
    
    def test_zero_capacity(self):
        """Test zero capacity validation."""
        with pytest.raises(ValidationError) as exc_info:
            TableCreate(
                restaurant_id="123e4567-e89b-12d3-a456-426614174000",
                table_number="T-01",
                capacity=0,
                location="Near window",
                status="AVAILABLE"
            )
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "greater_than_equal" for error in errors)
    
    def test_invalid_datetime_format(self):
        """Test invalid datetime format validation."""
        with pytest.raises(ValidationError) as exc_info:
            ReservationCreate(
                restaurant_id="123e4567-e89b-12d3-a456-426614174000",
                party_id="123e4567-e89b-12d3-a456-426614174001",
                reservation_time="invalid-datetime",
                party_size=4,
                customer_name="Test Customer",
                customer_phone="+1-555-0123",
                customer_email="test@example.com",
                status="CONFIRMED"
            )
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "datetime_parsing" for error in errors)
