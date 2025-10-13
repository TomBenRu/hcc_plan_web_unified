# Entwicklungsrichtlinien und Best Practices

## 0. KEEP IT SIMPLE - Philosophie (Oberste Priorität)
**Motto**: *"Besser simpel und funktionabel als kompliziert und verbugged"*

- **Einfachheit vor Features** - Funktionalität ist wichtiger als Perfektion
- **Radikale Vereinfachung bevorzugen** - Weniger Code = weniger Bugs
- **Komplexe Lösungen hinterfragen** - Oft gibt es einfachere Wege
- **Bewährte Patterns nutzen** - Keine Neuerfindung des Rades
- **Minimale Änderungen bevorzugen** - Bestehende Strukturen erweitern statt neu bauen
- **Zero-Configuration** - System soll automatisch funktionieren
- **Standards befolgen** - REST API Best Practices, HTTP Status Codes

**Praktische Anwendung:**
- Vor komplexer Implementierung: "Geht es auch einfacher?"
- Bei Bugs: "Können wir das Problem vereinfachen statt erweitern?"
- Bei Features: "Brauchen wir wirklich alle diese Optionen?"
- Bei Architektur: "Ist das die einfachste Lösung die funktioniert?"

## 1. Architektur-Prinzipien

### Service Layer Pattern
- **Alle Business Logic in Services** - Routes sind nur Adapter
- **Ein Service pro Entity** - `AppointmentService`, `ExchangeProposalService`
- **Services sind stateless** - Keine Instance-Variablen mit State
- **Transactional Boundaries** - `@db_session` Decorator bei DB-Operationen

```python
# Gut
class ExchangeProposalService:
    @staticmethod
    @db_session
    def create_proposal(...) -> ExchangeProposal:
        # Business Logic hier
        pass

# Schlecht - Business Logic in Route
@router.post("/proposals")
async def create_proposal(...):
    # DB-Zugriff direkt in Route - VERMEIDEN!
    proposal = ExchangeProposal(...)
```

### Exception-Driven Development
- **Domain-specific Exceptions** - Nie generische `Exception`
- **Exceptions in `api/exceptions/`** - Strukturiert nach Domain
- **Global Exception Handler** - In Middleware
- **HTTP Status Codes** - Automatisch aus Exception-Typ ableiten

```python
# api/exceptions/exchange_proposal.py
class ExchangeProposalError(Exception):
    """Basis für alle Tauschvorschlag-Errors"""
    pass

class InvalidProposalError(ExchangeProposalError):
    """Tauschvorschlag ist ungültig"""
    http_status = 400

# api/middleware/error_handler.py
@app.exception_handler(ExchangeProposalError)
async def handle_exchange_proposal_error(request, exc):
    return JSONResponse(
        status_code=exc.http_status,
        content={"detail": str(exc)}
    )
```

### API-First Design
- **OpenAPI/Swagger Docs** - Automatisch generiert, immer aktuell
- **Pydantic Schemas** - Type-Safe API-Contracts
- **Versionierung** - `/api/v1/...` für Breaking Changes
- **Consistent Response Format** - Einheitliche Error-Responses

## 2. Workflow-Guidelines

### Feature Development Process
1. **Schema definieren** - Pydantic Models zuerst
2. **Service implementieren** - Business Logic
3. **Tests schreiben** - Service-Layer Tests
4. **Route implementieren** - API Endpoint
5. **Frontend implementieren** - Template + HTMX
6. **Integration testen** - End-to-End

### Pull Request Checklist
- [ ] Tests geschrieben und bestanden
- [ ] Type Hints vollständig
- [ ] Docstrings vorhanden
- [ ] Black + isort ausgeführt
- [ ] mypy ohne Fehler
- [ ] OpenAPI Docs aktualisiert (automatisch)
- [ ] Migration erstellt (falls DB-Änderungen)

## 3. Testing Strategy

### Test Pyramid
```
      /\        E2E Tests (wenige)
     /  \       
    /____\      Integration Tests (mittel)
   /      \     
  /________\    Unit Tests (viele)
```

### Test Coverage Ziele
- **Unit Tests**: 80%+ Coverage
- **Service Layer**: 90%+ Coverage
- **Critical Paths**: 100% Coverage (Auth, Permissions, Payment)

### Test Naming Convention
```python
def test_<function>_<scenario>_<expected_result>():
    """Test: <Beschreibung in Deutsch>"""
    pass

# Beispiele
def test_create_exchange_proposal_success():
    """Test: Erfolgreiche Erstellung eines Tauschvorschlags"""
    pass

def test_create_exchange_proposal_invalid_appointment_raises_error():
    """Test: Fehlschlag bei ungültigem Einsatz wirft InvalidProposalError"""
    pass
```

