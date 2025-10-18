# API Documentation

## Overview

The Restaurant Seating System provides a comprehensive RESTful API built with FastAPI. The API follows REST principles and provides endpoints for all major system operations.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API does not implement authentication. In production, JWT-based authentication should be implemented.

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

## API Endpoints

### Restaurants

Base path: `/restaurants`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all restaurants |
| POST | `/` | Create a new restaurant |
| GET | `/{restaurant_id}` | Get restaurant by ID |
| PUT | `/{restaurant_id}` | Update restaurant |
| DELETE | `/{restaurant_id}` | Delete restaurant |
| GET | `/{restaurant_id}/sections` | Get restaurant sections |
| POST | `/{restaurant_id}/sections` | Create new section |
| GET | `/{restaurant_id}/tables` | Get restaurant tables |
| POST | `/{restaurant_id}/tables` | Create new table |
| GET | `/{restaurant_id}/analytics` | Get occupancy analytics |

### Parties

Base path: `/parties`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all parties |
| POST | `/` | Create a new party |
| GET | `/{party_id}` | Get party by ID |
| PUT | `/{party_id}` | Update party |
| DELETE | `/{party_id}` | Delete party |

### Reservations

Base path: `/reservations`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all reservations |
| POST | `/` | Create a new reservation |
| GET | `/{reservation_id}` | Get reservation by ID |
| PUT | `/{reservation_id}` | Update reservation |
| DELETE | `/{reservation_id}` | Delete reservation |

### Waiting List

Base path: `/waiting-list`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List waiting list entries |
| POST | `/` | Add to waiting list |
| GET | `/{entry_id}` | Get waiting list entry |
| PUT | `/{entry_id}` | Update waiting list entry |
| DELETE | `/{entry_id}` | Remove from waiting list |

### Servers

Base path: `/servers`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all servers |
| POST | `/` | Create a new server |
| GET | `/{server_id}` | Get server by ID |
| PUT | `/{server_id}` | Update server |
| DELETE | `/{server_id}` | Delete server |

### Assignments

Base path: `/assignments`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/table-assignments` | List table assignments |
| POST | `/table-assignments` | Create table assignment |
| GET | `/table-assignments/{assignment_id}` | Get table assignment |
| PUT | `/table-assignments/{assignment_id}` | Update table assignment |
| DELETE | `/table-assignments/{assignment_id}` | Delete table assignment |
| GET | `/reservation-assignments` | List reservation assignments |
| POST | `/reservation-assignments` | Create reservation assignment |
| GET | `/reservation-assignments/{assignment_id}` | Get reservation assignment |
| PUT | `/reservation-assignments/{assignment_id}` | Update reservation assignment |
| DELETE | `/reservation-assignments/{assignment_id}` | Delete reservation assignment |

## Data Models

### Restaurant

```json
{
  "id": "string",
  "name": "string",
  "address": "string",
  "phone": "string",
  "opening_time": "string",
  "closing_time": "string",
  "max_capacity": "integer",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Section

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "capacity": "integer",
  "is_active": "boolean",
  "restaurant_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Table

```json
{
  "id": "string",
  "table_number": "string",
  "capacity": "integer",
  "location": "string",
  "is_active": "boolean",
  "status": "AVAILABLE|OCCUPIED|RESERVED|OUT_OF_ORDER|CLEANING",
  "restaurant_id": "string",
  "section_ids": ["string"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Party

```json
{
  "id": "string",
  "name": "string",
  "size": "integer",
  "phone": "string",
  "email": "string",
  "status": "WAITING|SEATED|FINISHED|CANCELLED",
  "arrival_time": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Reservation

```json
{
  "id": "string",
  "reservation_time": "datetime",
  "party_size": "integer",
  "customer_name": "string",
  "customer_phone": "string",
  "customer_email": "string",
  "special_requests": "string",
  "status": "CONFIRMED|PENDING|CANCELLED|COMPLETED|NO_SHOW",
  "restaurant_id": "string",
  "party_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Waiting List Entry

```json
{
  "id": "string",
  "customer_name": "string",
  "customer_phone": "string",
  "party_size": "integer",
  "request_time": "datetime",
  "estimated_wait_time": "integer",
  "status": "WAITING|SEATED|CANCELLED|EXPIRED",
  "notes": "string",
  "restaurant_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Server

```json
{
  "id": "string",
  "first_name": "string",
  "last_name": "string",
  "employee_id": "string",
  "is_active": "boolean",
  "shift_start": "datetime",
  "shift_end": "datetime",
  "restaurant_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Table Assignment

```json
{
  "id": "string",
  "assigned_at": "datetime",
  "completed_at": "datetime",
  "status": "ACTIVE|COMPLETED|CANCELLED",
  "table_id": "string",
  "party_id": "string",
  "server_id": "string",
  "notes": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Reservation Assignment

```json
{
  "id": "string",
  "assigned_at": "datetime",
  "completed_at": "datetime",
  "status": "ACTIVE|COMPLETED|CANCELLED",
  "reservation_id": "string",
  "table_id": "string",
  "server_id": "string",
  "notes": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
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

- [API Reference](api-reference.md)
- [Authentication Guide](authentication.md)
- [Rate Limiting](rate-limiting.md)
- [SDK Documentation](sdk.md)
