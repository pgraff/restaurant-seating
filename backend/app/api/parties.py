"""
Party API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.services.party_service import PartyService
from app.models.schemas import Party, PartyCreate, PartyUpdate

router = APIRouter(prefix="/parties", tags=["Parties"])


@router.get("/", response_model=List[Party])
async def list_parties(
    status: Optional[str] = Query(None, description="Filter parties by status"),
    db: Session = Depends(get_db)
):
    """List all parties"""
    service = PartyService(db)
    return service.get_parties(status=status)


@router.post("/", response_model=Party, status_code=201)
async def create_party(
    party_data: PartyCreate,
    db: Session = Depends(get_db)
):
    """Create a new party"""
    service = PartyService(db)
    return service.create_party(party_data)


@router.get("/{party_id}", response_model=Party)
async def get_party(
    party_id: str,
    db: Session = Depends(get_db)
):
    """Get party by ID"""
    service = PartyService(db)
    party = service.get_party(party_id)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party


@router.put("/{party_id}", response_model=Party)
async def update_party(
    party_id: str,
    party_data: PartyUpdate,
    db: Session = Depends(get_db)
):
    """Update party"""
    service = PartyService(db)
    party = service.update_party(party_id, party_data)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party


@router.delete("/{party_id}", status_code=204)
async def delete_party(
    party_id: str,
    db: Session = Depends(get_db)
):
    """Delete party"""
    service = PartyService(db)
    if not service.delete_party(party_id):
        raise HTTPException(status_code=404, detail="Party not found")
