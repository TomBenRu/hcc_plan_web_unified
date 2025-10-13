# Projektstruktur - hcc_plan_web_unified

## Geplante Verzeichnisstruktur

```
hcc_plan_web_unified/
├── main.py                     # FastAPI App Entry Point
├── pyproject.toml              # Project Configuration (uv)
├── uv.lock                     # Dependency Lock File
├── .env                        # Environment Variables (nicht in Git)
├── .env.example                # Environment Variables Template
├── .gitignore                  # Git Ignore Rules
├── README.md                   # Project Documentation
├── alembic.ini                 # Alembic Configuration (DB Migrations)
├── alembic/                    # Database Migrations
│   ├── versions/               # Migration Scripts
│   └── env.py                  # Alembic Environment
│
├── api/                        # API Layer
│   ├── __init__.py
│   ├── templates.py            # Template Configuration
│   │
│   ├── auth/                   # Authentication System
│   │   ├── __init__.py
│   │   ├── jwt.py              # JWT Token Handling
│   │   ├── cookie_auth.py      # Cookie-based Authentication
│   │   ├── dependencies.py     # Auth Dependencies (get_current_user)
│   │   └── roles.py            # Role-based Access Control
│   │
│   ├── exceptions/             # Domain-specific Exceptions
│   │   ├── __init__.py
│   │   ├── base.py             # Base Exception Classes
│   │   ├── auth.py             # Authentication Exceptions
│   │   ├── appointment.py      # Appointment Exceptions
│   │   ├── availability.py     # Availability Exceptions
│   │   ├── collaboration.py    # Collaboration Exceptions (NEU)
│   │   ├── location.py         # Location Exceptions
│   │   ├── person.py           # Person Exceptions
│   │   └── plan.py             # Plan Exceptions
│   │
│   ├── middleware/             # Cross-cutting Concerns
│   │   ├── __init__.py
│   │   ├── cors.py             # CORS Middleware
│   │   ├── error_handler.py    # Global Error Handling
│   │   ├── logging.py          # Request Logging
│   │   └── rate_limit.py       # Rate Limiting (optional)
│   │
│   ├── models/                 # Pydantic Schemas (API Contracts)
│   │   ├── __init__.py
│   │   ├── base.py             # Base Schemas
│   │   ├── auth.py             # Auth Schemas (Login, Register)
│   │   ├── person.py           # Person Schemas
│   │   ├── team.py             # Team Schemas
│   │   ├── plan_period.py      # PlanPeriod Schemas
│   │   ├── availability.py     # Availability Schemas
│   │   ├── appointment.py      # Appointment Schemas
│   │   ├── plan.py             # Plan Schemas
│   │   ├── location.py         # Location Schemas
│   │   └── collaboration.py    # Collaboration Schemas (NEU)
│   │       ├── plan_version.py
│   │       ├── exchange_proposal.py
│   │       ├── comment.py
│   │       └── notification.py
│   │
│   ├── routes/                 # Route Definitions
│   │   ├── __init__.py
│   │   │
│   │   ├── api/                # JSON API Endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Authentication API
│   │   │   ├── appointments.py # Appointment CRUD API
│   │   │   ├── availability.py # Availability API
│   │   │   ├── locations.py    # Location API
│   │   │   ├── persons.py      # Person API
│   │   │   ├── plans.py        # Plan API
│   │   │   ├── teams.py        # Team API
│   │   │   └── collaboration.py # Collaboration API (NEU)
│   │   │       ├── plan_versions.py
│   │   │       ├── exchange_proposals.py
│   │   │       ├── comments.py
│   │   │       └── notifications.py
│   │   │
│   │   ├── web/                # HTML Rendering Routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Web Authentication Routes
│   │   │   ├── index.py        # Landing Page
│   │   │   │
│   │   │   ├── actor/          # Actor-specific Views
│   │   │   │   ├── __init__.py
│   │   │   │   ├── calendar.py # Einsatzplan-Kalender
│   │   │   │   ├── availability.py # Verfügbarkeitserfassung
│   │   │   │   └── exchanges.py # Tauschbörse
│   │   │   │
│   │   │   ├── cvo/            # CvO-specific Views
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dashboard.py # CvO Dashboard
│   │   │   │   ├── proposals.py # Tauschvorschläge verwalten
│   │   │   │   └── availability_matrix.py # Verfügbarkeitsmatrix
│   │   │   │
│   │   │   ├── dispatcher/     # Dispatcher Views
│   │   │   │   ├── __init__.py
│   │   │   │   ├── teams.py    # Team Management
│   │   │   │   └── planning.py # Planungswerkzeuge
│   │   │   │
│   │   │   └── admin/          # Admin Views
│   │   │       ├── __init__.py
│   │   │       ├── users.py    # User Management
│   │   │       ├── projects.py # Project Management
│   │   │       └── settings.py # System Settings
│   │   │
│   │   └── websockets/         # WebSocket Routes
│   │       ├── __init__.py
│   │       ├── connection_manager.py
│   │       └── notifications.py
│   │
│   ├── services/               # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication Logic
│   │   ├── appointment_service.py # Appointment Business Logic
│   │   ├── availability_service.py # Availability Management
│   │   ├── calendar_service.py # Calendar Logic
│   │   ├── location_service.py # Location Management
│   │   ├── person_service.py   # Person Management
│   │   ├── plan_service.py     # Plan Management
│   │   ├── team_service.py     # Team Management
│   │   └── collaboration/      # Collaboration Services (NEU)
│   │       ├── __init__.py
│   │       ├── plan_version_service.py
│   │       ├── exchange_proposal_service.py
│   │       ├── comment_service.py
│   │       ├── notification_service.py
│   │       └── cvo_service.py
│   │
│   └── utils/                  # Helper Functions
│       ├── __init__.py
│       ├── datetime_utils.py   # Date/Time Utilities
│       ├── converters.py       # Data Converters
│       ├── validators.py       # Custom Validators
│       └── email_utils.py      # Email Utilities
│
├── database/                   # Database Layer
│   ├── __init__.py
│   ├── db_setup.py             # Database Configuration
│   │
│   └── models/                 # PonyORM Entity Definitions
│       ├── __init__.py
│       ├── base.py             # Database Instance
│       ├── auth.py             # Authentication Entities (User)
│       ├── core.py             # Core Entities (Person, Team, Project)
│       ├── planning.py         # Planning Entities (PlanPeriod, Appointment, Plan)
│       ├── availability.py     # Availability Entities
│       ├── location.py         # Location Entities
│       └── collaboration.py    # Collaboration Entities (NEU)
│           ├── plan_version.py
│           ├── exchange_proposal.py
│           ├── comment.py
│           ├── notification.py
│           └── cvo_role.py
│
├── scheduler/                  # Background Tasks
│   ├── __init__.py
│   ├── scheduler_config.py     # APScheduler Configuration
│   ├── jobs.py                 # Job Definitions
│   └── tasks/                  # Task Implementations
│       ├── __init__.py
│       ├── availability_reminders.py
│       ├── plan_deadline_reminders.py
│       └── notification_cleanup.py
│
├── email_templates/            # Email Templates
│   ├── availability_confirmed.html
│   ├── availability_reminder.html
│   ├── plan_published.html
│   ├── exchange_proposal_created.html
│   ├── exchange_proposal_approved.html
│   └── exchange_proposal_rejected.html
│
├── static/                     # Static Web Assets
│   ├── css/
│   │   └── styles.css          # Custom CSS (zusätzlich zu Tailwind)
│   ├── js/
│   │   ├── tailwind-config.js  # Tailwind Configuration
│   │   ├── colorUtils.js       # Color Utilities (für Location Colors)
│   │   └── collaboration.js    # Collaboration Client (WebSocket)
│   └── images/
│       ├── logo.png
│       └── icons/
│
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Base Template
│   ├── index.html              # Landing Page
│   ├── login_modal.html        # Login Modal
│   ├── error.html              # Error Page
│   │
│   ├── components/             # Reusable Components
│   │   ├── navigation.html
│   │   ├── breadcrumbs.html
│   │   ├── pagination.html
│   │   └── loading_spinner.html
│   │
│   ├── actor/                  # Actor Templates
│   │   ├── calendar.html       # Kalenderansicht
│   │   ├── calendar_partial.html # HTMX Partial
│   │   ├── availability.html   # Verfügbarkeitserfassung
│   │   ├── exchange_proposal_modal.html
│   │   └── appointment_detail_modal.html
│   │
│   ├── cvo/                    # CvO Templates
│   │   ├── dashboard.html      # Dashboard
│   │   ├── proposals_list.html # Tauschvorschläge
│   │   ├── availability_matrix.html # Verfügbarkeitsmatrix
│   │   └── proposal_detail_modal.html
│   │
│   ├── dispatcher/             # Dispatcher Templates
│   │   ├── teams.html
│   │   ├── planning.html
│   │   └── plan_upload.html
│   │
│   └── admin/                  # Admin Templates
│       ├── users.html
│       ├── projects.html
│       └── settings.html
│
├── tests/                      # Test Suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest Configuration & Fixtures
│   │
│   ├── unit/                   # Unit Tests
│   │   ├── services/
│   │   │   ├── test_auth_service.py
│   │   │   ├── test_appointment_service.py
│   │   │   ├── test_availability_service.py
│   │   │   └── test_exchange_proposal_service.py
│   │   └── utils/
│   │       ├── test_datetime_utils.py
│   │       └── test_validators.py
│   │
│   ├── integration/            # Integration Tests
│   │   ├── api/
│   │   │   ├── test_auth_api.py
│   │   │   ├── test_appointments_api.py
│   │   │   ├── test_availability_api.py
│   │   │   └── test_collaboration_api.py
│   │   └── database/
│   │       └── test_database_integration.py
│   │
│   └── e2e/                    # End-to-End Tests
│       ├── test_actor_workflow.py
│       ├── test_cvo_workflow.py
│       └── test_collaboration_workflow.py
│
├── scripts/                    # Utility Scripts
│   ├── create_admin.py         # Create Admin User
│   ├── seed_database.py        # Seed Test Data
│   ├── migrate_from_old_db.py  # Migration from old systems
│   └── backup_database.py      # Database Backup
│
├── docs/                       # Documentation
│   ├── API.md                  # API Documentation
│   ├── ARCHITECTURE.md         # Architecture Overview
│   ├── DEPLOYMENT.md           # Deployment Guide
│   ├── CONTRIBUTING.md         # Contribution Guidelines
│   └── CHANGELOG.md            # Changelog
│
└── .venv/                      # Virtual Environment (nicht in Git)
```

