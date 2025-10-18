"""
Assignment API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.services.assignment_service import AssignmentService
from app.models.schemas import (
    TableAssignment, TableAssignmentCreate, TableAssignmentUpdate,
    ReservationAssignment, ReservationAssignmentCreate, ReservationAssignmentUpdate
)

router = APIRouter(prefix="/assignments", tags=["Assignments"])


# Table Assignment routes
@router.get("/table-assignments", response_model=List[TableAssignment])
async def list_table_assignments(
    table_id: Optional[str] = Query(None, description="Filter assignments by table ID"),
    party_id: Optional[str] = Query(None, description="Filter assignments by party ID"),
    server_id: Optional[str] = Query(None, description="Filter assignments by server ID"),
    status: Optional[str] = Query(None, description="Filter assignments by status"),
    db: Session = Depends(get_db)
):
    """List all table assignments"""
    service = AssignmentService(db)
    return service.get_table_assignments(
        table_id=table_id,
        party_id=party_id,
        server_id=server_id,
        status=status
    )


@router.post("/table-assignments", response_model=TableAssignment, status_code=201)
async def create_table_assignment(
    assignment_data: TableAssignmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new table assignment"""
    service = AssignmentService(db)
    try:
        return service.create_table_assignment(assignment_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/table-assignments/{assignment_id}", response_model=TableAssignment)
async def get_table_assignment(
    assignment_id: str,
    db: Session = Depends(get_db)
):
    """Get table assignment by ID"""
    service = AssignmentService(db)
    assignment = service.get_table_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Table assignment not found")
    return assignment


@router.put("/table-assignments/{assignment_id}", response_model=TableAssignment)
async def update_table_assignment(
    assignment_id: str,
    assignment_data: TableAssignmentUpdate,
    db: Session = Depends(get_db)
):
    """Update table assignment"""
    service = AssignmentService(db)
    assignment = service.update_table_assignment(assignment_id, assignment_data)
    if not assignment:
        raise HTTPException(status_code=404, detail="Table assignment not found")
    return assignment


@router.put("/table-assignments/{assignment_id}/complete", response_model=TableAssignment)
async def complete_table_assignment(
    assignment_id: str,
    db: Session = Depends(get_db)
):
    """Complete table assignment"""
    service = AssignmentService(db)
    assignment = service.complete_table_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Table assignment not found")
    return assignment


@router.delete("/table-assignments/{assignment_id}", status_code=204)
async def delete_table_assignment(
    assignment_id: str,
    db: Session = Depends(get_db)
):
    """Delete table assignment"""
    service = AssignmentService(db)
    if not service.delete_table_assignment(assignment_id):
        raise HTTPException(status_code=404, detail="Table assignment not found")


# Reservation Assignment routes
@router.get("/reservation-assignments", response_model=List[ReservationAssignment])
async def list_reservation_assignments(
    reservation_id: Optional[str] = Query(None, description="Filter assignments by reservation ID"),
    table_id: Optional[str] = Query(None, description="Filter assignments by table ID"),
    server_id: Optional[str] = Query(None, description="Filter assignments by server ID"),
    status: Optional[str] = Query(None, description="Filter assignments by status"),
    db: Session = Depends(get_db)
):
    """List all reservation assignments"""
    service = AssignmentService(db)
    return service.get_reservation_assignments(
        reservation_id=reservation_id,
        table_id=table_id,
        server_id=server_id,
        status=status
    )


@router.post("/reservation-assignments", response_model=ReservationAssignment, status_code=201)
async def create_reservation_assignment(
    assignment_data: ReservationAssignmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new reservation assignment"""
    service = AssignmentService(db)
    try:
        return service.create_reservation_assignment(assignment_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reservation-assignments/{assignment_id}", response_model=ReservationAssignment)
async def get_reservation_assignment(
    assignment_id: str,
    db: Session = Depends(get_db)
):
    """Get reservation assignment by ID"""
    service = AssignmentService(db)
    assignment = service.get_reservation_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Reservation assignment not found")
    return assignment


@router.put("/reservation-assignments/{assignment_id}", response_model=ReservationAssignment)
async def update_reservation_assignment(
    assignment_id: str,
    assignment_data: ReservationAssignmentUpdate,
    db: Session = Depends(get_db)
):
    """Update reservation assignment"""
    service = AssignmentService(db)
    assignment = service.update_reservation_assignment(assignment_id, assignment_data)
    if not assignment:
        raise HTTPException(status_code=404, detail="Reservation assignment not found")
    return assignment


@router.put("/reservation-assignments/{assignment_id}/complete", response_model=ReservationAssignment)
async def complete_reservation_assignment(
    assignment_id: str,
    db: Session = Depends(get_db)
):
    """Complete reservation assignment"""
    service = AssignmentService(db)
    assignment = service.complete_reservation_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Reservation assignment not found")
    return assignment


@router.delete("/reservation-assignments/{assignment_id}", status_code=204)
async def delete_reservation_assignment(
    assignment_id: str,
    db: Session = Depends(get_db)
):
    """Delete reservation assignment"""
    service = AssignmentService(db)
    if not service.delete_reservation_assignment(assignment_id):
        raise HTTPException(status_code=404, detail="Reservation assignment not found")
