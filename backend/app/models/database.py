"""
SQLAlchemy database models
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.database.connection import Base
from app.models.schemas import (
    TableStatus, PartyStatus, ReservationStatus, 
    WaitingListStatus, AssignmentStatus
)


def generate_uuid():
    """Generate a UUID string"""
    return str(uuid.uuid4())


class Restaurant(Base):
    """Restaurant model"""
    __tablename__ = "restaurants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(VARCHAR(255), nullable=False)
    address = Column(TEXT, nullable=False)
    phone = Column(VARCHAR(20), nullable=False)
    opening_time = Column(VARCHAR(8), nullable=False)  # HH:MM:SS format
    closing_time = Column(VARCHAR(8), nullable=False)  # HH:MM:SS format
    max_capacity = Column(Integer, nullable=False)
    created_at = Column(DATETIME, default=func.now(), nullable=False)
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    sections = relationship("Section", back_populates="restaurant", cascade="all, delete-orphan")
    tables = relationship("Table", back_populates="restaurant", cascade="all, delete-orphan")
    servers = relationship("Server", back_populates="restaurant", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="restaurant", cascade="all, delete-orphan")
    waiting_list = relationship("WaitingList", back_populates="restaurant", cascade="all, delete-orphan")


class Section(Base):
    """Section model"""
    __tablename__ = "sections"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(VARCHAR(255), nullable=False)
    description = Column(TEXT, nullable=True)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    restaurant_id = Column(String(36), ForeignKey("restaurants.id"), nullable=False)
    created_at = Column(DATETIME, default=func.now(), nullable=False)
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="sections")
    table_sections = relationship("TableSection", back_populates="section", cascade="all, delete-orphan")


class Table(Base):
    """Table model"""
    __tablename__ = "tables"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    table_number = Column(VARCHAR(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(TEXT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    status = Column(SQLEnum(TableStatus), default=TableStatus.AVAILABLE, nullable=False)
    restaurant_id = Column(String(36), ForeignKey("restaurants.id"), nullable=False)
    created_at = Column(DATETIME, default=func.now(), nullable=False)
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="tables")
    table_sections = relationship("TableSection", back_populates="table", cascade="all, delete-orphan")
    table_assignments = relationship("TableAssignment", back_populates="table", cascade="all, delete-orphan")
    reservation_assignments = relationship("ReservationAssignment", back_populates="table", cascade="all, delete-orphan")


class TableSection(Base):
    """Many-to-many relationship between tables and sections"""
    __tablename__ = "table_sections"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    table_id = Column(String(36), ForeignKey("tables.id"), nullable=False)
    section_id = Column(String(36), ForeignKey("sections.id"), nullable=False)
    created_at = Column(DATETIME, default=func.now(), nullable=False)

    # Relationships
    table = relationship("Table", back_populates="table_sections")
    section = relationship("Section", back_populates="table_sections")


class Party(Base):
    """Party model"""
    __tablename__ = "parties"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(VARCHAR(255), nullable=False)
    size = Column(Integer, nullable=False)
    phone = Column(VARCHAR(20), nullable=True)
    email = Column(VARCHAR(255), nullable=True)
    status = Column(SQLEnum(PartyStatus), default=PartyStatus.WAITING, nullable=False)
    arrival_time = Column(DATETIME, default=func.now(), nullable=False)
    created_at = Column(DATETIME, default=func.now(), nullable=False)
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    table_assignments = relationship("TableAssignment", back_populates="party", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="party", cascade="all, delete-orphan")


class Reservation(Base):
    """Reservation model"""
    __tablename__ = "reservations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    reservation_time = Column(DATETIME, nullable=False)
    party_size = Column(Integer, nullable=False)
    customer_name = Column(VARCHAR(255), nullable=False)
    customer_phone = Column(VARCHAR(20), nullable=False)
    customer_email = Column(VARCHAR(255), nullable=True)
    special_requests = Column(TEXT, nullable=True)
    status = Column(SQLEnum(ReservationStatus), default=ReservationStatus.PENDING, nullable=False)
    restaurant_id = Column(String(36), ForeignKey("restaurants.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=True)
    created_at = Column(DATETIME, default=func.now(), nullable=False)
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="reservations")
    party = relationship("Party", back_populates="reservations")
    reservation_assignments = relationship("ReservationAssignment", back_populates="reservation", cascade="all, delete-orphan")


class WaitingList(Base):
    """Waiting list model"""
    __tablename__ = "waiting_list"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_name = Column(VARCHAR(255), nullable=False)
    customer_phone = Column(VARCHAR(20), nullable=False)
    party_size = Column(Integer, nullable=False)
    request_time = Column(DATETIME, default=func.now(), nullable=False)
    estimated_wait_time = Column(Integer, nullable=True)
    status = Column(SQLEnum(WaitingListStatus), default=WaitingListStatus.WAITING, nullable=False)
    notes = Column(TEXT, nullable=True)
    restaurant_id = Column(String(36), ForeignKey("restaurants.id"), nullable=False)
    created_at = Column(DATETIME, default=func.now(), nullable=False)
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="waiting_list")


class Server(Base):
    """Server model"""
    __tablename__ = "servers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=False)
    employee_id = Column(VARCHAR(50), nullable=False, unique=True)
    is_active = Column(Boolean, default=True, nullable=False)
    shift_start = Column(DATETIME, nullable=True)
    shift_end = Column(DATETIME, nullable=True)
    restaurant_id = Column(String(36), ForeignKey("restaurants.id"), nullable=False)
    created_at = Column(DATETIME, default=func.now(), nullable=False)
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="servers")
    table_assignments = relationship("TableAssignment", back_populates="server", cascade="all, delete-orphan")
    reservation_assignments = relationship("ReservationAssignment", back_populates="server", cascade="all, delete-orphan")


class TableAssignment(Base):
    """Table assignment model"""
    __tablename__ = "table_assignments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    assigned_at = Column(DATETIME, default=func.now(), nullable=False)
    completed_at = Column(DATETIME, nullable=True)
    status = Column(SQLEnum(AssignmentStatus), default=AssignmentStatus.ACTIVE, nullable=False)
    table_id = Column(String(36), ForeignKey("tables.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    server_id = Column(String(36), ForeignKey("servers.id"), nullable=False)
    notes = Column(TEXT, nullable=True)
    created_at = Column(DATETIME, default=func.now(), nullable=False)
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    table = relationship("Table", back_populates="table_assignments")
    party = relationship("Party", back_populates="table_assignments")
    server = relationship("Server", back_populates="table_assignments")


class ReservationAssignment(Base):
    """Reservation assignment model"""
    __tablename__ = "reservation_assignments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    assigned_at = Column(DATETIME, default=func.now(), nullable=False)
    completed_at = Column(DATETIME, nullable=True)
    status = Column(SQLEnum(AssignmentStatus), default=AssignmentStatus.ACTIVE, nullable=False)
    reservation_id = Column(String(36), ForeignKey("reservations.id"), nullable=False)
    table_id = Column(String(36), ForeignKey("tables.id"), nullable=False)
    server_id = Column(String(36), ForeignKey("servers.id"), nullable=False)
    notes = Column(TEXT, nullable=True)
    created_at = Column(DATETIME, default=func.now(), nullable=False)
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    reservation = relationship("Reservation", back_populates="reservation_assignments")
    table = relationship("Table", back_populates="reservation_assignments")
    server = relationship("Server", back_populates="reservation_assignments")
