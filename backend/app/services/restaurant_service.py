"""
Restaurant service layer
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime, time
import uuid

from app.models.database import Restaurant, Section, Table, Party, Reservation, WaitingList, Server
from app.models.schemas import (
    RestaurantCreate, RestaurantUpdate, SectionCreate, SectionUpdate,
    TableCreate, TableUpdate, PartyCreate, PartyUpdate,
    ReservationCreate, ReservationUpdate, WaitingListCreate, WaitingListUpdate,
    ServerCreate, ServerUpdate, TableAvailabilityResponse, OccupancyAnalyticsResponse
)


class RestaurantService:
    """Service for restaurant operations"""

    def __init__(self, db: Session):
        self.db = db

    # Restaurant CRUD operations
    def create_restaurant(self, restaurant_data: RestaurantCreate) -> Restaurant:
        """Create a new restaurant"""
        restaurant = Restaurant(
            id=str(uuid.uuid4()),
            name=restaurant_data.name,
            address=restaurant_data.address,
            phone=restaurant_data.phone,
            opening_time=restaurant_data.opening_time,
            closing_time=restaurant_data.closing_time,
            max_capacity=restaurant_data.max_capacity
        )
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def get_restaurant(self, restaurant_id: str) -> Optional[Restaurant]:
        """Get restaurant by ID"""
        return self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    def get_restaurants(self, limit: int = 20, offset: int = 0) -> List[Restaurant]:
        """Get all restaurants with pagination"""
        return self.db.query(Restaurant).offset(offset).limit(limit).all()

    def update_restaurant(self, restaurant_id: str, restaurant_data: RestaurantUpdate) -> Optional[Restaurant]:
        """Update restaurant"""
        restaurant = self.get_restaurant(restaurant_id)
        if not restaurant:
            return None

        update_data = restaurant_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(restaurant, field, value)

        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def delete_restaurant(self, restaurant_id: str) -> bool:
        """Delete restaurant"""
        restaurant = self.get_restaurant(restaurant_id)
        if not restaurant:
            return False

        self.db.delete(restaurant)
        self.db.commit()
        return True

    # Section operations
    def create_section(self, section_data: SectionCreate) -> Section:
        """Create a new section"""
        section = Section(
            id=str(uuid.uuid4()),
            name=section_data.name,
            description=section_data.description,
            capacity=section_data.capacity,
            is_active=section_data.is_active,
            restaurant_id=section_data.restaurant_id
        )
        self.db.add(section)
        self.db.commit()
        self.db.refresh(section)
        return section

    def get_sections(self, restaurant_id: Optional[str] = None) -> List[Section]:
        """Get sections, optionally filtered by restaurant"""
        query = self.db.query(Section)
        if restaurant_id:
            query = query.filter(Section.restaurant_id == restaurant_id)
        return query.all()

    def get_section(self, section_id: str) -> Optional[Section]:
        """Get section by ID"""
        return self.db.query(Section).filter(Section.id == section_id).first()

    def update_section(self, section_id: str, section_data: SectionUpdate) -> Optional[Section]:
        """Update section"""
        section = self.get_section(section_id)
        if not section:
            return None

        update_data = section_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(section, field, value)

        self.db.commit()
        self.db.refresh(section)
        return section

    def delete_section(self, section_id: str) -> bool:
        """Delete section"""
        section = self.get_section(section_id)
        if not section:
            return False

        self.db.delete(section)
        self.db.commit()
        return True

    # Table operations
    def create_table(self, table_data: TableCreate) -> Table:
        """Create a new table"""
        table = Table(
            id=str(uuid.uuid4()),
            table_number=table_data.table_number,
            capacity=table_data.capacity,
            location=table_data.location,
            is_active=table_data.is_active,
            status=table_data.status,
            restaurant_id=table_data.restaurant_id
        )
        self.db.add(table)
        self.db.commit()
        self.db.refresh(table)
        return table

    def get_tables(self, restaurant_id: Optional[str] = None, section_id: Optional[str] = None, 
                   status: Optional[str] = None) -> List[Table]:
        """Get tables with optional filters"""
        query = self.db.query(Table)
        if restaurant_id:
            query = query.filter(Table.restaurant_id == restaurant_id)
        if section_id:
            query = query.join(TableSection).filter(TableSection.section_id == section_id)
        if status:
            query = query.filter(Table.status == status)
        return query.all()

    def get_table(self, table_id: str) -> Optional[Table]:
        """Get table by ID"""
        return self.db.query(Table).filter(Table.id == table_id).first()

    def update_table(self, table_id: str, table_data: TableUpdate) -> Optional[Table]:
        """Update table"""
        table = self.get_table(table_id)
        if not table:
            return None

        update_data = table_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(table, field, value)

        self.db.commit()
        self.db.refresh(table)
        return table

    def delete_table(self, table_id: str) -> bool:
        """Delete table"""
        table = self.get_table(table_id)
        if not table:
            return False

        self.db.delete(table)
        self.db.commit()
        return True

    # Table availability operations
    def check_table_availability(self, restaurant_id: str, date_time: datetime, 
                                party_size: int, duration: int = 120) -> TableAvailabilityResponse:
        """Check table availability for a given time and party size"""
        # Get available tables that can accommodate the party size
        available_tables = self.db.query(Table).filter(
            and_(
                Table.restaurant_id == restaurant_id,
                Table.is_active == True,
                Table.status == "AVAILABLE",
                Table.capacity >= party_size
            )
        ).all()

        # Calculate estimated wait time if no tables available
        estimated_wait_time = None
        if not available_tables:
            # Simple estimation based on current occupancy
            total_tables = self.db.query(Table).filter(Table.restaurant_id == restaurant_id).count()
            occupied_tables = self.db.query(Table).filter(
                and_(
                    Table.restaurant_id == restaurant_id,
                    Table.status.in_(["OCCUPIED", "RESERVED"])
                )
            ).count()
            
            if total_tables > 0:
                occupancy_rate = occupied_tables / total_tables
                estimated_wait_time = int(occupancy_rate * 60)  # Rough estimate in minutes

        return TableAvailabilityResponse(
            available_tables=available_tables,
            estimated_wait_time=estimated_wait_time
        )

    # Occupancy analytics
    def get_occupancy_analytics(self, restaurant_id: str, start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None) -> OccupancyAnalyticsResponse:
        """Get occupancy analytics for the restaurant"""
        total_tables = self.db.query(Table).filter(Table.restaurant_id == restaurant_id).count()
        occupied_tables = self.db.query(Table).filter(
            and_(
                Table.restaurant_id == restaurant_id,
                Table.status.in_(["OCCUPIED", "RESERVED"])
            )
        ).count()

        current_occupancy = (occupied_tables / total_tables * 100) if total_tables > 0 else 0

        # For now, return basic analytics
        # In a real implementation, you'd calculate historical data
        return OccupancyAnalyticsResponse(
            current_occupancy=current_occupancy,
            average_occupancy=current_occupancy,  # Simplified
            peak_hours=["19:00", "20:00", "21:00"],  # Placeholder
            total_tables=total_tables,
            occupied_tables=occupied_tables
        )
