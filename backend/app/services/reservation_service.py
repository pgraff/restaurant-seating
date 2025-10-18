"""
Reservation service layer
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime, date
import uuid

from app.models.database import Reservation
from app.models.schemas import ReservationCreate, ReservationUpdate


class ReservationService:
    """Service for reservation operations"""

    def __init__(self, db: Session):
        self.db = db

    def create_reservation(self, reservation_data: ReservationCreate) -> Reservation:
        """Create a new reservation"""
        reservation = Reservation(
            id=str(uuid.uuid4()),
            reservation_time=reservation_data.reservation_time,
            party_size=reservation_data.party_size,
            customer_name=reservation_data.customer_name,
            customer_phone=reservation_data.customer_phone,
            customer_email=reservation_data.customer_email,
            special_requests=reservation_data.special_requests,
            restaurant_id=reservation_data.restaurant_id
        )
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        """Get reservation by ID"""
        return self.db.query(Reservation).filter(Reservation.id == reservation_id).first()

    def get_reservations(self, restaurant_id: Optional[str] = None, 
                        status: Optional[str] = None, 
                        date_filter: Optional[date] = None) -> List[Reservation]:
        """Get reservations with optional filters"""
        query = self.db.query(Reservation)
        
        if restaurant_id:
            query = query.filter(Reservation.restaurant_id == restaurant_id)
        if status:
            query = query.filter(Reservation.status == status)
        if date_filter:
            query = query.filter(Reservation.reservation_time.date() == date_filter)
            
        return query.all()

    def update_reservation(self, reservation_id: str, reservation_data: ReservationUpdate) -> Optional[Reservation]:
        """Update reservation"""
        reservation = self.get_reservation(reservation_id)
        if not reservation:
            return None

        update_data = reservation_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(reservation, field, value)

        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def cancel_reservation(self, reservation_id: str) -> Optional[Reservation]:
        """Cancel a reservation"""
        reservation = self.get_reservation(reservation_id)
        if not reservation:
            return None

        reservation.status = "CANCELLED"
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def delete_reservation(self, reservation_id: str) -> bool:
        """Delete reservation"""
        reservation = self.get_reservation(reservation_id)
        if not reservation:
            return False

        self.db.delete(reservation)
        self.db.commit()
        return True