## 4. Database Best Practices

### Migrations
- **Immer Migrations erstellen** - Auch für kleine Änderungen
- **Descriptive Names** - `add_exchange_proposal_table.py`
- **Rollback-fähig** - Immer `down()` Methode implementieren
- **Testbar** - Migration in Test-DB testen vor Production

### Query Optimization
```python
# Gut - Prefetch verwenden
@db_session
def get_proposals_with_actors():
    return select(p for p in ExchangeProposal).prefetch(
        ExchangeProposal.proposer,
        ExchangeProposal.appointment_offered
    )

# Schlecht - N+1 Problem
@db_session
def get_proposals():
    proposals = select(p for p in ExchangeProposal)
    for p in proposals:
        print(p.proposer.name)  # Separate Query!
```

### Transaction Management
```python
# Gut - db_session für Transaktionen
@db_session
def create_proposal_with_notification(...):
    proposal = ExchangeProposal(...)
    notification = Notification(...)
    # Beide werden in einer Transaktion committed

# Schlecht - Manuelle Transaktion (nur in Ausnahmefällen)
```

## 5. Security Guidelines

### Authentication & Authorization
- **JWT Tokens** - Access Tokens mit kurzer Lebensdauer (15 Min)
- **Refresh Tokens** - Längere Lebensdauer (7 Tage)
- **Role-Based Access Control** - Granulare Permissions
- **Never Trust Input** - Immer Pydantic Validation

### Password Handling
```python
# Gut
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash(password)

# Schlecht - NIEMALS Plaintext Passwords speichern!
```

### SQL Injection Prevention
- **PonyORM schützt automatisch** - Generator Expressions sind sicher
- **Nie Raw SQL** - Außer absolut notwendig, dann Parameterized

### CORS Configuration
```python
# Production: Nur erlaubte Origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Development: Localhost erlauben
allow_origins=["http://localhost:3000"]
```

## 6. Performance Guidelines

### Caching Strategy
- **Template Caching** - Jinja2 Template Compilation
- **Query Result Caching** - Für häufige, langsame Queries
- **Static File Caching** - Nginx/CDN für CSS/JS
- **Cache Invalidation** - Bei Datenänderungen

### Async Best Practices
```python
# Gut - Async für I/O-bound Operations
@router.get("/appointments")
async def get_appointments():
    # Async DB Query
    return await fetch_appointments_async()

# Schlecht - Async für CPU-bound Operations (bringt nichts)
@router.post("/calculate-plan")
async def calculate_plan():
    # CPU-intensive OR-Tools Berechnung
    return complex_calculation()  # Sollte sync sein
```

### Pagination
```python
# Immer Pagination für Listen-Endpoints
@router.get("/appointments")
def get_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000)
):
    return appointments[skip:skip+limit]
```

## 7. Frontend Best Practices (HTMX + Alpine.js)

### HTMX Patterns
```html
<!-- Gut - Partielle Updates -->
<button 
    hx-post="/api/v1/proposals"
    hx-target="#proposal-list"
    hx-swap="afterbegin"
>
    Erstellen
</button>

<!-- Gut - Loading States -->
<button 
    hx-post="/api/v1/proposals"
    hx-indicator="#spinner"
>
    Erstellen
</button>
<div id="spinner" class="htmx-indicator">Lädt...</div>
```

### Alpine.js Patterns
```html
<!-- Gut - Reactive State -->
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    <div x-show="open">Content</div>
</div>

<!-- Gut - Computed Properties -->
<div x-data="{ count: 0 }" x-init="$watch('count', value => console.log(value))">
    <span x-text="count"></span>
    <button @click="count++">Increment</button>
</div>
```

### Mobile-First Design
```html
<!-- Responsive Classes -->
<div class="
    px-4 py-2          <!-- Mobile -->
    md:px-6 md:py-4    <!-- Tablet -->
    lg:px-8 lg:py-6    <!-- Desktop -->
">
```

## 8. Logging & Monitoring

### Logging Levels
- **DEBUG**: Entwicklung, detaillierte Infos
- **INFO**: Wichtige Events (User Login, Plan Created)
- **WARNING**: Unerwartete Situationen (Deprecated API genutzt)
- **ERROR**: Fehler die behandelt wurden
- **CRITICAL**: Fehler die System-Stabilität gefährden

