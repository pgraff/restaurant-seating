# Restaurant Seating System - Data Model

## Overview
This document defines the abstract data model for a restaurant seating system, focusing on the core entities and their relationships.

## UML Class Diagram

```mermaid
classDiagram
    class Restaurant {
        +String id
        +String name
        +String address
        +String phone
        +Time openingTime
        +Time closingTime
        +Integer maxCapacity
    }

    class Section {
        +String id
        +String name
        +String description
        +Integer capacity
        +Boolean isActive
    }

    class Table {
        +String id
        +String tableNumber
        +Integer capacity
        +String location
        +Boolean isActive
        +TableStatus status
    }

    class Party {
        +String id
        +String name
        +Integer size
        +String phone
        +String email
        +PartyStatus status
        +DateTime arrivalTime
    }

    class Reservation {
        +String id
        +DateTime reservationTime
        +Integer partySize
        +String customerName
        +String customerPhone
        +String customerEmail
        +String specialRequests
        +ReservationStatus status
        +DateTime createdAt
        +DateTime updatedAt
    }

    class WaitingList {
        +String id
        +String customerName
        +String customerPhone
        +Integer partySize
        +DateTime requestTime
        +Integer estimatedWaitTime
        +WaitingListStatus status
        +String notes
    }

    class Server {
        +String id
        +String firstName
        +String lastName
        +String employeeId
        +Boolean isActive
        +DateTime shiftStart
        +DateTime shiftEnd
    }

    class TableAssignment {
        +String id
        +DateTime assignedAt
        +DateTime completedAt
        +AssignmentStatus status
    }

    class ReservationAssignment {
        +String id
        +DateTime assignedAt
        +DateTime completedAt
        +AssignmentStatus status
    }

    %% Restaurant relationships
    Restaurant "1" -- "*" Section : contains
    Restaurant "1" -- "*" Table : has
    Restaurant "1" -- "*" Server : employs
    Restaurant "1" -- "*" Reservation : receives
    Restaurant "1" -- "1" WaitingList : maintains

    %% Section-Table many-to-many relationship
    Section "*" -- "*" Table : tags

    %% Table relationships
    Table "1" -- "*" TableAssignment : assigned_to
    Table "1" -- "*" ReservationAssignment : reserved_for

    %% Party relationships
    Party "1" -- "0..1" TableAssignment : seated_at
    %% Reservation relationships
    Reservation "1" -- "0..1" ReservationAssignment : assigned_to
    Reservation "1" -- "1" Party : for_party

    %% Server relationships
    Server "1" -- "*" TableAssignment : manages
    Server "1" -- "*" ReservationAssignment : handles

    %% WaitingList relationships
    WaitingList "0..1" -- "*" Party : represents
```

## Entity Descriptions

### Restaurant
Represents a restaurant establishment with basic information including name, address, contact details, operating hours, and maximum capacity.

### Section
Represents a logical grouping or area within the restaurant (e.g., "Patio", "Main Dining", "Bar Area"). Tables can belong to multiple sections, allowing for flexible categorization.

### Table
Represents a physical table in the restaurant with a unique identifier, capacity, location, and current status. Tables can be tagged with multiple sections.

### Party
Represents a group of customers dining together. Contains information about the party size, contact details, and current status (waiting, seated, etc.).

### Reservation
Represents a booked reservation with customer details, party size, reservation time, and special requests. Each reservation is associated with a party.

### WaitingList
Represents customers waiting for a table when the restaurant is at capacity. Contains customer information, party size, and estimated wait time.

### Server
Represents restaurant staff members who manage tables and handle reservations. Contains employee information and current shift details.

### TableAssignment
Represents the assignment of a table to a party for dining. Tracks when the assignment was made and completed.

### ReservationAssignment
Represents the assignment of a table to a reservation. Tracks the reservation fulfillment process.

## Key Design Decisions

1. **Section-Table Many-to-Many**: Tables can belong to multiple sections (e.g., a table could be both "Patio" and "Smoking Allowed")

2. **Separate Assignment Entities**: TableAssignment and ReservationAssignment track the actual seating process separately from the core entities

3. **Party as Central Entity**: Party serves as the central entity for customer groups, with both reservations and waiting list entries referencing it

4. **Status Enums**: Each entity includes status fields to track current state (e.g., TableStatus, PartyStatus, ReservationStatus)

5. **Flexible Relationships**: The model allows for various seating scenarios including walk-ins, reservations, and waiting list management
