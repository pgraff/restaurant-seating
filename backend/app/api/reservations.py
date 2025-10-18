"""
Reservation API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database.connection import get_db
from app.services.reservation_service import ReservationService
from app.models.schemas import Reservation, ReservationCreate, ReservationUpdate

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/", response_model=List[Reservation])
async def list_reservations(
    restaurant_id: Optional[str] = Query(None, description="Filter reservations by restaurant ID"),
    status: Optional[str] = Query(None, description="Filter reservations by status"),
    date_filter: Optional[date] = Query(None, description="Filter reservations by date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """List all reservations"""
    service = ReservationService(db)
    return service.get_reservations(
        restaurant_id=restaurant_id,
        status=status,
        date_filter=date_filter
    )


@router.post("/", response_model=Reservation, status_code=201)
async def create_reservation(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db)
):
    """Create a new reservation"""
    service = ReservationService(db)
    return service.create_reservation(reservation_data)


@router.get("/{reservation_id}", response_model=Reservation)
async def get_reservation(
    reservation_id: str,
    db: Session = Depends(get_db)
):
    """Get reservation by ID"""
    service = ReservationService(db)
    reservation = service.get_reservation(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@router.put("/{reservation_id}", response_model=Reservation)
async def update_reservation(
    reservation_id: str,
    reservation_data: ReservationUpdate,
    db: Session = Depends(get_db)
):
    """Update reservation"""
    service = ReservationService(db)
    reservation = service.update_reservation(reservation_id, reservation_data)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@router.delete("/{reservation_id}", response_model=Reservation)
async def cancel_reservation(
    reservation_id: str,
    db: Session = Depends(get_db)
):
    """Cancel reservation"""
    service = ReservationService(db)
    reservation = service.cancel_reservation(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation
