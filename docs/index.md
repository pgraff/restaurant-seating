# Restaurant Seating System

Welcome to the Restaurant Seating System API documentation.

## Overview

The Restaurant Seating System is a comprehensive API for managing restaurant seating, reservations, and table assignments. It provides a robust solution for restaurants to handle customer flow, table management, and reservation systems.

## Features

- **Restaurant Management**: Complete CRUD operations for restaurant entities
- **Table Management**: Flexible table configuration and status tracking
- **Reservation System**: Advanced booking and reservation management
- **Waiting List**: Queue management for walk-in customers
- **Real-time Analytics**: Occupancy tracking and reporting
- **Staff Management**: Server assignment and shift tracking

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   make dev
   ```

3. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

## API Endpoints

The API is organized around RESTful principles with the following main resource groups:

- **Restaurants**: Core restaurant management
- **Tables**: Table configuration and status
- **Reservations**: Booking management
- **Parties**: Customer group management
- **Servers**: Staff management
- **Analytics**: Reporting and insights

## Authentication

The API uses JWT-based authentication. See the [Authentication Guide](api/authentication.md) for details.

## Getting Help

- Check the [API Reference](api/overview.md) for detailed endpoint documentation
- Review the [Development Guide](development/setup.md) for setup instructions
- See [Contributing](development/contributing.md) for how to contribute to the project
