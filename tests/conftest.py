"""
Pytest configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def sample_restaurant_data():
    """Sample restaurant data for testing"""
    return {
        "name": "Test Restaurant",
        "address": "123 Test Street",
        "phone": "+1-555-0123",
        "openingTime": "09:00",
        "closingTime": "22:00",
        "maxCapacity": 100
    }
