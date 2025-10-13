# Session Handover - hcc_plan_web_unified
## Datum: 13. Oktober 2025

---

## 🎯 AKTUELLER STATUS

### Projekt erfolgreich aufgesetzt ✅
- **Repository**: `hcc_plan_web_unified` erstellt und aktiviert
- **Pfad**: `C:\Users\tombe\PycharmProjects\hcc_plan_web_unified`
- **Sprache**: Python 3.12+
- **Status**: Onboarding vollständig abgeschlossen

### Vorhandene Dateien
- ✅ `main.py` - Basis FastAPI App (Placeholder)
- ✅ `pyproject.toml` - Minimale Konfiguration
- ✅ `.venv/` - Virtual Environment vorhanden
- ✅ `.serena/` - Serena Konfiguration mit allen Memories

### Erstellte Dokumentation (in Serena Memories)
1. **project_overview** - Vollständige Projektbeschreibung
2. **tech_stack** - Technologie-Stack Dokumentation
3. **code_style_conventions** - Coding-Standards
4. **development_guidelines** - Best Practices
5. **project_structure** - Geplante Verzeichnisstruktur
6. **implementation_plan_detailed** - 22-Wochen Implementierungsplan
7. **suggested_commands** - Alle wichtigen Kommandos
8. **task_completion_checklist** - Task-Completion Checkliste

---

## 📝 PROJEKTZUSAMMENFASSUNG

### Projektziel
Entwicklung einer **modernen, kollaborativen Einsatzplanungs-Webapplikation** für Theater-Teams (Klinikclowns), die:
- Modernes Design kombiniert (von `appointment_plan_api_cl`)
- Features integriert (von `hcc_plan_api`)
- Neue Kollaborations-Features hinzufügt (Tauschvorschläge, CvO-Dashboard)
- Mit Desktop-App integriert (von `hcc_plan_db_playground`)

### Hauptfunktionen
**Für Actors (Mitarbeiter):**
- Einsatzplan-Kalenderansicht
- Verfügbarkeitserfassung
- Tauschbörse für Einsätze
- Mobile-First Design

**Für CvOs (Chief-Verantwortliche):**
- Dashboard mit Tauschvorschlägen
- Verfügbarkeitsmatrix
- Genehmigung/Ablehnung von Tauschen
- Engpass-Erkennung

**Für Dispatcher/Planer:**
- Plan-Upload von Desktop-App
- Planversions-Management
- Integration mit OR-Tools Solver

### Tech Stack
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Tailwind CSS + HTMX + Alpine.js
- **Database**: PonyORM mit SQLite (Dev) / PostgreSQL (Prod)
- **Auth**: JWT + Cookie-based
- **Real-Time**: WebSockets
- **Scheduling**: APScheduler
- **E-Mail**: SMTP Integration

---

## 🗺️ IMPLEMENTIERUNGSPLAN

### Zeitrahmen: 22 Wochen (5.5 Monate)
- **MVP**: 12 Wochen (Phase 1-5)
- **Full Feature Set**: +10 Wochen (Phase 6-10)

### Phasen-Übersicht
1. **Phase 1 (Woche 1-2)**: Foundation & Setup
2. **Phase 2 (Woche 3-6)**: Database & Core Entities
3. **Phase 3 (Woche 7-8)**: Authentication & Authorization
4. **Phase 4 (Woche 9-10)**: Verfügbarkeitserfassung
5. **Phase 5 (Woche 11-12)**: Einsatzplan-Kalender → **MVP ERREICHT**
6. **Phase 6 (Woche 13-14)**: Tauschvorschläge
7. **Phase 7 (Woche 15-16)**: CvO Dashboard
8. **Phase 8 (Woche 17-18)**: WebSocket Real-Time
9. **Phase 9 (Woche 19-20)**: Desktop-Integration
10. **Phase 10 (Woche 21-22)**: Polish & Optimization → **FULL FEATURE**

---

## 🚀 NÄCHSTE SCHRITTE (Phase 1 - Woche 1)

### Sofort zu erledigende Aufgaben:

#### 1. Git Setup
```bash
# .gitignore erstellen mit:
- Python: __pycache__/, .venv/, *.pyc, *.pyo
- IDE: .idea/, .vscode/
- Environment: .env, *.sqlite, *.db
- Build: dist/, build/, *.egg-info/
```

#### 2. Dependencies konfigurieren
```bash
# pyproject.toml erweitern mit:
- FastAPI >= 0.104.1
- Uvicorn >= 0.24.0
- Pydantic >= 2.4.2
- PonyORM >= 0.7.16
- python-jose, passlib[bcrypt]
- jinja2, APScheduler
- pytest, black, isort, mypy (dev dependencies)

# Dann installieren:
uv sync
```

#### 3. Environment Variables
```bash
# .env.example erstellen mit Template:
DATABASE_URL=sqlite:///data/hcc_plan.sqlite
SECRET_KEY=your-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
DEBUG=True

# .env erstellen (nicht in Git!)
```

#### 4. Verzeichnisstruktur erstellen
```bash
# Siehe project_structure.md Memory für vollständige Struktur
# Wichtigste Ordner zuerst:
api/
├── auth/
├── exceptions/
├── middleware/
├── models/
├── routes/
│   ├── api/
│   └── web/
├── services/
└── utils/

database/
└── models/

templates/
static/
├── css/
├── js/
└── images/

tests/
scripts/
```

#### 5. main.py erweitern
```python
# Lifespan Event Handler
# Static Files Mounting
# Exception Handlers
# Basic Routes (Health Check, Landing Page)
```

#### 6. Design-System Setup
```bash
# Tailwind CSS Configuration
# base.html Template mit Dark Theme
# Custom Color Palette (Teal-basiert)
# HTMX + Alpine.js Integration
```

---

## 🔑 WICHTIGE PRINZIPIEN

### KEEP IT SIMPLE
- Einfachheit vor Features
- Bewährte Patterns nutzen
- Keine Over-Engineering
- Standards befolgen

### Entwicklungsrichtlinien
- **Deutsche Kommentare** - Alle Kommentare auf Deutsch
- **Type Hints** - Durchgehend verwenden
- **Service Layer Pattern** - Business Logic in Services
- **Command Pattern** - Für Desktop-Integration später
- **Pydantic Schemas** - Für alle API Contracts
- **Exception-Driven** - Domain-specific Exceptions

### Code Style
- **snake_case** für Funktionen/Variablen
- **PascalCase** für Klassen
- **Black** für Formatierung (line-length: 100)
- **isort** für Import-Sortierung
- **mypy** für Type Checking

---

## 🎨 DESIGN-SYSTEM

### Color Palette (Dark Theme)
```
Backgrounds:
- dark-900: #121212 (Main BG)
- dark-800: #1a1a1a
- dark-700: #2a2a2a
- dark-600: #3a3a3a

Primary (Teal):
- primary-900: #004d4d
- primary-800: #006666
- primary-700: #008080
- primary-600: #009999
- primary-300: #40d4d4 (Accents)
```

### Frontend Stack
- **Tailwind CSS** - Utility-First CSS
- **HTMX** - HTML-über-HTTP Interaktivität
- **Alpine.js** - Leichtgewichtiges JavaScript
- **Jinja2** - Server-Side Templates

---

## 📚 REFERENZ-PROJEKTE

### Drei Vorgänger-Projekte als Basis:

1. **appointment_plan_api_cl** (Design-Vorlage)
   - Modernes Dark Theme
   - Excellente Kalenderansicht
   - HTMX + Alpine.js + Tailwind
   - **Zu portieren**: Templates, Design-System, Kalender-UI

2. **hcc_plan_api** (Feature-Basis)
   - Verfügbarkeitserfassung
   - APScheduler Integration
   - E-Mail-System
   - Team-Management
   - **Zu portieren**: Availables/AvailDay Entities, E-Mail-Templates, Scheduler Jobs

3. **hcc_plan_db_playground** (Desktop-App)
   - OR-Tools SAT-Solver
   - Command Pattern
   - Komplexe Planungsfunktionen
   - **Integration**: API Client für Plan-Upload später (Phase 9)