### Structured Logging
```python
import logging

logger = logging.getLogger(__name__)

# Gut - Structured
logger.info(
    "Exchange proposal created",
    extra={
        "user_id": user.id,
        "proposal_id": proposal.id,
        "action": "create_proposal"
    }
)

# Schlecht - Unstructured
logger.info(f"User {user.id} created proposal {proposal.id}")
```

### Health Checks
```python
@router.get("/health")
async def health_check():
    """Health Check Endpoint für Monitoring"""
    return {
        "status": "healthy",
        "database": check_db_connection(),
        "scheduler": check_scheduler_running(),
        "websocket": check_websocket_server()
    }
```

## 9. Deployment Guidelines

### Pre-Deployment Checklist
- [ ] Alle Tests grün
- [ ] Coverage-Ziele erfüllt
- [ ] Type Checking (mypy) fehlerfrei
- [ ] Security Audit (Dependencies)
- [ ] Database Migration getestet
- [ ] Environment Variables dokumentiert
- [ ] Logging konfiguriert
- [ ] Monitoring Setup

### Environment Variables
```bash
# .env.example (in Repo)
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your-secret-key-here
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

# .env (NICHT in Repo, in .gitignore)
DATABASE_URL=postgresql://prod-user:prod-pass@prod-db/prod-dbname
SECRET_KEY=actual-secret-production-key
```

### Database Backups
- **Automatische Backups** - Täglich, bevor Deployment
- **Retention Policy** - Mindestens 30 Tage
- **Backup Testing** - Monatlich Restore-Test

## 10. Documentation Standards

### API Documentation
- **OpenAPI/Swagger** - Automatisch aus FastAPI
- **Request/Response Examples** - Für jeden Endpoint
- **Error Responses** - Alle möglichen Fehler dokumentieren

### Code Documentation
```python
def create_exchange_proposal(
    proposer_id: UUID,
    appointment_offered_id: UUID
) -> ExchangeProposal:
    """
    Erstellt einen neuen Tauschvorschlag.
    
    Validiert:
    - Proposer ist Actor in dem Team
    - Appointment gehört zu Proposer
    - Appointment ist nicht bereits getauscht
    
    Args:
        proposer_id: ID des vorschlagenden Actors
        appointment_offered_id: ID des angebotenen Einsatzes
        
    Returns:
        Erstellter Tauschvorschlag
        
    Raises:
        InvalidProposalError: Bei Validierungsfehlern
        NotFoundError: Wenn Appointment nicht existiert
    """
    pass
```

### README Documentation
- **Project Setup** - Schritt-für-Schritt Anleitung
- **Running the App** - Development & Production
- **Testing** - Wie Tests ausführen
- **Deployment** - Deployment-Prozess
- **Contributing** - Contribution Guidelines

## 11. Git Workflow

### Branch Strategy
```
main          - Production-ready Code
develop       - Development Branch
feature/*     - Feature Branches
bugfix/*      - Bug Fix Branches
hotfix/*      - Production Hotfixes
```

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: Neues Feature
- `fix`: Bug Fix
- `docs`: Dokumentation
- `style`: Formatierung
- `refactor`: Code-Refactoring
- `test`: Tests
- `chore`: Build, Dependencies

**Beispiel:**
```
feat(collaboration): Tauschvorschläge erstellen und genehmigen

- ExchangeProposal Entity erstellt
- API Endpoints /api/v1/exchange-proposals implementiert
- CvO Dashboard mit Tauschvorschlag-Liste

Closes #42
```

## 12. Communication Guidelines

### Mit dem Team
- **Daily Standups** - Was gestern, was heute, Blocker?
- **Code Reviews** - Konstruktives Feedback
- **Documentation** - Entscheidungen dokumentieren
- **Knowledge Sharing** - Pair Programming, Tech Talks

### Mit Thomas (Projekt-Owner)
- **Vor strukturellen Änderungen**: Immer um Erlaubnis fragen
- **Nach Implementierung**: Status-Update und Test-Ergebnisse
- **Bei Problemen**: Sofort kommunizieren
- **Architektur-Entscheidungen**: Gemeinsam treffen

## 13. Troubleshooting Common Issues

### Database Connection Issues
```python
# Check Database Connection
@db_session
def check_db():
    try:
        select(p for p in Person).first()
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
```

### CORS Issues
```python
# Ensure CORS Middleware is added BEFORE routes
app.add_middleware(CORSMiddleware, ...)
app.include_router(router)  # After middleware!
```

### Static Files Not Loading
```python
# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ensure directory exists
# static/css/, static/js/, etc.
```
