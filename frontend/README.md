# Restaurant Seating System - Streamlit Frontend

A modern web-based frontend for the Restaurant Seating System built with Streamlit.

## Features

### 🏠 Dashboard
- Overview of restaurant status and metrics
- Current table occupancy rates
- Today's reservations summary
- Quick access to main functions

### 📅 Reservations Management
- **View Reservations**: Browse all reservations with filtering by date and status
- **Add New Reservation**: Create new reservations with customer details
- **Edit Reservations**: Update existing reservation information
- **Cancel Reservations**: Cancel or delete reservations

### 🪑 Table Assignment
- **Current Assignments**: View all currently occupied tables
- **Assign Tables**: Seat parties at available tables
- **Available Tables**: Monitor table status and availability
- **Table Management**: Update table status and information

### ⏳ Waiting List Management
- **Current Waiting List**: View all parties waiting to be seated
- **Add to Waiting List**: Add walk-in customers to the waiting list
- **Seat Next Party**: Automatically seat the next party when tables become available
- **Wait Time Management**: Update estimated wait times

### ⚙️ Configuration
- **Restaurant Setup**: Configure restaurant details, hours, and capacity
- **Section Management**: Create and manage restaurant sections
- **Table Configuration**: Set up tables with locations and capacities
- **Server Management**: Add and manage restaurant staff

## Getting Started

### Prerequisites
- Python 3.8+
- Streamlit
- Running Restaurant Seating System API backend

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the frontend:
```bash
streamlit run streamlit_app.py
```

3. Open your browser to `http://localhost:8501`

### Using Docker

The frontend is included in the Docker Compose setup:

```bash
# Start all services (database, API, frontend)
docker-compose up -d

# View logs
docker-compose logs -f streamlit

# Stop all services
docker-compose down
```

The frontend will be available at `http://localhost:8501`

### Development

For development with hot reloading:

```bash
# Run just the frontend
make frontend

# Run both backend and frontend
make dev-full
```

## Architecture

### File Structure
```
frontend/
├── streamlit_app.py          # Main application entry point
├── api_client.py             # API client for backend communication
├── pages/                    # Individual page modules
│   ├── __init__.py
│   ├── dashboard.py          # Dashboard overview
│   ├── reservations.py       # Reservation management
│   ├── table_assignment.py   # Table assignment interface
│   ├── waiting_list.py       # Waiting list management
│   └── configuration.py      # System configuration
└── README.md                 # This file
```

### API Integration

The frontend communicates with the backend API through the `RestaurantAPIClient` class, which provides:
- RESTful API calls to all backend endpoints
- Error handling and user feedback
- Data transformation between frontend and backend formats

### Key Components

1. **Main App** (`streamlit_app.py`): Entry point with navigation and styling
2. **API Client** (`api_client.py`): Handles all backend communication
3. **Page Modules**: Individual pages for different functionality areas
4. **Shared Styling**: Custom CSS for professional appearance

## Usage Guide

### First Time Setup

1. **Configure Restaurant**: Go to Configuration → Restaurants and create your restaurant
2. **Add Sections**: Create restaurant sections (e.g., "Main Dining", "Patio")
3. **Set Up Tables**: Add tables with appropriate capacities and locations
4. **Add Servers**: Register your restaurant staff

### Daily Operations

1. **Dashboard**: Check current status and occupancy
2. **Reservations**: Manage incoming reservations
3. **Table Assignment**: Seat parties as they arrive
4. **Waiting List**: Manage walk-in customers when full

### Managing Reservations

- **Adding**: Use the "Add New Reservation" tab
- **Viewing**: Filter by date and status in the "View Reservations" tab
- **Editing**: Click "Edit" on any reservation
- **Canceling**: Use the "Cancel" button to cancel reservations

### Table Management

- **Assigning**: Select available table, party, and server
- **Status Updates**: Change table status (Available, Occupied, Cleaning, etc.)
- **Monitoring**: View real-time table status

### Waiting List Operations

- **Adding Customers**: Use the "Add to Waiting List" form
- **Seating**: Use "Seat Next Party" when tables become available
- **Monitoring**: Track wait times and queue position

## Customization

### Styling
The app uses custom CSS defined in `streamlit_app.py`. You can modify the styles by editing the `st.markdown()` call with the CSS.

### API Configuration
The API client is configured to connect to `http://localhost:8000/api/v1` by default. To change this, modify the `base_url` parameter in the `RestaurantAPIClient` constructor.

### Adding New Pages
1. Create a new Python file in the `pages/` directory
2. Implement a `show()` function
3. Import and add the page to the navigation in `streamlit_app.py`

## Troubleshooting

### Common Issues

1. **API Connection Error**: Ensure the backend API is running on port 8000
2. **No Data Displayed**: Check that you have configured restaurants, tables, and servers
3. **Permission Errors**: Ensure the frontend has proper file permissions

### Debug Mode

To run in debug mode with more verbose logging:

```bash
streamlit run streamlit_app.py --logger.level=debug
```

## Contributing

1. Follow the existing code structure and patterns
2. Add proper error handling and user feedback
3. Test all functionality before submitting changes
4. Update documentation as needed

## License

This project is part of the Restaurant Seating System and follows the same license terms.
