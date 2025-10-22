"""
Unit tests for API endpoints
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestRestaurantAPI:
    """Test restaurant API endpoints."""
    
    def test_get_restaurants(self, client: TestClient, sample_restaurant):
        """Test GET /api/v1/restaurants/"""
        response = client.get("/api/v1/restaurants/")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Test Restaurant"
    
    def test_get_restaurants_pagination(self, client: TestClient, sample_restaurant):
        """Test GET /api/v1/restaurants/ with pagination parameters."""
        response = client.get("/api/v1/restaurants/?limit=1&offset=0")
        assert response.status_code == 200
        
        data = response.json()
        assert data["limit"] == 1
        assert data["offset"] == 0
        assert len(data["items"]) == 1
    
    def test_create_restaurant(self, client: TestClient):
        """Test POST /api/v1/restaurants/"""
        restaurant_data = {
            "name": "New Restaurant",
            "address": "456 New St",
            "phone": "+1-555-0456",
            "opening_time": "10:00:00",
            "closing_time": "23:00:00",
            "max_capacity": 150
        }
        
        response = client.post("/api/v1/restaurants/", json=restaurant_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == "New Restaurant"
        assert data["max_capacity"] == 150
        assert "id" in data
        assert "created_at" in data
    
    def test_create_restaurant_validation_error(self, client: TestClient):
        """Test POST /api/v1/restaurants/ with validation error."""
        invalid_data = {
            "name": "Test Restaurant"
            # Missing required fields
        }
        
        response = client.post("/api/v1/restaurants/", json=invalid_data)
        assert response.status_code == 422
        
        data = response.json()
        assert "message" in data
        assert data["message"] == "Validation error"
    
    def test_get_restaurant(self, client: TestClient, sample_restaurant):
        """Test GET /api/v1/restaurants/{restaurant_id}"""
        response = client.get(f"/api/v1/restaurants/{sample_restaurant.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Test Restaurant"
        assert data["id"] == sample_restaurant.id
    
    def test_get_restaurant_not_found(self, client: TestClient):
        """Test GET /api/v1/restaurants/{restaurant_id} with non-existent ID."""
        response = client.get("/api/v1/restaurants/non-existent-id")
        assert response.status_code == 404
    
    def test_update_restaurant(self, client: TestClient, sample_restaurant):
        """Test PUT /api/v1/restaurants/{restaurant_id}"""
        update_data = {
            "name": "Updated Restaurant",
            "max_capacity": 200
        }
        
        response = client.put(f"/api/v1/restaurants/{sample_restaurant.id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Updated Restaurant"
        assert data["max_capacity"] == 200
        assert data["address"] == "123 Test Street, Test City, TC 12345"  # Unchanged
    
    def test_delete_restaurant(self, client: TestClient, sample_restaurant):
        """Test DELETE /api/v1/restaurants/{restaurant_id}"""
        response = client.delete(f"/api/v1/restaurants/{sample_restaurant.id}")
        assert response.status_code == 204
        
        # Verify restaurant was deleted
        response = client.get(f"/api/v1/restaurants/{sample_restaurant.id}")
        assert response.status_code == 404


class TestSectionAPI:
    """Test section API endpoints."""
    
    def test_get_sections(self, client: TestClient, sample_restaurant, sample_section):
        """Test GET /api/v1/restaurants/{restaurant_id}/sections"""
        response = client.get(f"/api/v1/restaurants/{sample_restaurant.id}/sections")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Main Dining"
        assert data[0]["capacity"] == 50
    
    def test_create_section(self, client: TestClient, sample_restaurant):
        """Test POST /api/v1/restaurants/{restaurant_id}/sections"""
        section_data = {
            "restaurant_id": sample_restaurant.id,
            "name": "Patio",
            "description": "Outdoor seating",
            "capacity": 30
        }
        
        response = client.post(f"/api/v1/restaurants/{sample_restaurant.id}/sections", json=section_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == "Patio"
        assert data["capacity"] == 30
        assert data["restaurant_id"] == sample_restaurant.id
    
    def test_get_section(self, client: TestClient, sample_restaurant, sample_section):
        """Test GET /api/v1/restaurants/{restaurant_id}/sections/{section_id}"""
        response = client.get(f"/api/v1/restaurants/{sample_restaurant.id}/sections/{sample_section.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Main Dining"
        assert data["id"] == sample_section.id
    
    def test_update_section(self, client: TestClient, sample_restaurant, sample_section):
        """Test PUT /api/v1/restaurants/{restaurant_id}/sections/{section_id}"""
        update_data = {
            "name": "Updated Main Dining",
            "capacity": 60
        }
        
        response = client.put(f"/api/v1/restaurants/{sample_restaurant.id}/sections/{sample_section.id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Updated Main Dining"
        assert data["capacity"] == 60
    
    def test_delete_section(self, client: TestClient, sample_restaurant, sample_section):
        """Test DELETE /api/v1/restaurants/{restaurant_id}/sections/{section_id}"""
        response = client.delete(f"/api/v1/restaurants/{sample_restaurant.id}/sections/{sample_section.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Section deleted successfully"


class TestTableAPI:
    """Test table API endpoints."""
    
    def test_get_tables(self, client: TestClient, sample_restaurant, sample_table):
        """Test GET /api/v1/restaurants/{restaurant_id}/tables"""
        response = client.get(f"/api/v1/restaurants/{sample_restaurant.id}/tables")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["table_number"] == "T-01"
        assert data[0]["capacity"] == 4
    
    def test_create_table(self, client: TestClient, sample_restaurant):
        """Test POST /api/v1/restaurants/{restaurant_id}/tables"""
        table_data = {
            "restaurant_id": sample_restaurant.id,
            "table_number": "T-02",
            "capacity": 6,
            "location": "Corner table",
            "status": "AVAILABLE"
        }
        
        response = client.post(f"/api/v1/restaurants/{sample_restaurant.id}/tables", json=table_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["table_number"] == "T-02"
        assert data["capacity"] == 6
        assert data["status"] == "AVAILABLE"
    
    def test_get_table(self, client: TestClient, sample_restaurant, sample_table):
        """Test GET /api/v1/restaurants/{restaurant_id}/tables/{table_id}"""
        response = client.get(f"/api/v1/restaurants/{sample_restaurant.id}/tables/{sample_table.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["table_number"] == "T-01"
        assert data["id"] == sample_table.id
    
    def test_update_table(self, client: TestClient, sample_restaurant, sample_table):
        """Test PUT /api/v1/restaurants/{restaurant_id}/tables/{table_id}"""
        update_data = {
            "capacity": 8,
            "location": "Updated location"
        }
        
        response = client.put(f"/api/v1/restaurants/{sample_restaurant.id}/tables/{sample_table.id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["capacity"] == 8
        assert data["location"] == "Updated location"
    
    def test_delete_table(self, client: TestClient, sample_restaurant, sample_table):
        """Test DELETE /api/v1/restaurants/{restaurant_id}/tables/{table_id}"""
        response = client.delete(f"/api/v1/restaurants/{sample_restaurant.id}/tables/{sample_table.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Table deleted successfully"


class TestPartyAPI:
    """Test party API endpoints."""
    
    def test_get_parties(self, client: TestClient, sample_party):
        """Test GET /api/v1/parties/"""
        response = client.get("/api/v1/parties/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "Test Party"
    
    def test_create_party(self, client: TestClient):
        """Test POST /api/v1/parties/"""
        party_data = {
            "name": "New Party",
            "phone": "+1-555-0456",
            "email": "new@example.com",
            "size": 6,
            "status": "WAITING"
        }
        
        response = client.post("/api/v1/parties/", json=party_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == "New Party"
        assert data["size"] == 6
        assert data["status"] == "WAITING"
    
    def test_get_party(self, client: TestClient, sample_party):
        """Test GET /api/v1/parties/{party_id}"""
        response = client.get(f"/api/v1/parties/{sample_party.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Test Party"
        assert data["id"] == sample_party.id
    
    def test_update_party(self, client: TestClient, sample_party):
        """Test PUT /api/v1/parties/{party_id}"""
        update_data = {
            "name": "Updated Party",
            "size": 8
        }
        
        response = client.put(f"/api/v1/parties/{sample_party.id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Updated Party"
        assert data["size"] == 8
    
    def test_delete_party(self, client: TestClient, sample_party):
        """Test DELETE /api/v1/parties/{party_id}"""
        response = client.delete(f"/api/v1/parties/{sample_party.id}")
        assert response.status_code == 204


class TestReservationAPI:
    """Test reservation API endpoints."""
    
    def test_get_reservations(self, client: TestClient, sample_reservation):
        """Test GET /api/v1/reservations/"""
        response = client.get("/api/v1/reservations/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["customer_name"] == "Test Customer"
    
    def test_create_reservation(self, client: TestClient, sample_restaurant, sample_party):
        """Test POST /api/v1/reservations/"""
        reservation_data = {
            "restaurant_id": sample_restaurant.id,
            "party_id": sample_party.id,
            "reservation_time": "2025-10-21T20:00:00",
            "party_size": 4,
            "customer_name": "New Customer",
            "customer_phone": "+1-555-0456",
            "customer_email": "new@example.com",
            "status": "CONFIRMED",
            "special_requests": "Quiet table"
        }
        
        response = client.post("/api/v1/reservations/", json=reservation_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["customer_name"] == "New Customer"
        assert data["party_size"] == 4
        assert data["status"] == "CONFIRMED"
    
    def test_get_reservation(self, client: TestClient, sample_reservation):
        """Test GET /api/v1/reservations/{reservation_id}"""
        response = client.get(f"/api/v1/reservations/{sample_reservation.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["customer_name"] == "Test Customer"
        assert data["id"] == sample_reservation.id
    
    def test_update_reservation(self, client: TestClient, sample_reservation):
        """Test PUT /api/v1/reservations/{reservation_id}"""
        update_data = {
            "customer_name": "Updated Customer",
            "special_requests": "Updated requests"
        }
        
        response = client.put(f"/api/v1/reservations/{sample_reservation.id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["customer_name"] == "Updated Customer"
        assert data["special_requests"] == "Updated requests"
    
    def test_delete_reservation(self, client: TestClient, sample_reservation):
        """Test DELETE /api/v1/reservations/{reservation_id}"""
        response = client.delete(f"/api/v1/reservations/{sample_reservation.id}")
        assert response.status_code == 204


class TestServerAPI:
    """Test server API endpoints."""
    
    def test_get_servers(self, client: TestClient, sample_server):
        """Test GET /api/v1/servers/"""
        response = client.get("/api/v1/servers/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["first_name"] == "John"
    
    def test_create_server(self, client: TestClient, sample_restaurant):
        """Test POST /api/v1/servers/"""
        server_data = {
            "restaurant_id": sample_restaurant.id,
            "first_name": "Jane",
            "last_name": "Server",
            "employee_id": "EMP002",
            "is_active": True
        }
        
        response = client.post("/api/v1/servers/", json=server_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["first_name"] == "Jane"
        assert data["employee_id"] == "EMP002"
    
    def test_get_server(self, client: TestClient, sample_server):
        """Test GET /api/v1/servers/{server_id}"""
        response = client.get(f"/api/v1/servers/{sample_server.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["first_name"] == "John"
        assert data["id"] == sample_server.id
    
    def test_update_server(self, client: TestClient, sample_server):
        """Test PUT /api/v1/servers/{server_id}"""
        update_data = {
            "first_name": "Johnny"
        }
        
        response = client.put(f"/api/v1/servers/{sample_server.id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["first_name"] == "Johnny"
    
    def test_delete_server(self, client: TestClient, sample_server):
        """Test DELETE /api/v1/servers/{server_id}"""
        response = client.delete(f"/api/v1/servers/{sample_server.id}")
        assert response.status_code == 204


class TestAssignmentAPI:
    """Test assignment API endpoints."""
    
    def test_get_table_assignments(self, client: TestClient, sample_restaurant, sample_party, sample_table, sample_server):
        """Test GET /api/v1/assignments/table-assignments/"""
        # First create an assignment
        assignment_data = {
            "restaurant_id": sample_restaurant.id,
            "table_id": sample_table.id,
            "party_id": sample_party.id,
            "server_id": sample_server.id,
            "assigned_at": "2025-10-20T19:00:00",
            "status": "ASSIGNED"
        }
        
        create_response = client.post("/api/v1/assignments/table-assignments", json=assignment_data)
        assert create_response.status_code == 201
        
        # Now test getting assignments
        response = client.get("/api/v1/assignments/table-assignments/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["table_id"] == sample_table.id
    
    def test_create_table_assignment(self, client: TestClient, sample_restaurant, sample_party, sample_table, sample_server):
        """Test POST /api/v1/assignments/table-assignments"""
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
        
        data = response.json()
        assert data["table_id"] == sample_table.id
        assert data["party_id"] == sample_party.id
        assert data["server_id"] == sample_server.id
        assert data["status"] == "ASSIGNED"
    
    def test_get_table_assignment(self, client: TestClient, sample_restaurant, sample_party, sample_table, sample_server):
        """Test GET /api/v1/assignments/table-assignments/{assignment_id}"""
        # First create an assignment
        assignment_data = {
            "restaurant_id": sample_restaurant.id,
            "table_id": sample_table.id,
            "party_id": sample_party.id,
            "server_id": sample_server.id,
            "assigned_at": "2025-10-20T19:00:00",
            "status": "ASSIGNED"
        }
        
        create_response = client.post("/api/v1/assignments/table-assignments", json=assignment_data)
        assignment_id = create_response.json()["id"]
        
        # Now test getting the assignment
        response = client.get(f"/api/v1/assignments/table-assignments/{assignment_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["table_id"] == sample_table.id
        assert data["id"] == assignment_id
    
    def test_update_table_assignment(self, client: TestClient, sample_restaurant, sample_party, sample_table, sample_server):
        """Test PUT /api/v1/assignments/table-assignments/{assignment_id}"""
        # First create an assignment
        assignment_data = {
            "restaurant_id": sample_restaurant.id,
            "table_id": sample_table.id,
            "party_id": sample_party.id,
            "server_id": sample_server.id,
            "assigned_at": "2025-10-20T19:00:00",
            "status": "ASSIGNED"
        }
        
        create_response = client.post("/api/v1/assignments/table-assignments", json=assignment_data)
        assignment_id = create_response.json()["id"]
        
        # Now test updating the assignment
        update_data = {
            "status": "COMPLETED",
            "notes": "Service completed successfully"
        }
        
        response = client.put(f"/api/v1/assignments/table-assignments/{assignment_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "COMPLETED"
        assert data["notes"] == "Service completed successfully"
    
    def test_delete_table_assignment(self, client: TestClient, sample_restaurant, sample_party, sample_table, sample_server):
        """Test DELETE /api/v1/assignments/table-assignments/{assignment_id}"""
        # First create an assignment
        assignment_data = {
            "restaurant_id": sample_restaurant.id,
            "table_id": sample_table.id,
            "party_id": sample_party.id,
            "server_id": sample_server.id,
            "assigned_at": "2025-10-20T19:00:00",
            "status": "ASSIGNED"
        }
        
        create_response = client.post("/api/v1/assignments/table-assignments", json=assignment_data)
        assignment_id = create_response.json()["id"]
        
        # Now test deleting the assignment
        response = client.delete(f"/api/v1/assignments/table-assignments/{assignment_id}")
        assert response.status_code == 204


class TestHealthEndpoints:
    """Test health and utility endpoints."""
    
    def test_health_check(self, client: TestClient):
        """Test GET /health"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
    
    def test_root_endpoint(self, client: TestClient):
        """Test GET /"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "timestamp" in data
