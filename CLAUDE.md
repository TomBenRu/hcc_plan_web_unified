# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hcc_plan_web_unified** is a modern, collaborative scheduling web application for theater clown teams and similar organizations. It unifies features from three existing projects:
- **Design & UX**: From `appointment_plan_api_cl` (modern dark theme with Tailwind CSS)
- **Features**: From `hcc_plan_api` (availability tracking, APScheduler, email system)
- **Collaboration**: New features for team-based planning workflows

This is an early-stage project currently in Phase 1 (Foundation & Setup) with only basic FastAPI structure in place.

## Commands

### Development

```bash
# Start development server with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run with uv
uv run uvicorn main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=api --cov=database --cov-report=html

# Run specific test file
pytest tests/unit/services/test_exchange_proposal_service.py
```

### Code Quality

```bash
# Format code with Black (line length: 100)
black .

# Sort imports with isort
isort .

# Type check with mypy
mypy api database

# Run all quality checks (recommended before commit)
black . && isort . && mypy api database && pytest
```

### Database Management

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Seed database with test data
python scripts/seed_database.py

# Create admin user
python scripts/create_admin.py
```

### Environment Setup

```bash
# Create virtual environment
uv venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source .venv/bin/activate

# Install dependencies
uv sync

# Install with dev dependencies
uv sync --extra dev
```

## Architecture

### Layered Architecture

The project follows a strict layered architecture:

1. **Presentation Layer** (`api/routes/`)
   - `api/`: JSON API endpoints for programmatic access
   - `web/`: HTML rendering routes for browser (actor/, cvo/, dispatcher/, admin/)
   - `websockets/`: Real-time communication endpoints

2. **Business Logic Layer** (`api/services/`)
   - All business logic lives here, NOT in routes
   - One service per entity (e.g., `AppointmentService`, `ExchangeProposalService`)
   - Services are stateless with static methods
   - Use `@db_session` decorator for database operations

3. **Data Access Layer** (`database/models/`)
   - PonyORM entities define database schema
   - Entities act as repositories
   - Handle all database interactions

4. **Cross-Cutting Concerns**
   - `api/middleware/`: CORS, error handling, logging
   - `api/exceptions/`: Domain-specific exceptions
   - `api/utils/`: Helper functions
   - `scheduler/`: Background jobs with APScheduler

### Service Layer Pattern

**Critical**: Routes are thin adapters. All business logic goes in services.

```python
# Good - Business logic in service
class ExchangeProposalService:
    @staticmethod
    @db_session
    def create_proposal(proposer_id: UUID, ...) -> ExchangeProposal:
        # Validation
        # Business logic
        # Notifications
        return proposal

# Bad - Business logic in route (DO NOT DO THIS)
@router.post("/proposals")
async def create_proposal(...):
    proposal = ExchangeProposal(...)  # Direct DB access - WRONG
```

### Exception-Driven Development

- Use domain-specific exceptions in `api/exceptions/`
- Never raise generic `Exception` in business logic
- Global exception handlers in middleware convert to HTTP responses

```python
# api/exceptions/exchange_proposal.py
class ExchangeProposalError(Exception):
    """Base exception for exchange proposals"""
    pass

class InvalidProposalError(ExchangeProposalError):
    """Proposal is invalid"""
    http_status = 400
```

## Key Entities & Relationships

### Core Entities
- **User**: Authentication (email, hashed_password)
- **Person**: Profile data (f_name, l_name), linked to User
- **Team**: Groups of actors with a dispatcher
- **Project**: Top-level container for teams and persons

### Planning Entities
- **PlanPeriod**: Time period for scheduling (start_date, end_date)
- **Plan**: Collection of appointments for a period
- **Appointment**: Single scheduled event (date, time, location, persons)
- **LocationOfWork**: Venue with address

### Availability System
- **Availables**: Actor's availability for a PlanPeriod
- **AvailDay**: Specific available date with time_of_day

### Collaboration (New Features)
- **PlanVersion**: Versioning (draft → in_review → approved → final)
- **ExchangeProposal**: Actor proposes to swap appointments
- **CvORole**: Chief responsible for locations, approves proposals
- **Notification**: Push notifications for real-time updates

## Code Style

### Language & Conventions
- **Python 3.12+** with modern type hints
- **German comments and docstrings** (code in English)
- **snake_case** for functions/variables, **PascalCase** for classes
- **UPPER_CASE** for constants

### Pydantic Schemas
Use suffix conventions:
- `Create` for POST requests (e.g., `ExchangeProposalCreate`)
- `Update` for PUT/PATCH requests (e.g., `ExchangeProposalUpdate`)
- `Response` for API responses (e.g., `ExchangeProposalResponse`)
- Base schema without suffix for shared fields

### PonyORM Important Note
```python
from typing import Optional  # For type hints
from pony.orm import Optional as PonyOptional  # For PonyORM entities

# In PonyORM entities, use PonyOptional for nullable fields:
class ExchangeProposal(db.Entity):
    notes = PonyOptional(str)  # Database optional

# In Pydantic schemas, use Optional for type hints:
class ExchangeProposalCreate(BaseModel):
    notes: Optional[str] = None  # Type hint optional
```

### Database Queries
Always use prefetch to avoid N+1 problems:
```python
# Good - Use prefetch
@db_session
def get_proposals_with_actors():
    return select(p for p in ExchangeProposal).prefetch(
        ExchangeProposal.proposer,
        ExchangeProposal.appointment_offered
    )

