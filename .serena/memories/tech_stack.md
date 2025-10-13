# Tech Stack - hcc_plan_web_unified

## Backend-Framework
- **FastAPI** >= 0.104.1 - Modernes Python Web-Framework
  - Automatische OpenAPI/Swagger Dokumentation
  - Type Hints und Pydantic Integration
  - Async/Await Support
  - Dependency Injection
- **Uvicorn** >= 0.24.0 - ASGI Server für FastAPI
- **Python** >= 3.12 - Moderne Python-Version mit neuesten Features

## Frontend-Technologien
- **Tailwind CSS** - Utility-First CSS Framework
  - Responsive Design
  - Dark Theme Support
  - Custom Color Palette (Teal-basiert)
- **HTMX** - HTML-über-HTTP Interaktivität
  - Partielle Page Updates ohne Full Reload
  - Progressive Enhancement
  - Server-Side Rendering
- **Alpine.js** - Leichtgewichtiges JavaScript Framework
  - Deklarative Event-Handling
  - Reactive Components
  - Minimal JavaScript Bundle
- **Jinja2** >= 3.1.2 - Template-Engine für HTML
  - Server-Side Rendering
  - Template Inheritance
  - Macros und Filters

## Datenbank & ORM
- **PonyORM** >= 0.7.16 - Pythonisches ORM
  - Generator-basierte Queries
  - Automatic Query Optimization
  - Database-agnostic (SQLite/PostgreSQL)
- **SQLite** - Entwicklungsdatenbank
  - File-based für einfaches Setup
  - WAL-Mode für Multi-User Support
- **PostgreSQL** - Produktionsdatenbank
  - Robustheit und Skalierbarkeit
  - Advanced Features (JSON, Arrays)
  - ACID Compliance

## Authentication & Security
- **Python-JOSE** - JWT Token-Handling
  - Access Token Generation
  - Token Validation
- **Passlib[bcrypt]** >= 1.7.4 - Password Hashing
  - Bcrypt für sichere Passwort-Speicherung
- **Python-Multipart** >= 0.0.6 - Multipart Form-Handling
- **Email-Validator** >= 2.1.0 - E-Mail-Validierung

## Data Validation & Serialization
- **Pydantic** >= 2.4.2 - Data Validation
  - Type-Safe API Contracts
  - Automatic Documentation
  - JSON Schema Generation
  - Custom Validators

## Scheduling & Automation
- **APScheduler** >= 3.10.0 - Background Task Scheduling
  - Cron-style Scheduling
  - Job Persistence in Database
  - Timezone Support (Europe/Berlin)
  - Recurring Reminders

## Email Integration
- **SMTP** - E-Mail-Versand
  - Verfügbarkeitsbestätigungen
  - Planänderungs-Benachrichtigungen
  - Erinnerungen für Deadlines
  - Tauschvorschlag-Notifications

## Real-Time Communication
- **WebSockets** (FastAPI native) - Real-Time Updates
  - Push-Benachrichtigungen
  - Live-Synchronisation
  - Connection Management
  - Event Broadcasting

## Development Tools
- **pytest** >= 7.4.0 - Testing Framework
  - Unit Tests
  - Integration Tests
  - Fixtures und Mocking
- **pytest-cov** >= 4.1.0 - Test Coverage
  - Coverage Reports
  - Branch Coverage
- **black** >= 23.7.0 - Code Formatter
  - Zeilen-Länge: 100
  - Konsistenter Code-Style
- **isort** >= 5.12.0 - Import Sorter
  - Black-kompatibel
  - Gruppierte Imports
- **mypy** >= 1.5.1 - Type Checker
  - Static Type Checking
  - Type Hints Validation

## Package Management
- **uv** - Moderner Python Package Manager
  - Schneller als pip
  - Lock-File Support (uv.lock)
  - Virtual Environment Management
- **pyproject.toml** - Projektdefinition
  - PEP 518 Standard
  - Tool Configuration
  - Dependencies Management

## Deployment & Infrastructure
- **Docker** - Containerization (optional)
  - Multi-Stage Builds
  - Development & Production Images
- **Nginx** - Reverse Proxy (optional)
  - Static File Serving
  - Load Balancing
- **Systemd** - Service Management (Linux)
  - Auto-Start
  - Process Monitoring

## Integration mit Desktop-App
- **REST API Client** - Python requests
  - Plan-Upload von Desktop-App
  - Synchronisation von Tauschvorschlägen
  - Bidirektionale Kommunikation

## Monitoring & Logging
- **Python Logging** - Standard Library
  - Structured Logging
  - Log Levels (DEBUG, INFO, WARNING, ERROR)
  - File und Console Handlers
- **Health Checks** - FastAPI Endpoints
  - Database Connectivity
  - Scheduler Status
  - WebSocket Server Status

## Architektur-Pattern
- **Layered Architecture**
  - Presentation Layer (Routes)
  - Business Logic Layer (Services)
  - Data Access Layer (Models/ORM)
  - Cross-Cutting Concerns (Middleware, Exceptions)
- **Service Layer Pattern** - Business Logic in Services
- **Repository Pattern** - Datenzugriff über PonyORM
- **Dependency Injection** - FastAPI Dependencies
- **Exception-Driven Development** - Domain-specific Exceptions

## Design Patterns
- **MVC Pattern** - Model-View-Controller Separation
- **DTO Pattern** - Pydantic Schemas als Data Transfer Objects
- **Factory Pattern** - Objekterstellung (Services, Repositories)
- **Observer Pattern** - WebSocket Event Broadcasting
- **Strategy Pattern** - Verschiedene Authentication-Strategien

## Performance Optimizations
- **Async/Await** - Non-blocking I/O
- **Connection Pooling** - Database Connection Reuse
- **Caching** - Template Caching, Query Result Caching
- **Lazy Loading** - On-demand Data Loading
- **Pagination** - Große Datensätze in Chunks
- **Database Indexing** - Optimierte Queries

## Browser-Kompatibilität
- **Modern Browsers** - Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile Browsers** - iOS Safari, Chrome Mobile, Samsung Internet
- **Progressive Enhancement** - Funktioniert auch ohne JavaScript (HTMX)
