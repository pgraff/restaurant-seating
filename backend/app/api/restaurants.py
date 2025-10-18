"""
Restaurant API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.connection import get_db
from app.services.restaurant_service import RestaurantService
from app.models.schemas import (
    Restaurant, RestaurantCreate, RestaurantUpdate,
    Section, SectionCreate, SectionUpdate,
    Table, TableCreate, TableUpdate,
    TableAvailabilityResponse, OccupancyAnalyticsResponse,
    PaginatedResponse, Error
)
from app.models.database import Restaurant as RestaurantModel

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/", response_model=PaginatedResponse)
async def list_restaurants(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List all restaurants with pagination"""
    service = RestaurantService(db)
    restaurants = service.get_restaurants(limit=limit, offset=offset)
    total = service.db.query(RestaurantModel).count()
    
    return PaginatedResponse(
        items=[{
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "phone": restaurant.phone,
            "opening_time": restaurant.opening_time,
            "closing_time": restaurant.closing_time,
            "max_capacity": restaurant.max_capacity,
            "created_at": restaurant.created_at.isoformat(),
            "updated_at": restaurant.updated_at.isoformat()
        } for restaurant in restaurants],
        total=total,
        limit=limit,
        offset=offset
    )


@router.post("/", response_model=Restaurant, status_code=201)
async def create_restaurant(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db)
):
    """Create a new restaurant"""
    service = RestaurantService(db)
    return service.create_restaurant(restaurant_data)


@router.get("/{restaurant_id}", response_model=Restaurant)
async def get_restaurant(
    restaurant_id: str,
    db: Session = Depends(get_db)
):
    """Get restaurant by ID"""
    service = RestaurantService(db)
    restaurant = service.get_restaurant(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.put("/{restaurant_id}", response_model=Restaurant)
async def update_restaurant(
    restaurant_id: str,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db)
):
    """Update restaurant"""
    service = RestaurantService(db)
    restaurant = service.update_restaurant(restaurant_id, restaurant_data)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.delete("/{restaurant_id}", status_code=204)
async def delete_restaurant(
    restaurant_id: str,
    db: Session = Depends(get_db)
):
    """Delete restaurant"""
    service = RestaurantService(db)
    if not service.delete_restaurant(restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")


# Section routes
@router.get("/{restaurant_id}/sections", response_model=List[Section])
async def list_sections(
    restaurant_id: str,
    db: Session = Depends(get_db)
):
    """List sections for a restaurant"""
    service = RestaurantService(db)
    return service.get_sections(restaurant_id=restaurant_id)


@router.post("/{restaurant_id}/sections", response_model=Section, status_code=201)
async def create_section(
    restaurant_id: str,
    section_data: SectionCreate,
    db: Session = Depends(get_db)
):
    """Create a new section for a restaurant"""
    # Verify restaurant exists
    service = RestaurantService(db)
    restaurant = service.get_restaurant(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    section_data.restaurant_id = restaurant_id
    return service.create_section(section_data)


# Table routes
@router.get("/{restaurant_id}/tables", response_model=List[Table])
async def list_tables(
    restaurant_id: str,
    section_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List tables for a restaurant"""
    service = RestaurantService(db)
    return service.get_tables(restaurant_id=restaurant_id, section_id=section_id, status=status)


@router.post("/{restaurant_id}/tables", response_model=Table, status_code=201)
async def create_table(
    restaurant_id: str,
    table_data: TableCreate,
    db: Session = Depends(get_db)
):
    """Create a new table for a restaurant"""
    # Verify restaurant exists
    service = RestaurantService(db)
    restaurant = service.get_restaurant(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    table_data.restaurant_id = restaurant_id
    return service.create_table(table_data)


# Complex restaurant operations
@router.post("/{restaurant_id}/seating/assign-table")
async def assign_table_to_party(
    restaurant_id: str,
    table_id: str,
    party_id: str,
    server_id: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Assign table to party"""
    from app.services.assignment_service import AssignmentService
    from app.models.schemas import TableAssignmentCreate
    
    # Verify restaurant exists
    service = RestaurantService(db)
    restaurant = service.get_restaurant(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    assignment_service = AssignmentService(db)
    assignment_data = TableAssignmentCreate(
        table_id=table_id,
        party_id=party_id,
        server_id=server_id,
        notes=notes
    )
    
    try:
        assignment = assignment_service.create_table_assignment(assignment_data)
        return assignment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{restaurant_id}/seating/check-availability", response_model=TableAvailabilityResponse)
async def check_table_availability(
    restaurant_id: str,
    date_time: datetime = Query(..., description="Date and time to check availability"),
    party_size: int = Query(..., ge=1, description="Number of people in the party"),
    duration: int = Query(120, ge=30, description="Expected dining duration in minutes"),
    db: Session = Depends(get_db)
):
    """Check table availability for a given time and party size"""
    service = RestaurantService(db)
    return service.check_table_availability(restaurant_id, date_time, party_size, duration)


@router.get("/{restaurant_id}/analytics/occupancy", response_model=OccupancyAnalyticsResponse)
async def get_occupancy_analytics(
    restaurant_id: str,
    start_date: Optional[datetime] = Query(None, description="Start date for analytics"),
    end_date: Optional[datetime] = Query(None, description="End date for analytics"),
    db: Session = Depends(get_db)
):
    """Get occupancy analytics for the restaurant"""
    service = RestaurantService(db)
    return service.get_occupancy_analytics(restaurant_id, start_date, end_date)
