# Task Completion Checklist

## Nach jeder Feature-Implementierung

### 1. Code Quality Checks ✅

```bash
# Automatisch formatieren
black .
isort .

# Type Checking
mypy api database

# Linting (optional)
pylint api database
```

**Erwartung:**
- ✅ Keine Fehler bei black/isort
- ✅ Keine Fehler bei mypy (oder nur erlaubte Ignores)
- ✅ Keine kritischen pylint Warnungen

### 2. Tests schreiben und ausführen ✅

```bash
# Tests ausführen
pytest

# Mit Coverage
pytest --cov=api --cov=database --cov-report=html
```

**Erwartung:**
- ✅ Alle Tests grün
- ✅ Neue Feature hat Unit Tests (Service Layer)
- ✅ Neue API Endpoints haben Integration Tests
- ✅ Coverage bleibt > 80% (idealerweise steigt)

**Test-Checklist:**
- [ ] Unit Tests für Service Logic geschrieben
- [ ] Integration Tests für API Endpoints geschrieben
- [ ] Edge Cases getestet (z.B. ungültige Inputs)
- [ ] Error Handling getestet
- [ ] Alle Tests laufen durch

### 3. Dokumentation aktualisieren 📝

**Code-Dokumentation:**
- [ ] Docstrings für neue Funktionen/Klassen hinzugefügt
- [ ] Type Hints vollständig
- [ ] Komplexe Logik mit Kommentaren erklärt (auf Deutsch)

**API-Dokumentation:**
- [ ] OpenAPI/Swagger Docs automatisch aktualisiert (FastAPI macht das)
- [ ] Beispiel-Requests/Responses in Docstrings (optional)

**Projekt-Dokumentation:**
- [ ] README.md aktualisiert (falls nötig)
- [ ] CHANGELOG.md Eintrag hinzugefügt
- [ ] Wenn größeres Feature: docs/ARCHITECTURE.md aktualisiert

### 4. Database Migrations (falls DB-Änderungen) 💾

```bash
# Migration erstellen
alembic revision --autogenerate -m "Add exchange_proposal table"

# Migration testen
alembic upgrade head

# Rollback testen
alembic downgrade -1
alembic upgrade head

# Migration committen
git add alembic/versions/*.py
```

**Erwartung:**
- ✅ Migration läuft ohne Fehler
- ✅ Rollback funktioniert
- ✅ Migration ist beschreibend benannt

### 5. Git Commit 📦

```bash
# Status prüfen
git status

# Änderungen stagen
git add .

# Commit mit aussagekräftiger Message
git commit -m "feat(collaboration): Add exchange proposal creation

- ExchangeProposal entity created
- API endpoints /api/v1/collaboration/exchange-proposals implemented
- CvO can approve/reject proposals
- Email notifications on proposal creation

Closes #42"
```

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: Neues Feature
- `fix`: Bug Fix
- `docs`: Dokumentation
- `style`: Formatierung, Semicolons, etc.
- `refactor`: Code-Refactoring (keine Features/Fixes)
- `test`: Tests hinzufügen/ändern
- `chore`: Build, Dependencies, etc.

**Erwartung:**
- ✅ Commit Message beschreibend
- ✅ Keine Debug-Code/Console.logs committed
- ✅ Keine .env Dateien committed
- ✅ Keine temporären Dateien committed

### 6. Push und Pull Request 🚀

```bash
# Zu Feature Branch pushen
git push origin feature/exchange-proposals

# Pull Request erstellen auf GitHub/GitLab
# - Beschreibung was gemacht wurde
# - Screenshots bei UI-Änderungen
# - Link zu Issues (Closes #...)
# - Reviewer zuweisen
```

**Pull Request Checklist:**
- [ ] Beschreibung vollständig
- [ ] Tests laufen durch
- [ ] Keine Merge Conflicts
- [ ] Screenshots bei UI-Änderungen
- [ ] Reviewer zugewiesen

### 7. Code Review durchführen/erhalten 👀

**Als Reviewer:**
- [ ] Code Logik nachvollziehbar?
- [ ] Tests ausreichend?
- [ ] Security Considerations beachtet?
- [ ] Performance OK?
- [ ] Dokumentation vorhanden?

**Als Reviewee:**
- [ ] Feedback konstruktiv umsetzen
- [ ] Diskussionen klären
- [ ] Changes committen
- [ ] Re-Review anfragen

### 8. Nach Merge: Cleanup 🧹

```bash
# Branch löschen (lokal)
git branch -d feature/exchange-proposals

# Branch löschen (remote)
git push origin --delete feature/exchange-proposals

# Main/Develop Branch aktualisieren
git checkout main
git pull
```

## Spezielle Checklists

### Nach UI-Implementierung 🎨

- [ ] Responsive Design getestet (Desktop, Tablet, Mobile)
- [ ] Browser-Kompatibilität getestet (Chrome, Firefox, Safari, Edge)
- [ ] Accessibility geprüft (Keyboard Navigation, Screen Reader)
- [ ] Loading States implementiert
- [ ] Error States implementiert
- [ ] HTMX funktioniert korrekt
- [ ] Alpine.js Interaktionen funktionieren
- [ ] Dark Theme konsistent

**Test-Devices:**
- [ ] Desktop (1920x1080)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

### Nach API-Implementierung 🔌

