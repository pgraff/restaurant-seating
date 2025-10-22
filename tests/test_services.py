"""
Unit tests for service layer functions
"""
import pytest
from datetime import datetime, date, time
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch

from app.services.restaurant_service import RestaurantService
from app.services.party_service import PartyService
from app.services.reservation_service import ReservationService
from app.services.server_service import ServerService
from app.services.assignment_service import AssignmentService
from app.models.database import (
    Restaurant, Section, Table, Party, Reservation, Server, TableAssignment
)


class TestRestaurantService:
    """Test RestaurantService functionality."""
    
    def test_get_restaurants(self, db_session: Session, sample_restaurant):
        """Test getting restaurants with pagination."""
        service = RestaurantService(db_session)
        
        # Test with default pagination
        restaurants = service.get_restaurants()
        assert len(restaurants) == 1
        assert restaurants[0].name == "Test Restaurant"
        
        # Test with custom pagination
        restaurants = service.get_restaurants(limit=10, offset=0)
        assert len(restaurants) == 1
        
        # Test with offset
        restaurants = service.get_restaurants(limit=10, offset=1)
        assert len(restaurants) == 0
    
    def test_create_restaurant(self, db_session: Session):
        """Test creating a new restaurant."""
        service = RestaurantService(db_session)
        
        from app.models.schemas import RestaurantCreate
        restaurant_data = RestaurantCreate(
            name="New Restaurant",
            address="456 New St",
            phone="+1-555-0456",
            opening_time="10:00:00",
            closing_time="23:00:00",
            max_capacity=150
        )
        
        restaurant = service.create_restaurant(restaurant_data)
        assert restaurant.name == "New Restaurant"
        assert restaurant.max_capacity == 150
        assert restaurant.id is not None
        
        # Verify it was saved to database
        db_restaurant = db_session.query(Restaurant).filter_by(name="New Restaurant").first()
        assert db_restaurant is not None
        assert db_restaurant.name == "New Restaurant"
    
    def test_get_restaurant(self, db_session: Session, sample_restaurant):
        """Test getting a specific restaurant."""
        service = RestaurantService(db_session)
        
        restaurant = service.get_restaurant(sample_restaurant.id)
        assert restaurant is not None
        assert restaurant.name == "Test Restaurant"
        
        # Test with non-existent ID
        restaurant = service.get_restaurant("non-existent-id")
        assert restaurant is None
    
    def test_update_restaurant(self, db_session: Session, sample_restaurant):
        """Test updating a restaurant."""
        service = RestaurantService(db_session)
        
        from app.models.schemas import RestaurantUpdate
        update_data = RestaurantUpdate(
            name="Updated Restaurant",
            max_capacity=200
        )
        
        updated_restaurant = service.update_restaurant(sample_restaurant.id, update_data)
        assert updated_restaurant.name == "Updated Restaurant"
        assert updated_restaurant.max_capacity == 200
        assert updated_restaurant.address == "123 Test Street, Test City, TC 12345"  # Unchanged
        
        # Verify it was updated in database
        db_restaurant = db_session.query(Restaurant).filter_by(id=sample_restaurant.id).first()
        assert db_restaurant.name == "Updated Restaurant"
        assert db_restaurant.max_capacity == 200
    
    def test_delete_restaurant(self, db_session: Session, sample_restaurant):
        """Test deleting a restaurant."""
        service = RestaurantService(db_session)
        
        # Verify restaurant exists
        restaurant = db_session.query(Restaurant).filter_by(id=sample_restaurant.id).first()
        assert restaurant is not None
        
        # Delete restaurant
        result = service.delete_restaurant(sample_restaurant.id)
        assert result is True
        
        # Verify restaurant was deleted
        restaurant = db_session.query(Restaurant).filter_by(id=sample_restaurant.id).first()
        assert restaurant is None
        
        # Test deleting non-existent restaurant
        result = service.delete_restaurant("non-existent-id")
        assert result is False


