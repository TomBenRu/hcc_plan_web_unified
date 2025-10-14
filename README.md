# 🎭 HCC Plan Web Unified

Kollaborative Einsatzplanungs-Webapplikation für Theater-Teams (Klinikclowns)

## 📋 Über das Projekt

HCC Plan Web Unified ist eine moderne Webapplikation zur Einsatzplanung für Theater-Teams. Sie kombiniert:
- Modernes Dark Theme Design
- Kollaborations-Features (Tauschvorschläge, CvO-Dashboard)
- Verfügbarkeitserfassung
- Mobile-First Design
- Integration mit Desktop-App

## 🚀 Quick Start

### Voraussetzungen

- Python 3.12+
- uv (Python Package Manager)

### Installation

```bash
# Repository klonen
git clone <repository-url>
cd hcc_plan_web_unified

# Dependencies installieren
uv sync

# Environment Variables konfigurieren
cp .env.example .env
# Bearbeite .env mit deinen Einstellungen

# Development Server starten
uv run uvicorn main:app --reload
```

Die Applikation läuft auf: `http://localhost:8000`

### Development Dependencies installieren

```bash
uv sync --extra dev
```

## 📁 Projektstruktur

```
hcc_plan_web_unified/
├── api/                      # Backend API Code
│   ├── auth/                 # Authentication & Authorization
│   ├── exceptions/           # Custom Exceptions
│   ├── middleware/           # FastAPI Middleware
│   ├── models/               # Pydantic Schemas
│   ├── routes/               # API & Web Routes
│   │   ├── api/              # REST API Endpoints
│   │   └── web/              # Web Page Routes
│   │       ├── cvo/          # CvO-spezifische Routes
│   │       └── employee/     # Employee-spezifische Routes
│   ├── services/             # Business Logic Layer
│   └── utils/                # Utility Functions & Config
├── database/                 # Database Layer
│   ├── models/               # PonyORM Entities
│   └── db_setup.py           # Database Configuration
├── static/                   # Static Files (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                # Jinja2 Templates
│   ├── components/           # Reusable Components
│   ├── employee/             # Employee Views
│   └── base.html             # Base Template
├── tests/                    # Tests
│   ├── unit/                 # Unit Tests
│   └── integration/          # Integration Tests
├── scripts/                  # Utility Scripts
├── data/                     # SQLite Database (Development)
├── logs/                     # Log Files
├── main.py                   # Application Entry Point
├── pyproject.toml            # Project Configuration
└── .env                      # Environment Variables (nicht in Git)
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python Web Framework
- **Uvicorn** - ASGI Server
- **PonyORM** - ORM für Datenbank
- **Pydantic** - Data Validation
- **APScheduler** - Task Scheduling

### Frontend
- **Tailwind CSS** - Utility-First CSS Framework
- **HTMX** - HTML-über-HTTP Interaktivität
- **Alpine.js** - Leichtgewichtiges JavaScript Framework
- **Jinja2** - Server-Side Templates

### Database
- **SQLite** (Development)
- **PostgreSQL** (Production)

### Authentication
- **JWT** - JSON Web Tokens
- **bcrypt** - Password Hashing

## 📝 Entwicklung

### Code Formatierung

```bash
# Code formatieren mit Black
uv run black .

# Imports sortieren mit isort
uv run isort .

# Beide gleichzeitig
uv run black . && uv run isort .
```

### Type Checking

```bash
uv run mypy api database
```

### Tests ausführen

```bash
# Alle Tests
uv run pytest

# Mit Coverage
uv run pytest --cov=api --cov=database

# Spezifische Tests
uv run pytest tests/unit/
```

### Linting

```bash
uv run ruff check .
```

## 🔧 Konfiguration

Alle Einstellungen werden über Environment Variables in `.env` konfiguriert:

```bash
# Application
APP_NAME=HCC Plan Web Unified
DEBUG=True
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///data/hcc_plan.sqlite

# Security
SECRET_KEY=your-secret-key-here

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password

# Siehe .env.example für alle Optionen
```

## 📊 Development Status

### Phase 1: Foundation & Setup ✅
- [x] Projektstruktur erstellt
- [x] Dependencies konfiguriert
- [x] Environment Setup
- [x] FastAPI Basis-Setup
- [x] Database Setup
- [x] Base Template mit Dark Theme

### Phase 2: Database & Core Entities (In Arbeit)
- [ ] Person Entity
- [ ] Team Entity
- [ ] PlanVersion Entity
- [ ] Appointment Entity

### Nächste Phasen
- Phase 3: Authentication & Authorization
- Phase 4: Verfügbarkeitserfassung
- Phase 5: Einsatzplan-Kalender → **MVP**
- Phase 6-10: Advanced Features

## 🎨 Design-System

### Color Palette (Dark Theme)

```css
/* Backgrounds */
dark-900: #121212  /* Main Background */
dark-800: #1a1a1a
dark-700: #2a2a2a
dark-600: #3a3a3a

/* Primary (Teal) */
primary-900: #004d4d
primary-800: #006666
primary-700: #008080
primary-600: #009999
primary-300: #40d4d4  /* Accents */

/* Status Colors */
success: #10b981
warning: #f59e0b
error: #ef4444
info: #3b82f6
```

## 📚 API Dokumentation

Nach dem Start der Applikation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Feature Branch erstellen: `git checkout -b feature/my-feature`
2. Änderungen committen: `git commit -am 'feat: Add new feature'`
3. Branch pushen: `git push origin feature/my-feature`
4. Pull Request erstellen

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** feat, fix, docs, style, refactor, test, chore

## 📄 Lizenz

[Lizenz hier einfügen]

## 👥 Team

- Thomas - Project Owner

## 📞 Support

Bei Fragen oder Problemen: [Kontakt hier einfügen]
