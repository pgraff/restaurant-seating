"""
Server service layer
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import uuid

from app.models.database import Server
from app.models.schemas import ServerCreate, ServerUpdate


class ServerService:
    """Service for server operations"""

    def __init__(self, db: Session):
        self.db = db

    def create_server(self, server_data: ServerCreate) -> Server:
        """Create a new server"""
        server = Server(
            id=str(uuid.uuid4()),
            first_name=server_data.first_name,
            last_name=server_data.last_name,
            employee_id=server_data.employee_id,
            is_active=server_data.is_active,
            shift_start=server_data.shift_start,
            shift_end=server_data.shift_end,
            restaurant_id=server_data.restaurant_id
        )
        self.db.add(server)
        self.db.commit()
        self.db.refresh(server)
        return server

    def get_server(self, server_id: str) -> Optional[Server]:
        """Get server by ID"""
        return self.db.query(Server).filter(Server.id == server_id).first()

    def get_servers(self, restaurant_id: Optional[str] = None, 
                   is_active: Optional[bool] = None) -> List[Server]:
        """Get servers with optional filters"""
        query = self.db.query(Server)
        
        if restaurant_id:
            query = query.filter(Server.restaurant_id == restaurant_id)
        if is_active is not None:
            query = query.filter(Server.is_active == is_active)
            
        return query.all()

    def update_server(self, server_id: str, server_data: ServerUpdate) -> Optional[Server]:
        """Update server"""
        server = self.get_server(server_id)
        if not server:
            return None

        update_data = server_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(server, field, value)

        self.db.commit()
        self.db.refresh(server)
        return server

    def delete_server(self, server_id: str) -> bool:
        """Delete server"""
        server = self.get_server(server_id)
        if not server:
            return False

        self.db.delete(server)
        self.db.commit()
        return True