class TestPartyService:
    """Test PartyService functionality."""
    
    def test_get_parties(self, db_session: Session, sample_party):
        """Test getting parties with pagination."""
        service = PartyService(db_session)
        
        parties = service.get_parties()
        assert len(parties) == 1
        assert parties[0].name == "Test Party"
    
    def test_create_party(self, db_session: Session):
        """Test creating a new party."""
        service = PartyService(db_session)
        
        from app.models.schemas import PartyCreate
        party_data = PartyCreate(
            name="New Party",
            phone="+1-555-0456",
            email="new@example.com",
            size=6,
            status="WAITING"
        )
        
        party = service.create_party(party_data)
        assert party.name == "New Party"
        assert party.size == 6
        assert party.id is not None
    
    def test_get_party(self, db_session: Session, sample_party):
        """Test getting a specific party."""
        service = PartyService(db_session)
        
        party = service.get_party(sample_party.id)
        assert party is not None
        assert party.name == "Test Party"
        
        # Test with non-existent ID
        party = service.get_party("non-existent-id")
        assert party is None
    
    def test_update_party(self, db_session: Session, sample_party):
        """Test updating a party."""
        service = PartyService(db_session)
        
        from app.models.schemas import PartyUpdate
        update_data = PartyUpdate(
            name="Updated Party",
            size=8
        )
        
        updated_party = service.update_party(sample_party.id, update_data)
        assert updated_party.name == "Updated Party"
        assert updated_party.size == 8
        assert updated_party.phone == "+1-555-0123"  # Unchanged
    
    def test_delete_party(self, db_session: Session, sample_party):
        """Test deleting a party."""
        service = PartyService(db_session)
        
        result = service.delete_party(sample_party.id)
        assert result is True
        
        # Verify party was deleted
        party = db_session.query(Party).filter_by(id=sample_party.id).first()
        assert party is None


class TestReservationService:
    """Test ReservationService functionality."""
    
    def test_get_reservations(self, db_session: Session, sample_reservation):
        """Test getting reservations with pagination."""
        service = ReservationService(db_session)
        
        reservations = service.get_reservations()
        assert len(reservations) == 1
        assert reservations[0].customer_name == "Test Customer"
    
    def test_create_reservation(self, db_session: Session, sample_restaurant, sample_party):
        """Test creating a new reservation."""
        service = ReservationService(db_session)
        
        from app.models.schemas import ReservationCreate
        reservation_data = ReservationCreate(
            restaurant_id=sample_restaurant.id,
            reservation_time=datetime(2025, 10, 21, 20, 0, 0),
            party_size=4,
            customer_name="New Customer",
            customer_phone="+1-555-0456",
            customer_email="new@example.com",
            special_requests="Quiet table"
        )
        
        reservation = service.create_reservation(reservation_data)
        assert reservation.customer_name == "New Customer"
        assert reservation.party_size == 4
        assert reservation.id is not None
    
    def test_get_reservation(self, db_session: Session, sample_reservation):
        """Test getting a specific reservation."""
        service = ReservationService(db_session)
        
        reservation = service.get_reservation(sample_reservation.id)
        assert reservation is not None
        assert reservation.customer_name == "Test Customer"
        
        # Test with non-existent ID
        reservation = service.get_reservation("non-existent-id")
        assert reservation is None
    
    def test_update_reservation(self, db_session: Session, sample_reservation):
        """Test updating a reservation."""
        service = ReservationService(db_session)
        
        from app.models.schemas import ReservationUpdate
        update_data = ReservationUpdate(
            customer_name="Updated Customer",
            special_requests="Updated requests"
        )
        
        updated_reservation = service.update_reservation(sample_reservation.id, update_data)
        assert updated_reservation.customer_name == "Updated Customer"
        assert updated_reservation.special_requests == "Updated requests"
        assert updated_reservation.party_size == 4  # Unchanged
    
    def test_delete_reservation(self, db_session: Session, sample_reservation):
        """Test deleting a reservation."""
        service = ReservationService(db_session)
        
        result = service.delete_reservation(sample_reservation.id)
        assert result is True
        
        # Verify reservation was deleted
        reservation = db_session.query(Reservation).filter_by(id=sample_reservation.id).first()
        assert reservation is None


class TestServerService:
    """Test ServerService functionality."""
    
    def test_get_servers(self, db_session: Session, sample_server):
        """Test getting servers with pagination."""
        service = ServerService(db_session)
        
        servers = service.get_servers()
        assert len(servers) == 1
        assert servers[0].first_name == "John"
    
    def test_create_server(self, db_session: Session, sample_restaurant):
        """Test creating a new server."""
        service = ServerService(db_session)
        
        from app.models.schemas import ServerCreate
        server_data = ServerCreate(
            restaurant_id=sample_restaurant.id,
            first_name="Jane",
            last_name="Server",
            employee_id="EMP002",
            is_active=True
        )
        
        server = service.create_server(server_data)
        assert server.first_name == "Jane"
        assert server.employee_id == "EMP002"
        assert server.id is not None
    
    def test_get_server(self, db_session: Session, sample_server):
        """Test getting a specific server."""
        service = ServerService(db_session)
        
        server = service.get_server(sample_server.id)
        assert server is not None
        assert server.first_name == "John"
        
        # Test with non-existent ID
        server = service.get_server("non-existent-id")
        assert server is None
    
    def test_update_server(self, db_session: Session, sample_server):
        """Test updating a server."""
        service = ServerService(db_session)
        
        from app.models.schemas import ServerUpdate
        update_data = ServerUpdate(
            first_name="Johnny"
        )
        
        updated_server = service.update_server(sample_server.id, update_data)
        assert updated_server.first_name == "Johnny"
        assert updated_server.last_name == "Server"  # Unchanged
    
    def test_delete_server(self, db_session: Session, sample_server):
        """Test deleting a server."""
        service = ServerService(db_session)
        
        result = service.delete_server(sample_server.id)
        assert result is True
        
        # Verify server was deleted
        server = db_session.query(Server).filter_by(id=sample_server.id).first()
        assert server is None


