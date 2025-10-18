"""
Waiting List API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.services.waiting_list_service import WaitingListService
from app.models.schemas import WaitingList, WaitingListCreate, WaitingListUpdate

router = APIRouter(prefix="/waiting-list", tags=["Waiting List"])


@router.get("/", response_model=List[WaitingList])
async def list_waiting_list(
    restaurant_id: Optional[str] = Query(None, description="Filter waiting list by restaurant ID"),
    status: Optional[str] = Query(None, description="Filter waiting list by status"),
    db: Session = Depends(get_db)
):
    """List all waiting list entries"""
    service = WaitingListService(db)
    return service.get_waiting_list(restaurant_id=restaurant_id, status=status)


@router.post("/", response_model=WaitingList, status_code=201)
async def add_to_waiting_list(
    waiting_list_data: WaitingListCreate,
    db: Session = Depends(get_db)
):
    """Add party to waiting list"""
    service = WaitingListService(db)
    return service.add_to_waiting_list(waiting_list_data)


@router.get("/{waiting_list_id}", response_model=WaitingList)
async def get_waiting_list_entry(
    waiting_list_id: str,
    db: Session = Depends(get_db)
):
    """Get waiting list entry by ID"""
    service = WaitingListService(db)
    entry = service.get_waiting_list_entry(waiting_list_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Waiting list entry not found")
    return entry


@router.put("/{waiting_list_id}", response_model=WaitingList)
async def update_waiting_list_entry(
    waiting_list_id: str,
    waiting_list_data: WaitingListUpdate,
    db: Session = Depends(get_db)
):
    """Update waiting list entry"""
    service = WaitingListService(db)
    entry = service.update_waiting_list_entry(waiting_list_id, waiting_list_data)
    if not entry:
        raise HTTPException(status_code=404, detail="Waiting list entry not found")
    return entry


@router.delete("/{waiting_list_id}", status_code=204)
async def remove_from_waiting_list(
    waiting_list_id: str,
    db: Session = Depends(get_db)
):
    """Remove party from waiting list"""
    service = WaitingListService(db)
    if not service.remove_from_waiting_list(waiting_list_id):
        raise HTTPException(status_code=404, detail="Waiting list entry not found")


# Restaurant-specific waiting list operations
@router.get("/restaurants/{restaurant_id}/next", response_model=WaitingList)
async def get_next_waiting_party(
    restaurant_id: str,
    db: Session = Depends(get_db)
):
    """Get next party from waiting list for a restaurant"""
    service = WaitingListService(db)
    entry = service.get_next_waiting_party(restaurant_id)
    if not entry:
        raise HTTPException(status_code=404, detail="No parties in waiting list")
    return entry


@router.post("/restaurants/{restaurant_id}/add", response_model=WaitingList, status_code=201)
async def add_to_restaurant_waiting_list(
    restaurant_id: str,
    waiting_list_data: WaitingListCreate,
    db: Session = Depends(get_db)
):
    """Add party to restaurant's waiting list"""
    waiting_list_data.restaurant_id = restaurant_id
    service = WaitingListService(db)
    return service.add_to_waiting_list(waiting_list_data)