---

## ⚠️ KRITISCHE ENTSCHEIDUNGEN DOKUMENTIERT

### Architektur-Entscheidungen (mit Thomas abgestimmt)
1. **Option 2 gewählt**: Hybrid-Architektur
   - Desktop-App bleibt für Power-User
   - Neue Web-App für alle User + Mobile
   - Gemeinsames API-Backend

2. **Design von appointment_plan_api_cl favorisiert**
   - Modernes Dark Theme
   - Mobile-First
   - HTMX für Progressive Enhancement

3. **Keine strukturellen Änderungen ohne Rücksprache**
   - Alle Architektur-Entscheidungen mit Thomas abstimmen
   - Erst fragen, dann implementieren

---

## 🎯 MVP ERFOLGS-KRITERIEN (Woche 12)

### Must-Have Features:
- ✅ Modernes Design (Dark Theme, Tailwind)
- ✅ Authentication & Authorization
- ✅ Verfügbarkeitserfassung für Actors
- ✅ Einsatzplan-Kalenderansicht für Actors
- ✅ E-Mail-Benachrichtigungen
- ✅ Mobile-responsive

### MVP nicht enthalten (kommt später):
- ❌ Tauschvorschläge (Phase 6)
- ❌ CvO Dashboard (Phase 7)
- ❌ WebSocket Real-Time (Phase 8)
- ❌ Desktop-Integration (Phase 9)

---

## 💡 EMPFEHLUNGEN FÜR NÄCHSTE SESSION

### Priorität 1 (Sofort):
1. Git Setup (.gitignore, README.md)
2. pyproject.toml mit Dependencies konfigurieren
3. .env.example und .env erstellen
4. Virtual Environment aktivieren und Dependencies installieren

### Priorität 2 (Danach):
5. Verzeichnisstruktur erstellen
6. main.py erweitern mit FastAPI Setup
7. Database Setup (db_setup.py)
8. Base Template mit Design-System

### Priorität 3 (Optional für Woche 1):
9. Health Check Endpoint testen
10. Erste Tests schreiben
11. Development Server starten und testen

---

## 🔧 QUICK START KOMMANDOS

```bash
# Virtual Environment aktivieren
.venv\Scripts\activate

# Dependencies installieren
uv sync

# Development Server starten
uvicorn main:app --reload

# Tests ausführen
pytest

# Code formatieren
black . && isort .

# Type Checking
mypy api database
```

---

## 📞 KOMMUNIKATION

### Mit Thomas (Projekt-Owner)
- **Vor strukturellen Änderungen**: Immer abstimmen
- **Nach Implementierung**: Status-Update
- **Bei Problemen**: Sofort kommunizieren

### Wichtig zu wissen:
- Thomas bevorzugt **KEEP IT SIMPLE** Ansatz
- Deutsche Kommentare im Code
- Keine eigenständigen Architektur-Änderungen
- Rücksprache bei grundlegenden Entscheidungen

---

## 📋 OFFENE FRAGEN FÜR THOMAS

**Keine offenen Fragen aktuell** - Onboarding abgeschlossen, bereit für Implementierung.

---

## ✅ SESSION ABSCHLUSS

### Was wurde erreicht:
- ✅ Projekt `hcc_plan_web_unified` aufgesetzt
- ✅ Onboarding vollständig durchgeführt
- ✅ Alle Dokumentation in Memories gespeichert
- ✅ Implementierungsplan erstellt (22 Wochen)
- ✅ Nächste Schritte definiert (Phase 1)
- ✅ Bereit für Implementierung

### Nächste Session sollte beginnen mit:
1. Serena aktivieren: `activate_project hcc_plan_web_unified`
2. Memories laden (automatisch verfügbar)
3. Direkt mit Phase 1 Setup starten
4. `.gitignore` und `pyproject.toml` erstellen

---

**STATUS: READY FOR IMPLEMENTATION** 🚀

Alle Vorbereitungen abgeschlossen. Die nächste Session kann direkt mit der praktischen Implementierung beginnen!