class TestAssignmentService:
    """Test AssignmentService functionality."""
    
    def test_get_table_assignments(self, db_session: Session, sample_restaurant, sample_party, sample_table, sample_server):
        """Test getting table assignments."""
        service = AssignmentService(db_session)
        
        # Create a table assignment
        from app.models.schemas import TableAssignmentCreate
        assignment_data = TableAssignmentCreate(
            table_id=sample_table.id,
            party_id=sample_party.id,
            server_id=sample_server.id,
            assigned_at=datetime(2025, 10, 20, 19, 0, 0),
            status="ASSIGNED"
        )
        
        assignment = service.create_table_assignment(assignment_data)
        assert assignment.table_id == sample_table.id
        assert assignment.party_id == sample_party.id
        assert assignment.server_id == sample_server.id
        
        # Test getting assignments
        assignments = service.get_table_assignments()
        assert len(assignments) == 1
        assert assignments[0].table_id == sample_table.id
    
    def test_create_table_assignment(self, db_session: Session, sample_restaurant, sample_party, sample_table, sample_server):
        """Test creating a table assignment."""
        service = AssignmentService(db_session)
        
        from app.models.schemas import TableAssignmentCreate
        assignment_data = TableAssignmentCreate(
            table_id=sample_table.id,
            party_id=sample_party.id,
            server_id=sample_server.id,
            assigned_at=datetime(2025, 10, 20, 19, 0, 0),
            status="ASSIGNED"
        )
        
        assignment = service.create_table_assignment(assignment_data)
        assert assignment.table_id == sample_table.id
        assert assignment.party_id == sample_party.id
        assert assignment.status == "ACTIVE"  # Default status is ACTIVE
        assert assignment.id is not None
    
    def test_get_table_assignment(self, db_session: Session, sample_restaurant, sample_party, sample_table, sample_server):
        """Test getting a specific table assignment."""
        service = AssignmentService(db_session)
        
        # Create assignment first
        from app.models.schemas import TableAssignmentCreate
        assignment_data = TableAssignmentCreate(
            table_id=sample_table.id,
            party_id=sample_party.id,
            server_id=sample_server.id,
            assigned_at=datetime(2025, 10, 20, 19, 0, 0),
            status="ASSIGNED"
        )
        
        created_assignment = service.create_table_assignment(assignment_data)
        
        # Test getting the assignment
        assignment = service.get_table_assignment(created_assignment.id)
        assert assignment is not None
        assert assignment.table_id == sample_table.id
        
        # Test with non-existent ID
        assignment = service.get_table_assignment("non-existent-id")
        assert assignment is None
    
    def test_update_table_assignment(self, db_session: Session, sample_restaurant, sample_party, sample_table, sample_server):
        """Test updating a table assignment."""
        service = AssignmentService(db_session)
        
        # Create assignment first
        from app.models.schemas import TableAssignmentCreate
        assignment_data = TableAssignmentCreate(
            table_id=sample_table.id,
            party_id=sample_party.id,
            server_id=sample_server.id,
            assigned_at=datetime(2025, 10, 20, 19, 0, 0),
            status="ASSIGNED"
        )
        
        created_assignment = service.create_table_assignment(assignment_data)
        
        # Update assignment
        from app.models.schemas import TableAssignmentUpdate
        update_data = TableAssignmentUpdate(
            status="COMPLETED",
            notes="Service completed successfully"
        )
        
        updated_assignment = service.update_table_assignment(created_assignment.id, update_data)
        assert updated_assignment.status == "COMPLETED"
        assert updated_assignment.notes == "Service completed successfully"
    
    def test_delete_table_assignment(self, db_session: Session, sample_restaurant, sample_party, sample_table, sample_server):
        """Test deleting a table assignment."""
        service = AssignmentService(db_session)
        
        # Create assignment first
        from app.models.schemas import TableAssignmentCreate
        assignment_data = TableAssignmentCreate(
            table_id=sample_table.id,
            party_id=sample_party.id,
            server_id=sample_server.id,
            assigned_at=datetime(2025, 10, 20, 19, 0, 0),
            status="ASSIGNED"
        )
        
        created_assignment = service.create_table_assignment(assignment_data)
        
        # Delete assignment
        result = service.delete_table_assignment(created_assignment.id)
        assert result is True
        
        # Verify assignment was deleted
        assignment = db_session.query(TableAssignment).filter_by(id=created_assignment.id).first()
        assert assignment is None
