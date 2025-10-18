"""
API Client for communicating with the Restaurant Seating System backend
"""

import requests
import json
from typing import List, Dict, Optional, Any
from datetime import datetime, date
import streamlit as st

class RestaurantAPIClient:
    """Client for interacting with the Restaurant Seating System API"""
    
    def __init__(self, base_url: str = "http://fastapi:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Make HTTP request to API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return {}
    
    # Restaurant operations
    def get_restaurants(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Get list of restaurants"""
        response = self._make_request("GET", "/restaurants", params={"limit": limit, "offset": offset})
        return response.get("items", [])
    
    def get_restaurant(self, restaurant_id: str) -> Optional[Dict]:
        """Get restaurant by ID"""
        return self._make_request("GET", f"/restaurants/{restaurant_id}")
    
    def create_restaurant(self, restaurant_data: Dict) -> Optional[Dict]:
        """Create new restaurant"""
        return self._make_request("POST", "/restaurants", data=restaurant_data)
    
    def update_restaurant(self, restaurant_id: str, restaurant_data: Dict) -> Optional[Dict]:
        """Update restaurant"""
        return self._make_request("PUT", f"/restaurants/{restaurant_id}", data=restaurant_data)
    
    def delete_restaurant(self, restaurant_id: str) -> bool:
        """Delete restaurant"""
        response = self._make_request("DELETE", f"/restaurants/{restaurant_id}")
        return response is not None
    
    # Section operations
    def get_sections(self, restaurant_id: str) -> List[Dict]:
        """Get sections for a restaurant"""
        return self._make_request("GET", f"/restaurants/{restaurant_id}/sections")
    
    def create_section(self, restaurant_id: str, section_data: Dict) -> Optional[Dict]:
        """Create new section"""
        return self._make_request("POST", f"/restaurants/{restaurant_id}/sections", data=section_data)
    
    def update_section(self, section_id: str, section_data: Dict) -> Optional[Dict]:
        """Update section"""
        return self._make_request("PUT", f"/sections/{section_id}", data=section_data)
    
    def delete_section(self, section_id: str) -> bool:
        """Delete section"""
        response = self._make_request("DELETE", f"/sections/{section_id}")
        return response is not None
    
    # Table operations
    def get_tables(self, restaurant_id: str, section_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """Get tables for a restaurant"""
        params = {}
        if section_id:
            params["section_id"] = section_id
        if status:
            params["status"] = status
        return self._make_request("GET", f"/restaurants/{restaurant_id}/tables", params=params)
    
    def create_table(self, restaurant_id: str, table_data: Dict) -> Optional[Dict]:
        """Create new table"""
        return self._make_request("POST", f"/restaurants/{restaurant_id}/tables", data=table_data)
    
    def update_table(self, table_id: str, table_data: Dict) -> Optional[Dict]:
        """Update table"""
        return self._make_request("PUT", f"/tables/{table_id}", data=table_data)
    
    def delete_table(self, table_id: str) -> bool:
        """Delete table"""
        response = self._make_request("DELETE", f"/tables/{table_id}")
        return response is not None
    
    # Server operations
    def get_servers(self, restaurant_id: Optional[str] = None, is_active: Optional[bool] = None) -> List[Dict]:
        """Get servers"""
        params = {}
        if restaurant_id:
            params["restaurant_id"] = restaurant_id
        if is_active is not None:
            params["is_active"] = is_active
        return self._make_request("GET", "/servers", params=params)
    
    def create_server(self, server_data: Dict) -> Optional[Dict]:
        """Create new server"""
        return self._make_request("POST", "/servers", data=server_data)
    
    def update_server(self, server_id: str, server_data: Dict) -> Optional[Dict]:
        """Update server"""
        return self._make_request("PUT", f"/servers/{server_id}", data=server_data)
    
    def delete_server(self, server_id: str) -> bool:
        """Delete server"""
        response = self._make_request("DELETE", f"/servers/{server_id}")
        return response is not None
    
    # Reservation operations
    def get_reservations(self, restaurant_id: Optional[str] = None, status: Optional[str] = None, 
                        date_filter: Optional[date] = None) -> List[Dict]:
        """Get reservations"""
        params = {}
        if restaurant_id:
            params["restaurant_id"] = restaurant_id
        if status:
            params["status"] = status
        if date_filter:
            params["date"] = date_filter.isoformat()
        return self._make_request("GET", "/reservations", params=params)
    
    def create_reservation(self, reservation_data: Dict) -> Optional[Dict]:
        """Create new reservation"""
        return self._make_request("POST", "/reservations", data=reservation_data)
    
    def update_reservation(self, reservation_id: str, reservation_data: Dict) -> Optional[Dict]:
        """Update reservation"""
        return self._make_request("PUT", f"/reservations/{reservation_id}", data=reservation_data)
    
    def cancel_reservation(self, reservation_id: str) -> Optional[Dict]:
        """Cancel reservation"""
        return self._make_request("DELETE", f"/reservations/{reservation_id}")
    
    # Party operations
    def get_parties(self, status: Optional[str] = None) -> List[Dict]:
        """Get parties"""
        params = {}
        if status:
            params["status"] = status
        return self._make_request("GET", "/parties", params=params)
    
    def create_party(self, party_data: Dict) -> Optional[Dict]:
        """Create new party"""
        return self._make_request("POST", "/parties", data=party_data)
    
    def update_party(self, party_id: str, party_data: Dict) -> Optional[Dict]:
        """Update party"""
        return self._make_request("PUT", f"/parties/{party_id}", data=party_data)
    
    def delete_party(self, party_id: str) -> bool:
        """Delete party"""
        response = self._make_request("DELETE", f"/parties/{party_id}")
        return response is not None
    
    # Waiting list operations
    def get_waiting_list(self, restaurant_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """Get waiting list entries"""
        params = {}
        if restaurant_id:
            params["restaurant_id"] = restaurant_id
        if status:
            params["status"] = status
        return self._make_request("GET", "/waiting-list", params=params)
    
    def add_to_waiting_list(self, waiting_list_data: Dict) -> Optional[Dict]:
        """Add party to waiting list"""
        return self._make_request("POST", "/waiting-list", data=waiting_list_data)
    
    def update_waiting_list_entry(self, waiting_list_id: str, waiting_list_data: Dict) -> Optional[Dict]:
        """Update waiting list entry"""
        return self._make_request("PUT", f"/waiting-list/{waiting_list_id}", data=waiting_list_data)
    
    def remove_from_waiting_list(self, waiting_list_id: str) -> bool:
        """Remove from waiting list"""
        response = self._make_request("DELETE", f"/waiting-list/{waiting_list_id}")
        return response is not None
    
    def get_next_waiting_party(self, restaurant_id: str) -> Optional[Dict]:
        """Get next party from waiting list"""
        return self._make_request("GET", f"/restaurants/{restaurant_id}/waiting-list/next")
    
    # Table assignment operations
    def assign_table_to_party(self, restaurant_id: str, table_id: str, party_id: str, 
                            server_id: str, notes: Optional[str] = None) -> Optional[Dict]:
        """Assign table to party"""
        data = {
            "table_id": table_id,
            "party_id": party_id,
            "server_id": server_id
        }
        if notes:
            data["notes"] = notes
        return self._make_request("POST", f"/restaurants/{restaurant_id}/seating/assign-table", data=data)
    
    def check_table_availability(self, restaurant_id: str, date_time: datetime, 
                               party_size: int, duration: int = 120) -> Optional[Dict]:
        """Check table availability"""
        params = {
            "date_time": date_time.isoformat(),
            "party_size": party_size,
            "duration": duration
        }
        return self._make_request("GET", f"/restaurants/{restaurant_id}/seating/check-availability", params=params)
    
    def complete_table_assignment(self, restaurant_id: str, assignment_id: str) -> Optional[Dict]:
        """Complete table assignment"""
        return self._make_request("PUT", f"/restaurants/{restaurant_id}/seating/complete-assignment", 
                                params={"assignment_id": assignment_id})
    
    def get_occupancy_analytics(self, restaurant_id: str, start_date: Optional[date] = None, 
                              end_date: Optional[date] = None) -> Optional[Dict]:
        """Get occupancy analytics"""
        params = {}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        return self._make_request("GET", f"/restaurants/{restaurant_id}/analytics/occupancy", params=params)