- [ ] OpenAPI/Swagger Docs korrekt
- [ ] Request/Response Validation mit Pydantic
- [ ] Error Handling für alle Edge Cases
- [ ] HTTP Status Codes korrekt (200, 201, 400, 401, 403, 404, 500)
- [ ] Authentication/Authorization geprüft
- [ ] Rate Limiting berücksichtigt (wenn implementiert)
- [ ] API Tests (Integration) geschrieben

**API Test-Checklist:**
- [ ] Happy Path getestet
- [ ] Invalid Input getestet (400)
- [ ] Unauthorized Access getestet (401)
- [ ] Forbidden Access getestet (403)
- [ ] Not Found getestet (404)
- [ ] Server Error Handling getestet (500)

### Nach Database-Änderungen 💾

- [ ] Migration erstellt und getestet
- [ ] Indexes hinzugefügt (falls nötig)
- [ ] Constraints definiert (NOT NULL, UNIQUE, FK)
- [ ] Rollback-Strategie dokumentiert
- [ ] Performance-Impact geprüft (bei großen Tabellen)
- [ ] Backup vor Production-Deployment

### Nach Security-relevanten Änderungen 🔒

- [ ] Input Validation vollständig
- [ ] SQL Injection Prevention (PonyORM schützt automatisch)
- [ ] XSS Prevention (Template Escaping)
- [ ] CSRF Protection (falls Cookies verwendet)
- [ ] Authentication geprüft
- [ ] Authorization geprüft
- [ ] Sensitive Data nicht geloggt
- [ ] Passwörter gehasht (bcrypt)

**Security Checklist:**
- [ ] Keine Plaintext Passwords
- [ ] Keine API Keys in Code
- [ ] Keine Sensitive Data in Logs
- [ ] Input Validation auf Server-Side
- [ ] HTTPS in Production

## Deployment Checklist (Production)

### Pre-Deployment ✅

- [ ] Alle Tests grün (lokal)
- [ ] CI/CD Pipeline grün (falls vorhanden)
- [ ] Code Review abgeschlossen
- [ ] Changelog aktualisiert
- [ ] Migration getestet
- [ ] Backup erstellt

### Deployment 🚀

```bash
# 1. Database Backup
python scripts/backup_database.py

# 2. Pull latest code
git pull origin main

# 3. Dependencies updaten
uv sync

# 4. Migrations anwenden
alembic upgrade head

# 5. Tests ausführen
pytest

# 6. Server neu starten
systemctl restart hcc-plan-web  # Linux
# oder
docker-compose restart          # Docker
```

### Post-Deployment ✅

- [ ] Health Check erfolgreich (`/health`)
- [ ] API erreichbar
- [ ] Login funktioniert
- [ ] Kritische User Flows getestet
- [ ] Monitoring prüfen (Logs, Metrics)
- [ ] Error Rate normal
- [ ] Response Times normal

### Rollback Plan (falls nötig) 🔄

```bash
# 1. Code zurücksetzen
git checkout <previous-commit>

# 2. Migration rückgängig
alembic downgrade -1

# 3. Server neu starten
systemctl restart hcc-plan-web

# 4. Database Restore (worst case)
cp data/backups/hcc_plan_backup_*.sqlite data/hcc_plan.sqlite
```

## Kommunikation

### Mit Team 📢

**Nach Feature-Completion:**
- [ ] Team informieren (Slack/E-Mail)
- [ ] Neue Features demonstrieren (Demo-Session)
- [ ] Dokumentation teilen

**Bei Breaking Changes:**
- [ ] Frühzeitig kommunizieren
- [ ] Migration Guide schreiben
- [ ] Koordinierte Deployment planen

### Mit Thomas (Projekt-Owner) 💬

**Vor größeren Änderungen:**
- [ ] Architektur-Entscheidungen abstimmen
- [ ] Strukturelle Änderungen genehmigen lassen
- [ ] Timeline kommunizieren

**Nach Implementierung:**
- [ ] Status-Update geben
- [ ] Demo vorbereiten
- [ ] Feedback einholen

## Quick Reference: "Done" Definition

Ein Task ist "Done" wenn:
- ✅ Code geschrieben
- ✅ Code formatiert (black, isort)
- ✅ Type Checking erfolgreich (mypy)
- ✅ Tests geschrieben und grün
- ✅ Coverage > 80%
- ✅ Dokumentiert (Docstrings, Comments)
- ✅ Git Commit mit guter Message
- ✅ Pull Request erstellt
- ✅ Code Review bestanden
- ✅ Merged to main/develop
- ✅ Deployed (falls Production-Ready)
- ✅ Monitoring zeigt keine Probleme

## Häufige Fehler vermeiden ❌

**Nicht tun:**
- ❌ Committen ohne Tests
- ❌ Pushen ohne Formatierung
- ❌ Deployment ohne Backup
- ❌ Breaking Changes ohne Kommunikation
- ❌ Sensitive Data committen (.env, API Keys)
- ❌ Debug-Code in Production
- ❌ Hardcoded Values (statt Environment Variables)
- ❌ Ignore von Type Errors (ohne guten Grund)

**Immer tun:**
- ✅ Tests vor Commit
- ✅ Code Review vor Merge
- ✅ Backup vor Deployment
- ✅ Dokumentation aktualisieren
- ✅ Type Hints verwenden
- ✅ Error Handling implementieren
- ✅ Security prüfen
- ✅ Performance berücksichtigen
