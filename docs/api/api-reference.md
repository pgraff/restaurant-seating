# API Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API does not require authentication. In production, JWT-based authentication should be implemented.

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "data": { ... },
  "status": "success",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Error Response
```json
{
  "message": "Error description",
  "status_code": 400,
  "timestamp": "2024-01-01T12:00:00Z",
  "details": { ... }
}
```

## Endpoints

### Restaurants

#### List Restaurants

```http
GET /restaurants
```

**Query Parameters:**
- `limit` (integer, optional): Number of items per page (1-100, default: 20)
- `offset` (integer, optional): Number of items to skip (default: 0)

**Response:**
```json
{
  "items": [
    {
      "id": "string",
      "name": "string",
      "address": "string",
      "phone": "string",
      "opening_time": "string",
      "closing_time": "string",
      "max_capacity": 100,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

#### Create Restaurant

```http
POST /restaurants
```

**Request Body:**
```json
{
  "name": "string",
  "address": "string",
  "phone": "string",
  "opening_time": "string",
  "closing_time": "string",
  "max_capacity": 100
}
```

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "address": "string",
  "phone": "string",
  "opening_time": "string",
  "closing_time": "string",
  "max_capacity": 100,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get Restaurant

```http
GET /restaurants/{restaurant_id}
```

**Path Parameters:**
- `restaurant_id` (string): Restaurant ID

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "address": "string",
  "phone": "string",
  "opening_time": "string",
  "closing_time": "string",
  "max_capacity": 100,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Update Restaurant

```http
PUT /restaurants/{restaurant_id}
```

**Path Parameters:**
- `restaurant_id` (string): Restaurant ID

**Request Body:**
```json
{
  "name": "string",
  "address": "string",
  "phone": "string",
  "opening_time": "string",
  "closing_time": "string",
  "max_capacity": 100
}
```

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "address": "string",
  "phone": "string",
  "opening_time": "string",
  "closing_time": "string",
  "max_capacity": 100,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Delete Restaurant

```http
DELETE /restaurants/{restaurant_id}
```

**Path Parameters:**
- `restaurant_id` (string): Restaurant ID

**Response:**
```json
{
  "message": "Restaurant deleted successfully"
}
```

#### Get Restaurant Sections

```http
GET /restaurants/{restaurant_id}/sections
```

**Path Parameters:**
- `restaurant_id` (string): Restaurant ID

**Response:**
```json
[
  {
    "id": "string",
    "name": "string",
    "description": "string",
    "capacity": 50,
    "is_active": true,
    "restaurant_id": "string",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
]
```

#### Create Restaurant Section

```http
POST /restaurants/{restaurant_id}/sections
```

**Path Parameters:**
- `restaurant_id` (string): Restaurant ID

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "capacity": 50,
  "is_active": true
}
```

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "capacity": 50,
  "is_active": true,
  "restaurant_id": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get Restaurant Tables

```http
GET /restaurants/{restaurant_id}/tables
```

**Path Parameters:**
- `restaurant_id` (string): Restaurant ID

**Response:**
```json
[
  {
    "id": "string",
    "table_number": "string",
    "capacity": 4,
    "location": "string",
    "is_active": true,
    "status": "AVAILABLE",
    "restaurant_id": "string",
    "section_ids": ["string"],
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
]
```

#### Create Restaurant Table

```http
POST /restaurants/{restaurant_id}/tables
```

**Path Parameters:**
- `restaurant_id` (string): Restaurant ID

**Request Body:**
```json
{
  "table_number": "string",
  "capacity": 4,
  "location": "string",
  "is_active": true,
  "status": "AVAILABLE",
  "section_ids": ["string"]
}
```

**Response:**
```json
{
  "id": "string",
  "table_number": "string",
  "capacity": 4,
  "location": "string",
  "is_active": true,
  "status": "AVAILABLE",
  "restaurant_id": "string",
  "section_ids": ["string"],
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get Restaurant Analytics

```http
GET /restaurants/{restaurant_id}/analytics
```

**Path Parameters:**
- `restaurant_id` (string): Restaurant ID

**Response:**
```json
{
  "current_occupancy": 75.5,
  "average_occupancy": 68.2,
  "peak_hours": ["19:00", "20:00", "21:00"],
  "total_tables": 20,
  "occupied_tables": 15
}
```

### Parties

#### List Parties

```http
GET /parties
```

**Query Parameters:**
- `status` (string, optional): Filter by party status

**Response:**
```json
[
  {
    "id": "string",
    "name": "string",
    "size": 4,
    "phone": "string",
    "email": "string",
    "status": "WAITING",
    "arrival_time": "2024-01-01T12:00:00Z",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
]
```

#### Create Party

```http
POST /parties
```

**Request Body:**
```json
{
  "name": "string",
  "size": 4,
  "phone": "string",
  "email": "string",
  "status": "WAITING",
  "arrival_time": "2024-01-01T12:00:00Z"
}
```

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "size": 4,
  "phone": "string",
  "email": "string",
  "status": "WAITING",
  "arrival_time": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get Party

```http
GET /parties/{party_id}
```

**Path Parameters:**
- `party_id` (string): Party ID

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "size": 4,
  "phone": "string",
  "email": "string",
  "status": "WAITING",
  "arrival_time": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Update Party

```http
PUT /parties/{party_id}
```

**Path Parameters:**
- `party_id` (string): Party ID

**Request Body:**
```json
{
  "name": "string",
  "size": 4,
  "phone": "string",
  "email": "string",
  "status": "SEATED",
  "arrival_time": "2024-01-01T12:00:00Z"
}
```

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "size": 4,
  "phone": "string",
  "email": "string",
  "status": "SEATED",
  "arrival_time": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Delete Party

```http
DELETE /parties/{party_id}
```

**Path Parameters:**
- `party_id` (string): Party ID

**Response:**
```json
{
  "message": "Party deleted successfully"
}
```

### Reservations

#### List Reservations

```http
GET /reservations
```

**Query Parameters:**
- `restaurant_id` (string, optional): Filter by restaurant ID
- `status` (string, optional): Filter by reservation status
- `date` (date, optional): Filter by date (YYYY-MM-DD)

**Response:**
```json
[
  {
    "id": "string",
    "reservation_time": "2024-01-01T19:00:00Z",
    "party_size": 4,
    "customer_name": "string",
    "customer_phone": "string",
    "customer_email": "string",
    "special_requests": "string",
    "status": "CONFIRMED",
    "restaurant_id": "string",
    "party_id": "string",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
]
```

#### Create Reservation

```http
POST /reservations
```

**Request Body:**
```json
{
  "reservation_time": "2024-01-01T19:00:00Z",
  "party_size": 4,
  "customer_name": "string",
  "customer_phone": "string",
  "customer_email": "string",
  "special_requests": "string",
  "restaurant_id": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "reservation_time": "2024-01-01T19:00:00Z",
  "party_size": 4,
  "customer_name": "string",
  "customer_phone": "string",
  "customer_email": "string",
  "special_requests": "string",
  "status": "PENDING",
  "restaurant_id": "string",
  "party_id": null,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get Reservation

```http
GET /reservations/{reservation_id}
```

**Path Parameters:**
- `reservation_id` (string): Reservation ID

**Response:**
```json
{
  "id": "string",
  "reservation_time": "2024-01-01T19:00:00Z",
  "party_size": 4,
  "customer_name": "string",
  "customer_phone": "string",
  "customer_email": "string",
  "special_requests": "string",
  "status": "CONFIRMED",
  "restaurant_id": "string",
  "party_id": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Update Reservation

```http
PUT /reservations/{reservation_id}
```

**Path Parameters:**
- `reservation_id` (string): Reservation ID

**Request Body:**
```json
{
  "reservation_time": "2024-01-01T19:00:00Z",
  "party_size": 4,
  "customer_name": "string",
  "customer_phone": "string",
  "customer_email": "string",
  "special_requests": "string",
  "status": "CONFIRMED"
}
```

**Response:**
```json
{
  "id": "string",
  "reservation_time": "2024-01-01T19:00:00Z",
  "party_size": 4,
  "customer_name": "string",
  "customer_phone": "string",
  "customer_email": "string",
  "special_requests": "string",
  "status": "CONFIRMED",
  "restaurant_id": "string",
  "party_id": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Delete Reservation

```http
DELETE /reservations/{reservation_id}
```

**Path Parameters:**
- `reservation_id` (string): Reservation ID

**Response:**
```json
{
  "message": "Reservation deleted successfully"
}
```

### Waiting List

#### List Waiting List

```http
GET /waiting-list
```

**Query Parameters:**
- `restaurant_id` (string, optional): Filter by restaurant ID
- `status` (string, optional): Filter by waiting list status

**Response:**
```json
[
  {
    "id": "string",
    "customer_name": "string",
    "customer_phone": "string",
    "party_size": 4,
    "request_time": "2024-01-01T12:00:00Z",
    "estimated_wait_time": 30,
    "status": "WAITING",
    "notes": "string",
    "restaurant_id": "string",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
]
```

#### Add to Waiting List

```http
POST /waiting-list
```

**Request Body:**
```json
{
  "customer_name": "string",
  "customer_phone": "string",
  "party_size": 4,
  "estimated_wait_time": 30,
  "notes": "string",
  "restaurant_id": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "customer_name": "string",
  "customer_phone": "string",
  "party_size": 4,
  "request_time": "2024-01-01T12:00:00Z",
  "estimated_wait_time": 30,
  "status": "WAITING",
  "notes": "string",
  "restaurant_id": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get Waiting List Entry

```http
GET /waiting-list/{entry_id}
```

**Path Parameters:**
- `entry_id` (string): Waiting list entry ID

**Response:**
```json
{
  "id": "string",
  "customer_name": "string",
  "customer_phone": "string",
  "party_size": 4,
  "request_time": "2024-01-01T12:00:00Z",
  "estimated_wait_time": 30,
  "status": "WAITING",
  "notes": "string",
  "restaurant_id": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Update Waiting List Entry

```http
PUT /waiting-list/{entry_id}
```

**Path Parameters:**
- `entry_id` (string): Waiting list entry ID

**Request Body:**
```json
{
  "customer_name": "string",
  "customer_phone": "string",
  "party_size": 4,
  "estimated_wait_time": 30,
  "status": "SEATED",
  "notes": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "customer_name": "string",
  "customer_phone": "string",
  "party_size": 4,
  "request_time": "2024-01-01T12:00:00Z",
  "estimated_wait_time": 30,
  "status": "SEATED",
  "notes": "string",
  "restaurant_id": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Remove from Waiting List

```http
DELETE /waiting-list/{entry_id}
```

**Path Parameters:**
- `entry_id` (string): Waiting list entry ID

**Response:**
```json
{
  "message": "Waiting list entry removed successfully"
}
```

### Servers

#### List Servers

```http
GET /servers
```

**Query Parameters:**
- `restaurant_id` (string, optional): Filter by restaurant ID
- `is_active` (boolean, optional): Filter by active status

**Response:**
```json
[
  {
    "id": "string",
    "first_name": "string",
    "last_name": "string",
    "employee_id": "string",
    "is_active": true,
    "shift_start": "2024-01-01T09:00:00Z",
    "shift_end": "2024-01-01T17:00:00Z",
    "restaurant_id": "string",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
]
```

#### Create Server

```http
POST /servers
```

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "employee_id": "string",
  "is_active": true,
  "shift_start": "2024-01-01T09:00:00Z",
  "shift_end": "2024-01-01T17:00:00Z",
  "restaurant_id": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "first_name": "string",
  "last_name": "string",
  "employee_id": "string",
  "is_active": true,
  "shift_start": "2024-01-01T09:00:00Z",
  "shift_end": "2024-01-01T17:00:00Z",
  "restaurant_id": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Get Server

```http
GET /servers/{server_id}
```

**Path Parameters:**
- `server_id` (string): Server ID

**Response:**
```json
{
  "id": "string",
  "first_name": "string",
  "last_name": "string",
  "employee_id": "string",
  "is_active": true,
  "shift_start": "2024-01-01T09:00:00Z",
  "shift_end": "2024-01-01T17:00:00Z",
  "restaurant_id": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Update Server

```http
PUT /servers/{server_id}
```

**Path Parameters:**
- `server_id` (string): Server ID

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "employee_id": "string",
  "is_active": true,
  "shift_start": "2024-01-01T09:00:00Z",
  "shift_end": "2024-01-01T17:00:00Z"
}
```

**Response:**
```json
{
  "id": "string",
  "first_name": "string",
  "last_name": "string",
  "employee_id": "string",
  "is_active": true,
  "shift_start": "2024-01-01T09:00:00Z",
  "shift_end": "2024-01-01T17:00:00Z",
  "restaurant_id": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Delete Server

```http
DELETE /servers/{server_id}
```

**Path Parameters:**
- `server_id` (string): Server ID

**Response:**
```json
{
  "message": "Server deleted successfully"
}
```

### Assignments

#### Table Assignments

##### List Table Assignments

```http
GET /assignments/table-assignments
```

**Query Parameters:**
- `table_id` (string, optional): Filter by table ID
- `party_id` (string, optional): Filter by party ID
- `server_id` (string, optional): Filter by server ID
- `status` (string, optional): Filter by assignment status

**Response:**
```json
[
  {
    "id": "string",
    "assigned_at": "2024-01-01T12:00:00Z",
    "completed_at": null,
    "status": "ACTIVE",
    "table_id": "string",
    "party_id": "string",
    "server_id": "string",
    "notes": "string",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
]
```

##### Create Table Assignment

```http
POST /assignments/table-assignments
```

**Request Body:**
```json
{
  "table_id": "string",
  "party_id": "string",
  "server_id": "string",
  "notes": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "assigned_at": "2024-01-01T12:00:00Z",
  "completed_at": null,
  "status": "ACTIVE",
  "table_id": "string",
  "party_id": "string",
  "server_id": "string",
  "notes": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

##### Get Table Assignment

```http
GET /assignments/table-assignments/{assignment_id}
```

**Path Parameters:**
- `assignment_id` (string): Assignment ID

**Response:**
```json
{
  "id": "string",
  "assigned_at": "2024-01-01T12:00:00Z",
  "completed_at": null,
  "status": "ACTIVE",
  "table_id": "string",
  "party_id": "string",
  "server_id": "string",
  "notes": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

##### Update Table Assignment

```http
PUT /assignments/table-assignments/{assignment_id}
```

**Path Parameters:**
- `assignment_id` (string): Assignment ID

**Request Body:**
```json
{
  "status": "COMPLETED",
  "completed_at": "2024-01-01T14:00:00Z",
  "notes": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "assigned_at": "2024-01-01T12:00:00Z",
  "completed_at": "2024-01-01T14:00:00Z",
  "status": "COMPLETED",
  "table_id": "string",
  "party_id": "string",
  "server_id": "string",
  "notes": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

##### Delete Table Assignment

```http
DELETE /assignments/table-assignments/{assignment_id}
```

**Path Parameters:**
- `assignment_id` (string): Assignment ID

**Response:**
```json
{
  "message": "Table assignment deleted successfully"
}
```

#### Reservation Assignments

##### List Reservation Assignments

```http
GET /assignments/reservation-assignments
```

**Query Parameters:**
- `reservation_id` (string, optional): Filter by reservation ID
- `table_id` (string, optional): Filter by table ID
- `server_id` (string, optional): Filter by server ID
- `status` (string, optional): Filter by assignment status

**Response:**
```json
[
  {
    "id": "string",
    "assigned_at": "2024-01-01T12:00:00Z",
    "completed_at": null,
    "status": "ACTIVE",
    "reservation_id": "string",
    "table_id": "string",
    "server_id": "string",
    "notes": "string",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
]
```

##### Create Reservation Assignment

```http
POST /assignments/reservation-assignments
```

**Request Body:**
```json
{
  "reservation_id": "string",
  "table_id": "string",
  "server_id": "string",
  "notes": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "assigned_at": "2024-01-01T12:00:00Z",
  "completed_at": null,
  "status": "ACTIVE",
  "reservation_id": "string",
  "table_id": "string",
  "server_id": "string",
  "notes": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

##### Get Reservation Assignment

```http
GET /assignments/reservation-assignments/{assignment_id}
```

**Path Parameters:**
- `assignment_id` (string): Assignment ID

**Response:**
```json
{
  "id": "string",
  "assigned_at": "2024-01-01T12:00:00Z",
  "completed_at": null,
  "status": "ACTIVE",
  "reservation_id": "string",
  "table_id": "string",
  "server_id": "string",
  "notes": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

##### Update Reservation Assignment

```http
PUT /assignments/reservation-assignments/{assignment_id}
```

**Path Parameters:**
- `assignment_id` (string): Assignment ID

**Request Body:**
```json
{
  "status": "COMPLETED",
  "completed_at": "2024-01-01T14:00:00Z",
  "notes": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "assigned_at": "2024-01-01T12:00:00Z",
  "completed_at": "2024-01-01T14:00:00Z",
  "status": "COMPLETED",
  "reservation_id": "string",
  "table_id": "string",
  "server_id": "string",
  "notes": "string",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

##### Delete Reservation Assignment

```http
DELETE /assignments/reservation-assignments/{assignment_id}
```

**Path Parameters:**
- `assignment_id` (string): Assignment ID

**Response:**
```json
{
  "message": "Reservation assignment deleted successfully"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

## Status Codes

### Table Status
- `AVAILABLE` - Table is free and ready for seating
- `OCCUPIED` - Table is currently in use
- `RESERVED` - Table is reserved for a specific time
- `OUT_OF_ORDER` - Table is not available due to maintenance
- `CLEANING` - Table is being cleaned after use

### Party Status
- `WAITING` - Party is waiting for a table
- `SEATED` - Party has been seated at a table
- `FINISHED` - Party has finished dining
- `CANCELLED` - Party cancelled their visit

### Reservation Status
- `CONFIRMED` - Reservation is confirmed
- `PENDING` - Reservation is pending confirmation
- `CANCELLED` - Reservation was cancelled
- `COMPLETED` - Reservation was completed
- `NO_SHOW` - Customer didn't show up

### Waiting List Status
- `WAITING` - Customer is waiting for a table
- `SEATED` - Customer has been seated
- `CANCELLED` - Customer cancelled their wait
- `EXPIRED` - Wait time expired

### Assignment Status
- `ACTIVE` - Assignment is currently active
- `COMPLETED` - Assignment has been completed
- `CANCELLED` - Assignment was cancelled

## Rate Limiting

Currently, no rate limiting is implemented. In production, rate limiting should be added to prevent abuse.

## Pagination

List endpoints support pagination:

```
GET /api/v1/restaurants?limit=20&offset=0
```

**Parameters:**
- `limit`: Number of items per page (1-100, default: 20)
- `offset`: Number of items to skip (default: 0)

**Response:**
```json
{
  "items": [...],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

## Filtering

Many endpoints support filtering:

```
GET /api/v1/parties?status=WAITING
GET /api/v1/reservations?restaurant_id=123&date=2024-01-01
```

## Sorting

Currently, no explicit sorting is supported. Results are returned in creation order.

## API Versioning

The API uses URL versioning:
- Current version: `v1`
- Base path: `/api/v1`

## Interactive Documentation

The API provides interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## SDK and Client Libraries

### Python Client

A Python client is provided in `frontend/api_client.py`:

```python
from api_client import RestaurantAPIClient

client = RestaurantAPIClient(base_url="http://localhost:8000")

# Get all restaurants
restaurants = client.get_restaurants()

# Create a new party
party = client.create_party({
    "name": "Smith Party",
    "size": 4,
    "phone": "+1234567890"
})
```

## Testing

### Health Check

```
GET /health
```

Returns system health status.

### Example Requests

#### Create a Restaurant

```bash
curl -X POST "http://localhost:8000/api/v1/restaurants" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "The Bistro",
    "address": "123 Main St, City, State 12345",
    "phone": "+1234567890",
    "opening_time": "09:00:00",
    "closing_time": "22:00:00",
    "max_capacity": 100
  }'
```

#### Create a Party

```bash
curl -X POST "http://localhost:8000/api/v1/parties" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smith Party",
    "size": 4,
    "phone": "+1234567890",
    "email": "smith@example.com"
  }'
```

#### Create a Reservation

```bash
curl -X POST "http://localhost:8000/api/v1/reservations" \
  -H "Content-Type: application/json" \
  -d '{
    "reservation_time": "2024-01-01T19:00:00Z",
    "party_size": 4,
    "customer_name": "John Smith",
    "customer_phone": "+1234567890",
    "customer_email": "john@example.com",
    "restaurant_id": "restaurant-uuid"
  }'
```

## Next Steps

- [API Overview](overview.md)
- [Authentication Guide](authentication.md)
- [Rate Limiting](rate-limiting.md)
- [SDK Documentation](sdk.md)
