"""
Pydantic models for API request/response schemas
Based on the OpenAPI specification
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums
class TableStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    RESERVED = "RESERVED"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    CLEANING = "CLEANING"


class PartyStatus(str, Enum):
    WAITING = "WAITING"
    SEATED = "SEATED"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"


class ReservationStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    NO_SHOW = "NO_SHOW"


class WaitingListStatus(str, Enum):
    WAITING = "WAITING"
    SEATED = "SEATED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class AssignmentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# Base models
class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    class Config:
        from_attributes = True
        use_enum_values = True


# Restaurant schemas
class RestaurantBase(BaseSchema):
    name: str = Field(..., description="Name of the restaurant")
    address: str = Field(..., description="Physical address of the restaurant")
    phone: str = Field(..., description="Contact phone number")
    opening_time: str = Field(..., description="Daily opening time")
    closing_time: str = Field(..., description="Daily closing time")
    max_capacity: int = Field(..., ge=1, description="Maximum total capacity of the restaurant")


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseSchema):
    name: Optional[str] = Field(None, description="Name of the restaurant")
    address: Optional[str] = Field(None, description="Physical address of the restaurant")
    phone: Optional[str] = Field(None, description="Contact phone number")
    opening_time: Optional[str] = Field(None, description="Daily opening time")
    closing_time: Optional[str] = Field(None, description="Daily closing time")
    max_capacity: Optional[int] = Field(None, ge=1, description="Maximum total capacity of the restaurant")


class Restaurant(RestaurantBase):
    id: str = Field(..., description="Unique identifier for the restaurant")
    created_at: datetime = Field(..., description="When the restaurant was created")
    updated_at: datetime = Field(..., description="When the restaurant was last updated")


# Section schemas
class SectionBase(BaseSchema):
    name: str = Field(..., description="Name of the section")
    description: Optional[str] = Field(None, description="Description of the section")
    capacity: int = Field(..., ge=1, description="Maximum capacity of the section")
    is_active: bool = Field(True, description="Whether the section is currently active")


class SectionCreate(SectionBase):
    restaurant_id: str = Field(..., description="ID of the restaurant this section belongs to")


class SectionUpdate(BaseSchema):
    name: Optional[str] = Field(None, description="Name of the section")
    description: Optional[str] = Field(None, description="Description of the section")
    capacity: Optional[int] = Field(None, ge=1, description="Maximum capacity of the section")
    is_active: Optional[bool] = Field(None, description="Whether the section is currently active")


class Section(SectionBase):
    id: str = Field(..., description="Unique identifier for the section")
    restaurant_id: str = Field(..., description="ID of the restaurant this section belongs to")
    created_at: datetime = Field(..., description="When the section was created")
    updated_at: datetime = Field(..., description="When the section was last updated")


# Table schemas
class TableBase(BaseSchema):
    table_number: str = Field(..., description="Human-readable table number")
    capacity: int = Field(..., ge=1, description="Maximum number of people the table can seat")
    location: str = Field(..., description="Physical location description of the table")
    is_active: bool = Field(True, description="Whether the table is currently active")
    status: TableStatus = Field(TableStatus.AVAILABLE, description="Current status of the table")


class TableCreate(TableBase):
    restaurant_id: str = Field(..., description="ID of the restaurant this table belongs to")
    section_ids: Optional[List[str]] = Field(default_factory=list, description="IDs of sections this table belongs to")


class TableUpdate(BaseSchema):
    table_number: Optional[str] = Field(None, description="Human-readable table number")
    capacity: Optional[int] = Field(None, ge=1, description="Maximum number of people the table can seat")
    location: Optional[str] = Field(None, description="Physical location description of the table")
    is_active: Optional[bool] = Field(None, description="Whether the table is currently active")
    status: Optional[TableStatus] = Field(None, description="Current status of the table")
    section_ids: Optional[List[str]] = Field(None, description="IDs of sections this table belongs to")


class Table(TableBase):
    id: str = Field(..., description="Unique identifier for the table")
    restaurant_id: str = Field(..., description="ID of the restaurant this table belongs to")
    section_ids: List[str] = Field(default_factory=list, description="IDs of sections this table belongs to")
    created_at: datetime = Field(..., description="When the table was created")
    updated_at: datetime = Field(..., description="When the table was last updated")


# Party schemas
class PartyBase(BaseSchema):
    name: str = Field(..., description="Name of the party (e.g., 'Smith Party')")
    size: int = Field(..., ge=1, description="Number of people in the party")
    phone: Optional[str] = Field(None, description="Contact phone number for the party")
    email: Optional[EmailStr] = Field(None, description="Contact email for the party")


class PartyCreate(PartyBase):
    status: PartyStatus = Field(PartyStatus.WAITING, description="Current status of the party")
    arrival_time: Optional[datetime] = Field(None, description="When the party arrived")


class PartyUpdate(BaseSchema):
    name: Optional[str] = Field(None, description="Name of the party (e.g., 'Smith Party')")
    size: Optional[int] = Field(None, ge=1, description="Number of people in the party")
    phone: Optional[str] = Field(None, description="Contact phone number for the party")
    email: Optional[EmailStr] = Field(None, description="Contact email for the party")
    status: Optional[PartyStatus] = Field(None, description="Current status of the party")
    arrival_time: Optional[datetime] = Field(None, description="When the party arrived")


class Party(PartyBase):
    id: str = Field(..., description="Unique identifier for the party")
    status: PartyStatus = Field(..., description="Current status of the party")
    arrival_time: datetime = Field(..., description="When the party arrived")
    created_at: datetime = Field(..., description="When the party was created")
    updated_at: datetime = Field(..., description="When the party was last updated")


# Reservation schemas
class ReservationBase(BaseSchema):
    reservation_time: datetime = Field(..., description="Scheduled reservation time")
    party_size: int = Field(..., ge=1, description="Number of people in the party")
    customer_name: str = Field(..., description="Name of the customer making the reservation")
    customer_phone: str = Field(..., description="Phone number of the customer")
    customer_email: Optional[EmailStr] = Field(None, description="Email address of the customer")
    special_requests: Optional[str] = Field(None, description="Any special requests or notes")


class ReservationCreate(ReservationBase):
    restaurant_id: str = Field(..., description="ID of the restaurant")


class ReservationUpdate(BaseSchema):
    reservation_time: Optional[datetime] = Field(None, description="Scheduled reservation time")
    party_size: Optional[int] = Field(None, ge=1, description="Number of people in the party")
    customer_name: Optional[str] = Field(None, description="Name of the customer making the reservation")
    customer_phone: Optional[str] = Field(None, description="Phone number of the customer")
    customer_email: Optional[EmailStr] = Field(None, description="Email address of the customer")
    special_requests: Optional[str] = Field(None, description="Any special requests or notes")
    status: Optional[ReservationStatus] = Field(None, description="Current status of the reservation")


class Reservation(ReservationBase):
    id: str = Field(..., description="Unique identifier for the reservation")
    status: ReservationStatus = Field(..., description="Current status of the reservation")
    restaurant_id: str = Field(..., description="ID of the restaurant")
    party_id: Optional[str] = Field(None, description="ID of the associated party")
    created_at: datetime = Field(..., description="When the reservation was created")
    updated_at: datetime = Field(..., description="When the reservation was last updated")


# Waiting List schemas
class WaitingListBase(BaseSchema):
    customer_name: str = Field(..., description="Name of the customer")
    customer_phone: str = Field(..., description="Phone number of the customer")
    party_size: int = Field(..., ge=1, description="Number of people in the party")
    estimated_wait_time: Optional[int] = Field(None, ge=0, description="Estimated wait time in minutes")
    notes: Optional[str] = Field(None, description="Additional notes about the waiting list entry")


class WaitingListCreate(WaitingListBase):
    restaurant_id: str = Field(..., description="ID of the restaurant")


class WaitingListUpdate(BaseSchema):
    customer_name: Optional[str] = Field(None, description="Name of the customer")
    customer_phone: Optional[str] = Field(None, description="Phone number of the customer")
    party_size: Optional[int] = Field(None, ge=1, description="Number of people in the party")
    estimated_wait_time: Optional[int] = Field(None, ge=0, description="Estimated wait time in minutes")
    status: Optional[WaitingListStatus] = Field(None, description="Current status of the waiting list entry")
    notes: Optional[str] = Field(None, description="Additional notes about the waiting list entry")


class WaitingList(WaitingListBase):
    id: str = Field(..., description="Unique identifier for the waiting list entry")
    request_time: datetime = Field(..., description="When the customer requested to be added to waiting list")
    status: WaitingListStatus = Field(..., description="Current status of the waiting list entry")
    restaurant_id: str = Field(..., description="ID of the restaurant")
    created_at: datetime = Field(..., description="When the waiting list entry was created")
    updated_at: datetime = Field(..., description="When the waiting list entry was last updated")


# Server schemas
class ServerBase(BaseSchema):
    first_name: str = Field(..., description="First name of the server")
    last_name: str = Field(..., description="Last name of the server")
    employee_id: str = Field(..., description="Employee ID number")
    is_active: bool = Field(True, description="Whether the server is currently active")
    shift_start: Optional[datetime] = Field(None, description="Start time of current shift")
    shift_end: Optional[datetime] = Field(None, description="End time of current shift")


class ServerCreate(ServerBase):
    restaurant_id: str = Field(..., description="ID of the restaurant this server works for")


class ServerUpdate(BaseSchema):
    first_name: Optional[str] = Field(None, description="First name of the server")
    last_name: Optional[str] = Field(None, description="Last name of the server")
    employee_id: Optional[str] = Field(None, description="Employee ID number")
    is_active: Optional[bool] = Field(None, description="Whether the server is currently active")
    shift_start: Optional[datetime] = Field(None, description="Start time of current shift")
    shift_end: Optional[datetime] = Field(None, description="End time of current shift")


class Server(ServerBase):
    id: str = Field(..., description="Unique identifier for the server")
    restaurant_id: str = Field(..., description="ID of the restaurant this server works for")
    created_at: datetime = Field(..., description="When the server was created")
    updated_at: datetime = Field(..., description="When the server was last updated")


# Table Assignment schemas
class TableAssignmentBase(BaseSchema):
    table_id: str = Field(..., description="ID of the assigned table")
    party_id: str = Field(..., description="ID of the assigned party")
    server_id: str = Field(..., description="ID of the managing server")
    notes: Optional[str] = Field(None, description="Additional notes about the assignment")


class TableAssignmentCreate(TableAssignmentBase):
    pass


class TableAssignmentUpdate(BaseSchema):
    status: Optional[AssignmentStatus] = Field(None, description="Current status of the assignment")
    completed_at: Optional[datetime] = Field(None, description="When the assignment was completed")
    notes: Optional[str] = Field(None, description="Additional notes about the assignment")


class TableAssignment(TableAssignmentBase):
    id: str = Field(..., description="Unique identifier for the assignment")
    assigned_at: datetime = Field(..., description="When the assignment was made")
    completed_at: Optional[datetime] = Field(None, description="When the assignment was completed")
    status: AssignmentStatus = Field(..., description="Current status of the assignment")
    created_at: datetime = Field(..., description="When the assignment was created")
    updated_at: datetime = Field(..., description="When the assignment was last updated")


# Reservation Assignment schemas
class ReservationAssignmentBase(BaseSchema):
    reservation_id: str = Field(..., description="ID of the assigned reservation")
    table_id: str = Field(..., description="ID of the assigned table")
    server_id: str = Field(..., description="ID of the managing server")
    notes: Optional[str] = Field(None, description="Additional notes about the assignment")


class ReservationAssignmentCreate(ReservationAssignmentBase):
    pass


class ReservationAssignmentUpdate(BaseSchema):
    status: Optional[AssignmentStatus] = Field(None, description="Current status of the assignment")
    completed_at: Optional[datetime] = Field(None, description="When the assignment was completed")
    notes: Optional[str] = Field(None, description="Additional notes about the assignment")


class ReservationAssignment(ReservationAssignmentBase):
    id: str = Field(..., description="Unique identifier for the assignment")
    assigned_at: datetime = Field(..., description="When the assignment was made")
    completed_at: Optional[datetime] = Field(None, description="When the assignment was completed")
    status: AssignmentStatus = Field(..., description="Current status of the assignment")
    created_at: datetime = Field(..., description="When the assignment was created")
    updated_at: datetime = Field(..., description="When the assignment was last updated")


# Error schemas
class Error(BaseSchema):
    message: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")
    details: Optional[dict] = Field(None, description="Additional error details")


# Response schemas
class PaginatedResponse(BaseSchema):
    items: List[dict] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    limit: int = Field(..., description="Number of items per page")
    offset: int = Field(..., description="Number of items skipped")


class TableAvailabilityResponse(BaseSchema):
    available_tables: List[Table] = Field(..., description="List of available tables")
    estimated_wait_time: Optional[int] = Field(None, description="Estimated wait time in minutes if no tables available")


class OccupancyAnalyticsResponse(BaseSchema):
    current_occupancy: float = Field(..., description="Current occupancy percentage")
    average_occupancy: float = Field(..., description="Average occupancy for the period")
    peak_hours: List[str] = Field(..., description="Peak hours")
    total_tables: int = Field(..., description="Total number of tables")
    occupied_tables: int = Field(..., description="Number of occupied tables")
