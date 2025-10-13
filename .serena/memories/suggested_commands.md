# Suggested Commands - hcc_plan_web_unified

## Development Commands

### Environment Setup
```bash
# Virtual Environment erstellen (mit uv)
uv venv

# Virtual Environment aktivieren
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Dependencies installieren
uv sync

# Development Dependencies installieren
uv sync --extra dev
```

### Running the Application

```bash
# Development Server starten (mit Auto-Reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Oder mit uv:
uv run uvicorn main:app --reload

# Production-like (ohne Reload)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Testing

```bash
# Alle Tests ausführen
pytest

# Tests mit Coverage
pytest --cov=api --cov=database --cov-report=html

# Spezifische Test-Datei
pytest tests/unit/services/test_exchange_proposal_service.py

# Tests mit Output
pytest -v

# Tests mit Breakpoint-Debugging
pytest --pdb

# Nur failed Tests erneut ausführen
pytest --lf
```

### Code Quality

```bash
# Code formatieren mit Black
black .

# Import Sorting mit isort
isort .

# Black + isort zusammen
black . && isort .

# Type Checking mit mypy
mypy api database

# Linting (optional, wenn pylint installiert)
pylint api database
```

### Database

```bash
# Database Migrations (mit Alembic)
# Neue Migration erstellen
alembic revision --autogenerate -m "Add exchange_proposal table"

# Migrations anwenden
alembic upgrade head

# Migration rückgängig machen
alembic downgrade -1

# Migration History anzeigen
alembic history

# Aktuelle Version anzeigen
alembic current

# Database seeden mit Test-Daten
python scripts/seed_database.py

# Admin User erstellen
python scripts/create_admin.py
```

### Git Workflow

```bash
# Feature Branch erstellen
git checkout -b feature/exchange-proposals

# Status prüfen
git status

# Changes stagen
git add .

# Commit mit aussagekräftiger Message
git commit -m "feat(collaboration): Add exchange proposal creation"

# Push to remote
git push origin feature/exchange-proposals

# Branch wechseln
git checkout main

# Merge Feature Branch (nach Review)
git merge feature/exchange-proposals

# Branch löschen
git branch -d feature/exchange-proposals
```

### Docker (Optional)

```bash
# Docker Image bauen
docker build -t hcc-plan-web-unified .

# Container starten
docker run -p 8000:8000 hcc-plan-web-unified

# Docker Compose (wenn vorhanden)
docker-compose up

# Docker Compose im Background
docker-compose up -d

# Logs anzeigen
docker-compose logs -f

# Container stoppen
docker-compose down
```

### Utilities

```bash
# Requirements exportieren (falls requirements.txt benötigt)
uv pip compile pyproject.toml -o requirements.txt

# Dependency Tree anzeigen
uv pip tree

# Outdated Dependencies finden
uv pip list --outdated

# Spezifische Dependency updaten
uv pip install --upgrade fastapi

# Python REPL mit Projekt-Context
python -i scripts/repl_setup.py
```

### Debugging

```bash
# App mit Python Debugger starten
python -m pdb main.py

# Mit ipdb (besserer Debugger, muss installiert sein)
pip install ipdb
python -m ipdb main.py

# Logs in Echtzeit anzeigen (wenn in Datei geloggt wird)
tail -f logs/app.log
```

### Performance Testing

```bash
# Load Testing mit Locust (wenn installiert)
locust -f tests/performance/locustfile.py

# Memory Profiling (wenn memory_profiler installiert)
python -m memory_profiler main.py

# Line Profiling (wenn line_profiler installiert)
kernprof -l -v main.py
```

### Project Management

```bash
# Liste aller TODOs im Code finden
# Windows (PowerShell):
Select-String -Pattern "TODO|FIXME|HACK" -Path . -Recurse

# Linux/Mac:
grep -r "TODO\|FIXME\|HACK" .

# Lines of Code zählen
# Windows (PowerShell):
(Get-ChildItem -Include *.py -Recurse | Get-Content).Count

