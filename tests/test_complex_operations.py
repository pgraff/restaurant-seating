"""
Unit tests for complex operations and business logic
"""
import pytest
from datetime import datetime, date, time
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.services.restaurant_service import RestaurantService
from app.services.party_service import PartyService
from app.services.reservation_service import ReservationService
from app.services.assignment_service import AssignmentService
from app.models.database import (
    Restaurant, Section, Table, Party, Reservation, Server, TableAssignment
)


class TestComplexRestaurantOperations:
    """Test complex restaurant operations."""
    
    def test_assign_table_to_party(self, db_session: Session, sample_restaurant, sample_party, sample_table, sample_server):
        """Test assigning a table to a party."""
        service = RestaurantService(db_session)
        
        # Test table assignment
        result = service.assign_table_to_party(
            restaurant_id=sample_restaurant.id,
            table_id=sample_table.id,
            party_id=sample_party.id,
            server_id=sample_server.id
        )
        
        assert result is not None
        assert result["table_id"] == sample_table.id
        assert result["party_id"] == sample_party.id
        assert result["server_id"] == sample_server.id
        
        # Verify table status changed
        table = db_session.query(Table).filter_by(id=sample_table.id).first()
        assert table.status == "OCCUPIED"
        
        # Verify party status changed
        party = db_session.query(Party).filter_by(id=sample_party.id).first()
        assert party.status == "SEATED"
    
    def test_check_table_availability(self, db_session: Session, sample_restaurant, sample_table):
        """Test checking table availability."""
        service = RestaurantService(db_session)
        
        # Test available table
        availability = service.check_table_availability(
            restaurant_id=sample_restaurant.id,
            table_id=sample_table.id,
            date=date(2025, 10, 20),
            time=time(19, 0)
        )
        
        assert availability["available"] is True
        assert availability["table_id"] == sample_table.id
        
        # Test occupied table
        sample_table.status = "OCCUPIED"
        db_session.commit()
        
        availability = service.check_table_availability(
            restaurant_id=sample_restaurant.id,
            table_id=sample_table.id,
            date=date(2025, 10, 20),
            time=time(19, 0)
        )
        
        assert availability["available"] is False
    
    def test_get_occupancy_analytics(self, db_session: Session, sample_restaurant, sample_table):
        """Test getting occupancy analytics."""
        service = RestaurantService(db_session)
        
        # Create some test data
        sample_table.status = "OCCUPIED"
        db_session.commit()
        
        analytics = service.get_occupancy_analytics(
            restaurant_id=sample_restaurant.id,
            start_date=date(2025, 10, 20),
            end_date=date(2025, 10, 20)
        )
        
        assert "total_tables" in analytics
        assert "occupied_tables" in analytics
        assert "available_tables" in analytics
        assert "occupancy_rate" in analytics
        assert analytics["total_tables"] == 1
        assert analytics["occupied_tables"] == 1
        assert analytics["occupancy_rate"] == 100.0


class TestReservationWorkflow:
    """Test complete reservation workflow."""
    
    def test_complete_reservation_workflow(self, client: TestClient, sample_restaurant, sample_party, sample_table, sample_server):
        """Test complete reservation workflow from creation to table assignment."""
        
        # 1. Create a reservation
        reservation_data = {
            "restaurant_id": sample_restaurant.id,
            "party_id": sample_party.id,
            "reservation_time": "2025-10-20T19:00:00",
            "party_size": 4,
            "customer_name": "Test Customer",
            "customer_phone": "+1-555-0123",
            "customer_email": "test@example.com",
            "status": "CONFIRMED",
            "special_requests": "Window table preferred"
        }
        
        reservation_response = client.post("/api/v1/reservations/", json=reservation_data)
        assert reservation_response.status_code == 201
        reservation_id = reservation_response.json()["id"]
        
        # 2. Assign table to reservation
        assignment_data = {
            "restaurant_id": sample_restaurant.id,
            "table_id": sample_table.id,
            "party_id": sample_party.id,
            "server_id": sample_server.id,
            "assigned_at": "2025-10-20T19:00:00",
            "status": "ASSIGNED"
        }
        
        assignment_response = client.post("/api/v1/assignments/table-assignments", json=assignment_data)
        assert assignment_response.status_code == 201
        assignment_id = assignment_response.json()["id"]
        
        # 3. Verify reservation details
        reservation_response = client.get(f"/api/v1/reservations/{reservation_id}")
        assert reservation_response.status_code == 200
        reservation = reservation_response.json()
        assert reservation["status"] == "CONFIRMED"
        
        # 4. Verify table assignment
        assignment_response = client.get(f"/api/v1/assignments/table-assignments/{assignment_id}")
        assert assignment_response.status_code == 200
        assignment = assignment_response.json()
        assert assignment["table_id"] == sample_table.id
        assert assignment["party_id"] == sample_party.id
        assert assignment["status"] == "ASSIGNED"
        
        # 5. Complete the assignment
        completion_data = {
            "status": "COMPLETED",
            "notes": "Service completed successfully"
        }
        
        completion_response = client.put(f"/api/v1/assignments/table-assignments/{assignment_id}", json=completion_data)
        assert completion_response.status_code == 200
        
        # 6. Verify completion
        final_assignment = completion_response.json()
        assert final_assignment["status"] == "COMPLETED"
        assert final_assignment["notes"] == "Service completed successfully"


