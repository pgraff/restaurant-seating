"""
Assignment service layer for table and reservation assignments
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.database import TableAssignment, ReservationAssignment, Table, Party, Server, Reservation
from app.models.schemas import (
    TableAssignmentCreate, TableAssignmentUpdate,
    ReservationAssignmentCreate, ReservationAssignmentUpdate
)


class AssignmentService:
    """Service for assignment operations"""

    def __init__(self, db: Session):
        self.db = db

    # Table Assignment operations
    def create_table_assignment(self, assignment_data: TableAssignmentCreate) -> TableAssignment:
        """Create a new table assignment"""
        # Check if table is available
        table = self.db.query(Table).filter(Table.id == assignment_data.table_id).first()
        if not table or table.status != "AVAILABLE":
            raise ValueError("Table is not available for assignment")

        # Check if party exists and is waiting
        party = self.db.query(Party).filter(Party.id == assignment_data.party_id).first()
        if not party or party.status != "WAITING":
            raise ValueError("Party is not available for assignment")

        # Check if server exists and is active
        server = self.db.query(Server).filter(Server.id == assignment_data.server_id).first()
        if not server or not server.is_active:
            raise ValueError("Server is not available for assignment")

        assignment = TableAssignment(
            id=str(uuid.uuid4()),
            table_id=assignment_data.table_id,
            party_id=assignment_data.party_id,
            server_id=assignment_data.server_id,
            notes=assignment_data.notes
        )
        
        self.db.add(assignment)
        
        # Update table status
        table.status = "OCCUPIED"
        
        # Update party status
        party.status = "SEATED"
        
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def get_table_assignment(self, assignment_id: str) -> Optional[TableAssignment]:
        """Get table assignment by ID"""
        return self.db.query(TableAssignment).filter(TableAssignment.id == assignment_id).first()

    def get_table_assignments(self, table_id: Optional[str] = None,
                             party_id: Optional[str] = None,
                             server_id: Optional[str] = None,
                             status: Optional[str] = None) -> List[TableAssignment]:
        """Get table assignments with optional filters"""
        query = self.db.query(TableAssignment)
        
        if table_id:
            query = query.filter(TableAssignment.table_id == table_id)
        if party_id:
            query = query.filter(TableAssignment.party_id == party_id)
        if server_id:
            query = query.filter(TableAssignment.server_id == server_id)
        if status:
            query = query.filter(TableAssignment.status == status)
            
        return query.all()

    def update_table_assignment(self, assignment_id: str, 
                               assignment_data: TableAssignmentUpdate) -> Optional[TableAssignment]:
        """Update table assignment"""
        assignment = self.get_table_assignment(assignment_id)
        if not assignment:
            return None

        update_data = assignment_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(assignment, field, value)

        # If marking as completed, update table status
        if assignment_data.status == "COMPLETED":
            table = self.db.query(Table).filter(Table.id == assignment.table_id).first()
            if table:
                table.status = "CLEANING"  # Table needs cleaning after party leaves

        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def complete_table_assignment(self, assignment_id: str) -> Optional[TableAssignment]:
        """Complete a table assignment"""
        assignment = self.get_table_assignment(assignment_id)
        if not assignment:
            return None

        assignment.status = "COMPLETED"
        assignment.completed_at = datetime.utcnow()
        
        # Update table status
        table = self.db.query(Table).filter(Table.id == assignment.table_id).first()
        if table:
            table.status = "CLEANING"
        
        # Update party status
        party = self.db.query(Party).filter(Party.id == assignment.party_id).first()
        if party:
            party.status = "FINISHED"

        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def delete_table_assignment(self, assignment_id: str) -> bool:
        """Delete table assignment"""
        assignment = self.get_table_assignment(assignment_id)
        if not assignment:
            return False

        # Reset table status
        table = self.db.query(Table).filter(Table.id == assignment.table_id).first()
        if table:
            table.status = "AVAILABLE"

        self.db.delete(assignment)
        self.db.commit()
        return True

    # Reservation Assignment operations
    def create_reservation_assignment(self, assignment_data: ReservationAssignmentCreate) -> ReservationAssignment:
        """Create a new reservation assignment"""
        # Check if table is available
        table = self.db.query(Table).filter(Table.id == assignment_data.table_id).first()
        if not table or table.status != "AVAILABLE":
            raise ValueError("Table is not available for assignment")

        # Check if reservation exists and is confirmed
        reservation = self.db.query(Reservation).filter(Reservation.id == assignment_data.reservation_id).first()
        if not reservation or reservation.status != "CONFIRMED":
            raise ValueError("Reservation is not available for assignment")

        # Check if server exists and is active
        server = self.db.query(Server).filter(Server.id == assignment_data.server_id).first()
        if not server or not server.is_active:
            raise ValueError("Server is not available for assignment")

        assignment = ReservationAssignment(
            id=str(uuid.uuid4()),
            reservation_id=assignment_data.reservation_id,
            table_id=assignment_data.table_id,
            server_id=assignment_data.server_id,
            notes=assignment_data.notes
        )
        
        self.db.add(assignment)
        
        # Update table status
        table.status = "RESERVED"
        
        # Update reservation status
        reservation.status = "CONFIRMED"
        
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def get_reservation_assignment(self, assignment_id: str) -> Optional[ReservationAssignment]:
        """Get reservation assignment by ID"""
        return self.db.query(ReservationAssignment).filter(ReservationAssignment.id == assignment_id).first()

    def get_reservation_assignments(self, reservation_id: Optional[str] = None,
                                   table_id: Optional[str] = None,
                                   server_id: Optional[str] = None,
                                   status: Optional[str] = None) -> List[ReservationAssignment]:
        """Get reservation assignments with optional filters"""
        query = self.db.query(ReservationAssignment)
        
        if reservation_id:
            query = query.filter(ReservationAssignment.reservation_id == reservation_id)
        if table_id:
            query = query.filter(ReservationAssignment.table_id == table_id)
        if server_id:
            query = query.filter(ReservationAssignment.server_id == server_id)
        if status:
            query = query.filter(ReservationAssignment.status == status)
            
        return query.all()

    def update_reservation_assignment(self, assignment_id: str, 
                                     assignment_data: ReservationAssignmentUpdate) -> Optional[ReservationAssignment]:
        """Update reservation assignment"""
        assignment = self.get_reservation_assignment(assignment_id)
        if not assignment:
            return None

        update_data = assignment_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(assignment, field, value)

        # If marking as completed, update table status
        if assignment_data.status == "COMPLETED":
            table = self.db.query(Table).filter(Table.id == assignment.table_id).first()
            if table:
                table.status = "CLEANING"  # Table needs cleaning after party leaves

        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def complete_reservation_assignment(self, assignment_id: str) -> Optional[ReservationAssignment]:
        """Complete a reservation assignment"""
        assignment = self.get_reservation_assignment(assignment_id)
        if not assignment:
            return None

        assignment.status = "COMPLETED"
        assignment.completed_at = datetime.utcnow()
        
        # Update table status
        table = self.db.query(Table).filter(Table.id == assignment.table_id).first()
        if table:
            table.status = "CLEANING"
        
        # Update reservation status
        reservation = self.db.query(Reservation).filter(Reservation.id == assignment.reservation_id).first()
        if reservation:
            reservation.status = "COMPLETED"

        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def delete_reservation_assignment(self, assignment_id: str) -> bool:
        """Delete reservation assignment"""
        assignment = self.get_reservation_assignment(assignment_id)
        if not assignment:
            return False

        # Reset table status
        table = self.db.query(Table).filter(Table.id == assignment.table_id).first()
        if table:
            table.status = "AVAILABLE"

        self.db.delete(assignment)
        self.db.commit()
        return True