# Bad - N+1 query problem
@db_session
def get_proposals():
    proposals = select(p for p in ExchangeProposal)
    for p in proposals:
        print(p.proposer.name)  # Separate query for each!
```

## Frontend Stack

### HTMX + Alpine.js + Tailwind CSS
- **HTMX**: Partial page updates without full reload
- **Alpine.js**: Lightweight reactive components
- **Tailwind CSS**: Utility-first styling with custom dark theme

### Custom Color Palette (Teal-based Dark Theme)
```javascript
colors: {
    'dark-900': '#121212',  // Darkest background
    'dark-800': '#1a1a1a',
    'dark-700': '#2a2a2a',
    'dark-600': '#3a3a3a',
    'primary-900': '#004d4d',  // Teal dark
    'primary-800': '#006666',
    'primary-700': '#008080',
    'primary-600': '#009999',
    'primary-300': '#40d4d4',  // Teal light
}
```

### HTMX Pattern Example
```html
<button
    hx-post="/api/v1/exchange-proposals"
    hx-target="#proposal-list"
    hx-swap="afterbegin"
    hx-indicator="#spinner"
    class="btn-primary"
>
    Vorschlag erstellen
</button>
```

## Testing Strategy

### Test Pyramid
- **Unit Tests**: 80%+ coverage, focus on service layer (90%+)
- **Integration Tests**: API endpoints
- **E2E Tests**: Critical user flows

### Test Naming Convention
```python
def test_<function>_<scenario>_<expected_result>():
    """Test: <German description>"""
    pass

# Example
def test_create_exchange_proposal_invalid_appointment_raises_error():
    """Test: Fehlschlag bei ungültigem Einsatz wirft InvalidProposalError"""
    pass
```

## Development Philosophy: KEEP IT SIMPLE

**Motto**: "Better simple and working than complicated and buggy"

Before implementing complex solutions, always ask:
- "Is there a simpler way?"
- "Do we really need all these options?"
- "Is this the simplest solution that works?"

Prioritize:
- ✅ Simplicity over features
- ✅ Working code over perfect code
- ✅ Extending existing patterns over creating new ones
- ✅ Following standards (REST, HTTP status codes)
- ✅ Zero-configuration where possible

## Authentication & Roles

### Role-Based Access Control
- **ADMIN**: Full system access
- **DISPATCHER**: Team management, plan creation
- **CVO**: Approve exchange proposals for their locations
- **ACTOR**: View schedule, enter availability, propose exchanges

### JWT Authentication
- Access tokens: 15 minutes lifetime
- Refresh tokens: 7 days lifetime
- Cookie-based auth for web interface
- API key auth for desktop app integration

## User Workflows

### Actor Workflow
1. View appointments in calendar
2. Enter availability for upcoming PlanPeriods
3. Propose appointment exchanges
4. Receive notifications for approved/rejected exchanges

### CvO Workflow
1. View dashboard with pending proposals
2. Check availability matrix for their locations
3. Approve or reject exchange proposals
4. Monitor critical days (understaffing warnings)

### Dispatcher/Planner Workflow
1. Create PlanPeriods with deadlines
2. Upload plans from desktop app (hcc_plan_db_playground)
3. Coordinate with CvOs
4. Finalize and publish plans

## Integration with Desktop App

The desktop app (hcc_plan_db_playground) uses OR-Tools SAT solver for complex optimization. Integration via API:

```python
# Desktop app uploads optimized plan
POST /api/v1/integration/plan-versions
{
    "plan_data": {...},
    "status": "draft"
}

# Desktop app retrieves approved exchange proposals
GET /api/v1/integration/plan-versions/{version_id}/proposals

# Desktop app syncs changes back
PUT /api/v1/integration/plan-versions/{version_id}/sync
```

## Project Status & Roadmap

**Current Phase**: Phase 1 - Foundation & Setup (Weeks 1-2)
**Status**: Project structure initialized, dependencies defined

### MVP Scope (12 weeks)
- Modern design with Tailwind CSS
- Authentication & authorization
- Availability tracking
- Calendar view for appointments
- Email notifications
- Mobile-responsive

### Full Feature Set (additional 10 weeks)
- Exchange proposals with CvO approval
- Real-time WebSocket notifications
- CvO dashboard with availability matrix
- Desktop app integration
- Performance optimization
- Comprehensive testing

## Important Notes

### Before Making Structural Changes
Always ask for permission from the project owner (Thomas) before:
- Changing the layered architecture
- Adding new major dependencies
- Modifying database schema significantly
- Changing authentication approach

### Performance Considerations
- Use async endpoints for I/O-bound operations
- Implement pagination for list endpoints (max 1000 items)
- Cache frequently accessed data
- Use database indexes on foreign keys and commonly queried fields

### Security Best Practices
- Never log passwords or sensitive data
- Always use parameterized queries (PonyORM handles this)
- Validate all input with Pydantic
- Use HTTPS in production
- Configure CORS appropriately for environment

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Database Locked (SQLite)
Enable WAL mode in `database/db_setup.py`:
```python
db.bind('sqlite', 'data/hcc_plan.sqlite', create_db=True,
        pragmas={'journal_mode': 'WAL'})
```

### Import Errors
```bash
# Set PYTHONPATH
export PYTHONPATH=$(pwd)  # Linux/Mac
set PYTHONPATH=%CD%  # Windows
```