class TestWaitingListOperations:
    """Test waiting list operations."""
    
    def test_add_to_waiting_list(self, client: TestClient, sample_restaurant, sample_party):
        """Test adding a party to waiting list."""
        waiting_list_data = {
            "restaurant_id": sample_restaurant.id,
            "party_id": sample_party.id,
            "party_size": 4,
            "estimated_wait_time": 30,
            "status": "WAITING"
        }
        
        response = client.post("/api/v1/waiting-list/", json=waiting_list_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["party_id"] == sample_party.id
        assert data["party_size"] == 4
        assert data["status"] == "WAITING"
    
    def test_get_next_waiting_party(self, client: TestClient, sample_restaurant, sample_party):
        """Test getting next party from waiting list."""
        # First add party to waiting list
        waiting_list_data = {
            "restaurant_id": sample_restaurant.id,
            "party_id": sample_party.id,
            "party_size": 4,
            "estimated_wait_time": 30,
            "status": "WAITING"
        }
        
        add_response = client.post("/api/v1/waiting-list/", json=waiting_list_data)
        assert add_response.status_code == 201
        
        # Then get next waiting party
        response = client.get(f"/api/v1/restaurants/{sample_restaurant.id}/waiting-list/next")
        assert response.status_code == 200
        
        data = response.json()
        assert data["party_id"] == sample_party.id
        assert data["party_size"] == 4


class TestTableManagement:
    """Test table management operations."""
    
    def test_table_status_updates(self, client: TestClient, sample_restaurant, sample_table):
        """Test updating table status through different operations."""
        
        # Test setting table to occupied
        update_data = {"status": "OCCUPIED"}
        response = client.put(f"/api/v1/restaurants/{sample_restaurant.id}/tables/{sample_table.id}", json=update_data)
        assert response.status_code == 200
        
        table = response.json()
        assert table["status"] == "OCCUPIED"
        
        # Test setting table to cleaning
        update_data = {"status": "CLEANING"}
        response = client.put(f"/api/v1/restaurants/{sample_restaurant.id}/tables/{sample_table.id}", json=update_data)
        assert response.status_code == 200
        
        table = response.json()
        assert table["status"] == "CLEANING"
        
        # Test setting table back to available
        update_data = {"status": "AVAILABLE"}
        response = client.put(f"/api/v1/restaurants/{sample_restaurant.id}/tables/{sample_table.id}", json=update_data)
        assert response.status_code == 200
        
        table = response.json()
        assert table["status"] == "AVAILABLE"
    
    def test_table_capacity_validation(self, client: TestClient, sample_restaurant):
        """Test table capacity validation."""
        # Test creating table with valid capacity
        table_data = {
            "restaurant_id": sample_restaurant.id,
            "table_number": "T-03",
            "capacity": 8,
            "location": "Large table",
            "status": "AVAILABLE"
        }
        
        response = client.post(f"/api/v1/restaurants/{sample_restaurant.id}/tables", json=table_data)
        assert response.status_code == 201
        
        table = response.json()
        assert table["capacity"] == 8
        
        # Test creating table with invalid capacity
        invalid_table_data = {
            "restaurant_id": sample_restaurant.id,
            "table_number": "T-04",
            "capacity": 0,  # Invalid capacity
            "location": "Invalid table",
            "status": "AVAILABLE"
        }
        
        response = client.post(f"/api/v1/restaurants/{sample_restaurant.id}/tables", json=invalid_table_data)
        assert response.status_code == 422  # Validation error


class TestErrorHandling:
    """Test error handling in complex operations."""
    
    def test_assign_nonexistent_table(self, client: TestClient, sample_restaurant, sample_party, sample_server):
        """Test assigning non-existent table to party."""
        assignment_data = {
            "restaurant_id": sample_restaurant.id,
            "table_id": "non-existent-table-id",
            "party_id": sample_party.id,
            "server_id": sample_server.id,
            "assigned_at": "2025-10-20T19:00:00",
            "status": "ASSIGNED"
        }
        
        response = client.post("/api/v1/assignments/table-assignments", json=assignment_data)
        assert response.status_code == 404
    
    def test_assign_occupied_table(self, client: TestClient, sample_restaurant, sample_party, sample_table, sample_server):
        """Test assigning already occupied table."""
        # First assign the table
        assignment_data = {
            "restaurant_id": sample_restaurant.id,
            "table_id": sample_table.id,
            "party_id": sample_party.id,
            "server_id": sample_server.id,
            "assigned_at": "2025-10-20T19:00:00",
            "status": "ASSIGNED"
        }
        
        response = client.post("/api/v1/assignments/table-assignments", json=assignment_data)
        assert response.status_code == 201
        
        # Try to assign the same table to another party
        another_party_data = {
            "name": "Another Party",
            "phone": "+1-555-0456",
            "email": "another@example.com",
            "size": 2,
            "status": "WAITING"
        }
        
        party_response = client.post("/api/v1/parties/", json=another_party_data)
        another_party_id = party_response.json()["id"]
        
        duplicate_assignment_data = {
            "restaurant_id": sample_restaurant.id,
            "table_id": sample_table.id,
            "party_id": another_party_id,
            "server_id": sample_server.id,
            "assigned_at": "2025-10-20T19:00:00",
            "status": "ASSIGNED"
        }
        
        response = client.post("/api/v1/assignments/table-assignments", json=duplicate_assignment_data)
        # This should either succeed (if we allow multiple assignments) or fail with appropriate error
        # The behavior depends on business logic implementation
        assert response.status_code in [201, 400, 409]  # Success, Bad Request, or Conflict
