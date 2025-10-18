# Contributing Guide

## Overview

Thank you for your interest in contributing to the Restaurant Seating System! This guide will help you get started with contributing to the project.

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/yourusername/restaurant-seating-system.git
cd restaurant-seating-system

# Add upstream remote
git remote add upstream https://github.com/originalowner/restaurant-seating-system.git
```

### 2. Development Setup

```bash
# Create development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Start development environment
make dev
```

### 3. Create a Branch

```bash
# Create a new branch for your feature
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/your-bug-description
```

## Development Workflow

### 1. Code Style

We use several tools to maintain code quality:

#### Black (Code Formatting)
```bash
# Format code
black backend/ frontend/ tests/

# Check formatting
black --check backend/ frontend/ tests/
```

#### isort (Import Sorting)
```bash
# Sort imports
isort backend/ frontend/ tests/

# Check import sorting
isort --check-only backend/ frontend/ tests/
```

#### Flake8 (Linting)
```bash
# Lint code
flake8 backend/ frontend/ tests/

# Lint with specific configuration
flake8 --config=setup.cfg backend/ frontend/ tests/
```

#### MyPy (Type Checking)
```bash
# Type check
mypy backend/

# Type check with strict mode
mypy --strict backend/
```

### 2. Testing

#### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=backend tests/

# Run tests in watch mode
pytest-watch tests/
```

#### Test Coverage
```bash
# Generate coverage report
pytest --cov=backend --cov-report=html tests/

# View coverage report
open htmlcov/index.html
```

### 3. Database Changes

#### Create Migrations
```bash
# Create a new migration
cd backend
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

#### Test Database Changes
```bash
# Test with fresh database
pytest --test-db tests/

# Test specific migration
alembic upgrade head
pytest tests/test_models.py
```

## Pull Request Process

### 1. Before Submitting

- [ ] Code follows the project's style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] No merge conflicts with main branch

### 2. Commit Messages

Follow the conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add table availability endpoint
fix(database): resolve foreign key constraint issue
docs(readme): update installation instructions
test(services): add unit tests for party service
```

### 3. Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
```

### 4. Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and checks
2. **Code Review**: At least one maintainer reviews the code
3. **Testing**: Manual testing may be required
4. **Approval**: Maintainer approves the PR
5. **Merge**: PR is merged into main branch

## Code Standards

### 1. Python Code Style

#### Function and Variable Naming
```python
# Good: snake_case for functions and variables
def create_restaurant(restaurant_data):
    restaurant_id = generate_uuid()
    return restaurant

# Good: PascalCase for classes
class RestaurantService:
    pass

# Good: UPPER_CASE for constants
MAX_CAPACITY = 100
```

#### Docstrings
```python
def create_restaurant(self, restaurant_data: RestaurantCreate) -> Restaurant:
    """
    Create a new restaurant.
    
    Args:
        restaurant_data: Restaurant data for creation
        
    Returns:
        Created restaurant object
        
    Raises:
        ValueError: If restaurant data is invalid
        SQLAlchemyError: If database operation fails
    """
    pass
```

#### Type Hints
```python
from typing import List, Optional, Dict, Any

def get_restaurants(
    self, 
    limit: int = 20, 
    offset: int = 0
) -> List[Restaurant]:
    """Get restaurants with pagination."""
    pass
```

### 2. API Design

#### RESTful Endpoints
```python
# Good: RESTful design
@router.get("/restaurants/{restaurant_id}")
@router.post("/restaurants")
@router.put("/restaurants/{restaurant_id}")
@router.delete("/restaurants/{restaurant_id}")

# Good: Nested resources
@router.get("/restaurants/{restaurant_id}/tables")
@router.post("/restaurants/{restaurant_id}/tables")
```

#### Error Handling
```python
# Good: Specific error responses
@router.get("/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: str, db: Session = Depends(get_db)):
    restaurant = service.get_restaurant(restaurant_id)
    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )
    return restaurant
```

### 3. Database Design

#### Model Relationships
```python
# Good: Clear relationships
class Restaurant(Base):
    __tablename__ = "restaurants"
    
    # One-to-many relationships
    tables = relationship("Table", back_populates="restaurant")
    servers = relationship("Server", back_populates="restaurant")
```

#### Constraints
```python
# Good: Database constraints
class Table(Base):
    __tablename__ = "tables"
    
    table_number = Column(VARCHAR(50), nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)
    status = Column(SQLEnum(TableStatus), default=TableStatus.AVAILABLE)
```

## Testing Guidelines

### 1. Unit Tests

```python
def test_create_restaurant_success(test_db_session, sample_restaurant_data):
    """Test successful restaurant creation."""
    service = RestaurantService(test_db_session)
    restaurant_data = RestaurantCreate(**sample_restaurant_data)
    
    restaurant = service.create_restaurant(restaurant_data)
    
    assert restaurant.name == sample_restaurant_data["name"]
    assert restaurant.id is not None
    assert restaurant.created_at is not None