## Wichtige Dateien und ihre Funktion

### main.py
Haupteinstiegspunkt der Anwendung:
- FastAPI App Initialisierung
- Middleware Setup
- Router Registrierung
- Lifespan Events (Startup/Shutdown)
- Database Initialization
- Scheduler Startup

### pyproject.toml
Project Configuration:
- Dependencies
- Development Dependencies
- Tool Configuration (black, isort, mypy, pytest)
- Entry Points

### .env / .env.example
Environment Variables:
- DATABASE_URL
- SECRET_KEY
- SMTP Configuration
- CORS Origins
- Debug Mode

## Architektur-Layers

### 1. Presentation Layer (Routes)
- **API Routes**: JSON Responses für programmatischen Zugriff
- **Web Routes**: HTML Responses für Browser
- **WebSocket Routes**: Real-Time Communication

### 2. Business Logic Layer (Services)
- Alle Business Logic
- Transaktionale Operationen
- Validierung und Fehlerbehandlung
- Integration verschiedener Entities

### 3. Data Access Layer (Database Models)
- PonyORM Entities
- Database Schema
- Relationships
- Constraints

### 4. Cross-Cutting Concerns
- **Middleware**: CORS, Error Handling, Logging
- **Exceptions**: Domain-specific Errors
- **Utils**: Helper Functions
- **Scheduler**: Background Jobs