# Linux/Mac:
find . -name "*.py" | xargs wc -l
```

### Windows-Specific Commands

```powershell
# Prozesse auf Port 8000 finden und beenden
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Virtual Environment aktivieren (PowerShell)
.\.venv\Scripts\Activate.ps1

# Environment Variables setzen (aktuelle Session)
$env:DATABASE_URL="sqlite:///data/test.db"

# Verzeichnis-Struktur anzeigen
tree /F

# Dateien suchen
Get-ChildItem -Recurse -Filter "*.py"
```

### API Testing

```bash
# Mit curl (Windows: curl.exe oder Git Bash verwenden)
# Health Check
curl http://localhost:8000/health

# Login (JSON)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Mit httpie (schönere Ausgabe, muss installiert sein)
pip install httpie
http GET http://localhost:8000/health
http POST http://localhost:8000/api/v1/auth/login email=user@example.com password=password

# OpenAPI/Swagger Docs öffnen
# Browser öffnen mit: http://localhost:8000/docs
```

### Backup & Restore

```bash
# Database Backup (SQLite)
# Windows:
copy data\hcc_plan.sqlite data\backups\hcc_plan_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.sqlite

# Linux/Mac:
cp data/hcc_plan.sqlite data/backups/hcc_plan_backup_$(date +%Y%m%d).sqlite

# Database Restore
# Windows:
copy data\backups\hcc_plan_backup_20250101.sqlite data\hcc_plan.sqlite

# Linux/Mac:
cp data/backups/hcc_plan_backup_20250101.sqlite data/hcc_plan.sqlite
```

### CI/CD (wenn Setup vorhanden)

```bash
# GitHub Actions lokal testen (mit act)
act

# Pre-commit Hooks installieren (wenn verwendet)
pre-commit install

# Pre-commit Hooks manuell ausführen
pre-commit run --all-files
```

### Tailwind CSS (falls lokale Builds nötig)

```bash
# Tailwind CLI installieren (optional)
npm install -g tailwindcss

# Tailwind Build (watch mode)
tailwindcss -i static/css/input.css -o static/css/output.css --watch

# Tailwind Production Build (minified)
tailwindcss -i static/css/input.css -o static/css/output.css --minify
```

## Quick Reference

### Start Development (Schnellstart)
```bash
.venv\Scripts\activate          # 1. Virtual Env aktivieren
uvicorn main:app --reload       # 2. Server starten
# Browser: http://localhost:8000
```

### Before Commit (Pre-Commit Checklist)
```bash
black .                         # 1. Code formatieren
isort .                         # 2. Imports sortieren
mypy api database              # 3. Type Check
pytest                         # 4. Tests ausführen
git add .                       # 5. Changes stagen
git commit -m "..."            # 6. Commit
```

### After Pulling from Remote
```bash
git pull                        # 1. Änderungen holen
uv sync                        # 2. Dependencies updaten
alembic upgrade head           # 3. Database Migrations
pytest                         # 4. Tests ausführen
```

## Environment Variables

### Required (.env Datei)
```bash
# Database
DATABASE_URL=sqlite:///data/hcc_plan.sqlite
# oder PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/hcc_plan

# Security
SECRET_KEY=your-secret-key-min-32-characters-long

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Application
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# WebSocket (optional)
WS_URL=ws://localhost:8000/ws
```

## Troubleshooting

### Port bereits in Benutzung
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :8000
kill -9 <PID>
```

### Database Locked (SQLite)
```bash
# Alle Connections schließen und neu starten
# Oder WAL-Mode aktivieren in db_setup.py:
db.bind(..., pragmas={'journal_mode': 'WAL'})
```

### Import Errors
```bash
# PYTHONPATH setzen
# Windows:
set PYTHONPATH=%CD%
# Linux/Mac:
export PYTHONPATH=$(pwd)

# Oder in main.py:
import sys
sys.path.insert(0, '.')
```

### Module nicht gefunden
```bash
# Dependencies neu installieren
uv sync --reinstall

# Virtual Environment neu erstellen
rmdir /s .venv        # Windows
rm -rf .venv          # Linux/Mac
uv venv
uv sync
```