def test_create_restaurant_validation_error(test_db_session):
    """Test restaurant creation with invalid data."""
    service = RestaurantService(test_db_session)
    
    with pytest.raises(ValidationError):
        service.create_restaurant({"name": ""})  # Empty name should fail
```

### 2. Integration Tests

```python
def test_restaurant_api_integration(test_client, sample_restaurant_data):
    """Test restaurant API integration."""
    # Create restaurant
    response = test_client.post("/api/v1/restaurants", json=sample_restaurant_data)
    assert response.status_code == 201
    
    restaurant_id = response.json()["id"]
    
    # Get restaurant
    response = test_client.get(f"/api/v1/restaurants/{restaurant_id}")
    assert response.status_code == 200
    assert response.json()["name"] == sample_restaurant_data["name"]
```

### 3. Test Data Management

```python
@pytest.fixture
def sample_restaurant_data():
    """Sample restaurant data for testing."""
    return {
        "name": "Test Restaurant",
        "address": "123 Test St",
        "phone": "+1234567890",
        "opening_time": "09:00:00",
        "closing_time": "22:00:00",
        "max_capacity": 100
    }

@pytest.fixture
def restaurant_with_tables(test_db_session, sample_restaurant_data):
    """Create restaurant with sample tables."""
    service = RestaurantService(test_db_session)
    restaurant = service.create_restaurant(sample_restaurant_data)
    
    # Create tables
    tables = []
    for i in range(3):
        table = service.create_table({
            "table_number": f"T{i+1}",
            "capacity": 4,
            "location": f"Section {i+1}",
            "restaurant_id": restaurant.id
        })
        tables.append(table)
    
    return {"restaurant": restaurant, "tables": tables}
```

## Documentation Standards

### 1. Code Documentation

#### Module Docstrings
```python
"""
Restaurant service layer.

This module provides business logic for restaurant operations including
CRUD operations, analytics, and table management.
"""
```

#### Class Docstrings
```python
class RestaurantService:
    """
    Service for restaurant operations.
    
    This service handles all restaurant-related business logic including
    creation, updates, deletion, and analytics.
    """
```

### 2. API Documentation

#### Endpoint Documentation
```python
@router.post("/restaurants", response_model=Restaurant, status_code=201)
async def create_restaurant(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new restaurant.
    
    This endpoint creates a new restaurant with the provided data.
    The restaurant will be assigned a unique ID and timestamps.
    
    Args:
        restaurant_data: Restaurant creation data
        db: Database session
        
    Returns:
        Created restaurant object
        
    Raises:
        HTTPException: If validation fails or database error occurs
    """
```

### 3. README Updates

When adding new features, update the README:

```markdown
## New Features

### Table Availability API
- Added endpoint to check table availability
- Supports filtering by date and party size
- Returns estimated wait times

### Usage
```python
# Check table availability
response = client.get("/api/v1/restaurants/{id}/tables/availability")
```
```

## Issue Reporting

### 1. Bug Reports

When reporting bugs, include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, etc.
- **Screenshots**: If applicable

### 2. Feature Requests

When requesting features, include:

- **Description**: Clear description of the feature
- **Use Case**: Why this feature is needed
- **Proposed Solution**: How you think it should work
- **Alternatives**: Other solutions considered

### 3. Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed

## Release Process

### 1. Version Numbering

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### 2. Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] CHANGELOG updated
- [ ] Release notes prepared
- [ ] Tag created

### 3. Changelog

Update `CHANGELOG.md` with:

```markdown
## [1.1.0] - 2024-01-01

### Added
- Table availability API endpoint
- Real-time occupancy analytics
- Bulk table assignment feature

### Changed
- Improved error messages
- Updated API documentation

### Fixed
- Fixed table status update bug
- Resolved memory leak in analytics
```

## Community Guidelines

### 1. Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the golden rule

### 2. Communication

- Use clear, concise language
- Provide context for questions
- Be patient with newcomers
- Ask questions when unsure

### 3. Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

## Getting Help

### 1. Documentation

- Check existing documentation first
- Look for similar issues in GitHub
- Review code examples

### 2. Community Support

- GitHub Discussions for questions
- GitHub Issues for bugs and features
- Pull requests for code contributions

### 3. Maintainer Contact

For urgent issues or questions:
- Create a GitHub issue
- Tag maintainers in comments
- Use appropriate labels

## Next Steps

- [Development Setup](setup.md)
- [Testing Guide](testing.md)
- [API Documentation](../api/overview.md)
- [Deployment Guide](../deployment/overview.md)