## Naming Conventions

### Directories
- **Lowercase mit Unterstrichen**: `exchange_proposals/`
- **Plural für Kollektionen**: `services/`, `models/`, `routes/`
- **Hierarchisch organisiert**: `routes/web/actor/`

### Files
- **Lowercase mit Unterstrichen**: `exchange_proposal_service.py`
- **Descriptive Names**: Dateiname beschreibt Inhalt
- **Suffixes für Clarity**: `_service.py`, `_test.py`, `_modal.html`

### Modules
- **`__init__.py`** in jedem Package
- **Exports in `__init__.py`**: Wichtige Klassen/Funktionen exportieren
- **Relative Imports**: Innerhalb Package relative Imports nutzen

## Design Patterns Used

### Service Layer Pattern
Jede Entity hat einen Service mit Business Logic.

### Repository Pattern
PonyORM Entities fungieren als Repositories.

### Factory Pattern
Services erstellen komplexe Objekte.

### Observer Pattern
WebSocket für Event Broadcasting.

### Dependency Injection
FastAPI Dependencies für Auth, DB-Session, etc.

## Development Workflow

### 1. Feature Branch erstellen
```bash
git checkout -b feature/exchange-proposals
```

### 2. Schema definieren
```python
# api/models/collaboration.py
class ExchangeProposalCreate(BaseModel):
    ...
```

### 3. Entity erstellen
```python
# database/models/collaboration.py
class ExchangeProposal(db.Entity):
    ...
```

### 4. Service implementieren
```python
# api/services/collaboration/exchange_proposal_service.py
class ExchangeProposalService:
    @staticmethod
    def create_proposal(...) -> ExchangeProposal:
        ...
```

### 5. Tests schreiben
```python
# tests/unit/services/test_exchange_proposal_service.py
def test_create_exchange_proposal_success():
    ...
```

### 6. API Route erstellen
```python
# api/routes/api/collaboration/exchange_proposals.py
@router.post("/")
async def create_exchange_proposal(...):
    ...
```

### 7. Template erstellen
```html
<!-- templates/actor/exchange_proposal_modal.html -->
```

### 8. Integration testen
```python
# tests/integration/api/test_collaboration_api.py
def test_create_exchange_proposal_integration():
    ...
```
