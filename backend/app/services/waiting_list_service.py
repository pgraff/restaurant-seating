"""
Waiting list service layer
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, asc
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.database import WaitingList
from app.models.schemas import WaitingListCreate, WaitingListUpdate


class WaitingListService:
    """Service for waiting list operations"""

    def __init__(self, db: Session):
        self.db = db

    def add_to_waiting_list(self, waiting_list_data: WaitingListCreate) -> WaitingList:
        """Add party to waiting list"""
        waiting_list_entry = WaitingList(
            id=str(uuid.uuid4()),
            customer_name=waiting_list_data.customer_name,
            customer_phone=waiting_list_data.customer_phone,
            party_size=waiting_list_data.party_size,
            estimated_wait_time=waiting_list_data.estimated_wait_time,
            notes=waiting_list_data.notes,
            restaurant_id=waiting_list_data.restaurant_id
        )
        self.db.add(waiting_list_entry)
        self.db.commit()
        self.db.refresh(waiting_list_entry)
        return waiting_list_entry

    def get_waiting_list_entry(self, waiting_list_id: str) -> Optional[WaitingList]:
        """Get waiting list entry by ID"""
        return self.db.query(WaitingList).filter(WaitingList.id == waiting_list_id).first()

    def get_waiting_list(self, restaurant_id: Optional[str] = None, 
                        status: Optional[str] = None) -> List[WaitingList]:
        """Get waiting list entries with optional filters"""
        query = self.db.query(WaitingList)
        
        if restaurant_id:
            query = query.filter(WaitingList.restaurant_id == restaurant_id)
        if status:
            query = query.filter(WaitingList.status == status)
            
        # Order by request time (FIFO)
        query = query.order_by(asc(WaitingList.request_time))
        return query.all()

    def get_next_waiting_party(self, restaurant_id: str) -> Optional[WaitingList]:
        """Get the next party in the waiting list"""
        return self.db.query(WaitingList).filter(
            and_(
                WaitingList.restaurant_id == restaurant_id,
                WaitingList.status == "WAITING"
            )
        ).order_by(asc(WaitingList.request_time)).first()

    def update_waiting_list_entry(self, waiting_list_id: str, 
                                 waiting_list_data: WaitingListUpdate) -> Optional[WaitingList]:
        """Update waiting list entry"""
        waiting_list_entry = self.get_waiting_list_entry(waiting_list_id)
        if not waiting_list_entry:
            return None

        update_data = waiting_list_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(waiting_list_entry, field, value)

        self.db.commit()
        self.db.refresh(waiting_list_entry)
        return waiting_list_entry

    def remove_from_waiting_list(self, waiting_list_id: str) -> bool:
        """Remove party from waiting list"""
        waiting_list_entry = self.get_waiting_list_entry(waiting_list_id)
        if not waiting_list_entry:
            return False

        self.db.delete(waiting_list_entry)
        self.db.commit()
        return True

    def mark_as_seated(self, waiting_list_id: str) -> Optional[WaitingList]:
        """Mark waiting list entry as seated"""
        waiting_list_entry = self.get_waiting_list_entry(waiting_list_id)
        if not waiting_list_entry:
            return None

        waiting_list_entry.status = "SEATED"
        self.db.commit()
        self.db.refresh(waiting_list_entry)
        return waiting_list_entry
