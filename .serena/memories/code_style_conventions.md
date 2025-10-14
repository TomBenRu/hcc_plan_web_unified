# Code Style und Konventionen

## Programmiersprache
- **Python 3.12+** mit modernen Features
- **Type Hints** durchgehend verwendet (Pydantic, typing)
- **Deutsch als Kommentarsprache** - Kommentare und Docstrings in deutscher Sprache

## Namenskonventionen
- **snake_case** für Funktionen, Variablen und Module
- **PascalCase** für Klassen
- **UPPER_CASE** für Konstanten
- **Beschreibende Namen** - Keine Abkürzungen außer bei Standards (id, url, etc.)

### Beispiele
```python
# Gut
def get_available_actors(plan_period_id: UUID) -> list[Person]:
    """Holt alle verfügbaren Actors für eine Planperiode."""
    pass

# Schlecht
def getAvlActors(ppId):  # CamelCase, Abkürzungen
    pass
```

## Pydantic & FastAPI Konventionen

### Schemas
- **Suffix-Konvention**:
  - `Create` für POST-Requests (z.B. `ExchangeProposalCreate`)
  - `Update` für PUT/PATCH-Requests (z.B. `ExchangeProposalUpdate`)
  - `Response` für API-Responses (z.B. `ExchangeProposalResponse`)
  - Basis-Schema ohne Suffix für gemeinsame Felder

```python
class ExchangeProposalBase(BaseModel):
    """Basis-Felder für Tauschvorschläge"""
    notes: str

class ExchangeProposalCreate(ExchangeProposalBase):
    """Erstellen eines Tauschvorschlags"""
    appointment_offered_id: UUID
    appointment_wanted_id: Optional[UUID] = None

class ExchangeProposalResponse(ExchangeProposalBase):
    """API-Response für Tauschvorschlag"""
    id: UUID
    status: str
    created_at: datetime
    proposer: PersonResponse
```

### API Routes
- **Prefix mit Version**: `/api/v1/...`
- **Plural für Ressourcen**: `/api/v1/appointments` (nicht `/api/v1/appointment`)
- **RESTful Konventionen**:
  - `GET /api/v1/appointments` - Liste
  - `GET /api/v1/appointments/{id}` - Detail
  - `POST /api/v1/appointments` - Erstellen
  - `PUT /api/v1/appointments/{id}` - Vollständiges Update
  - `PATCH /api/v1/appointments/{id}` - Partielles Update
  - `DELETE /api/v1/appointments/{id}` - Löschen

## Service Layer Pattern

### Services Konvention
- **Ein Service pro Entity** (z.B. `AppointmentService`, `ExchangeProposalService`)
- **Statische Methoden** oder **Klassen-Methoden** bevorzugt
- **Keine Business Logic in Routes** - nur in Services

```python
# api/services/exchange_proposal_service.py

class ExchangeProposalService:
    """Service für Tauschvorschläge Business Logic"""
    
    @staticmethod
    @db_session
    def create_proposal(
        proposer_id: UUID,
        appointment_offered_id: UUID,
        appointment_wanted_id: Optional[UUID],
        notes: str
    ) -> ExchangeProposal:
        """
        Erstellt einen neuen Tauschvorschlag.
        
        Args:
            proposer_id: ID des vorschlagenden Actors
            appointment_offered_id: ID des angebotenen Einsatzes
            appointment_wanted_id: ID des gewünschten Einsatzes (optional)
            notes: Nachricht an CvO
            
        Returns:
            Erstellter Tauschvorschlag
            
        Raises:
            InvalidProposalError: Bei ungültigen Daten
        """
        # Business Logic hier
        pass
```

## Exception Handling

### Domain-Specific Exceptions
- **Eigene Exception-Hierarchie** pro Domain
- **Exceptions im `api/exceptions/` Ordner**
- **Niemals generische Exceptions in Business Logic**

```python
# api/exceptions/exchange_proposal.py

class ExchangeProposalError(Exception):
    """Basis-Exception für Tauschvorschläge"""
    pass

class InvalidProposalError(ExchangeProposalError):
    """Tauschvorschlag ist ungültig"""
    pass

class ProposalAlreadyReviewedError(ExchangeProposalError):
    """Tauschvorschlag wurde bereits bearbeitet"""
    pass
```

## Database (PonyORM) Konventionen

### Entity Naming
```python
from pony.orm import Required, Optional as PonyOptional, Set

class ExchangeProposal(db.Entity):
    """PonyORM Entity für Tauschvorschläge"""
    
    # Primary Key - immer UUID
    id = PrimaryKey(UUID, auto=True)
    
    # Required Fields
    proposer = Required('Person')
    status = Required(str)
    created_at = Required(datetime, default=utcnow_naive)
    
    # Optional Fields - PonyOptional statt Optional!
    reviewed_by = PonyOptional('Person')
    notes = PonyOptional(str)
    
    # Relationships
    plan_version = Required('PlanVersion')
    notifications = Set('Notification')
```

### Wichtig: `Optional` vs `PonyOptional`
```python
from typing import Optional  # Für Type Hints
from pony.orm import Optional as PonyOptional  # Für PonyORM

# In PonyORM Entities:
notes = PonyOptional(str)  # Datenbank-Optional

# In Pydantic Schemas:
notes: Optional[str] = None  # Type Hint Optional
```

## Template Konventionen (Jinja2)

### Naming
- **Lowercase mit Unterstrichen**: `appointment_detail_modal.html`
- **Partials mit `_partial` Suffix**: `calendar_partial.html`
- **Modals mit `_modal` Suffix**: `exchange_proposal_modal.html`

### Structure
```html
<!-- templates/actor/exchange_proposal_modal.html -->

{# Kommentare in Jinja2 mit {# #} #}

{# HTMX Attribute für interaktive Elemente #}
<button 
    hx-post="/api/v1/exchange-proposals"
    hx-target="#modal-container"
    hx-swap="innerHTML"
    class="btn-primary"
>
    Vorschlag senden
</button>
```

## Tailwind CSS Konventionen

### Custom Colors (in tailwind-config.js)
```javascript
colors: {
    'dark-900': '#121212',
    'dark-800': '#1a1a1a',
    'dark-700': '#2a2a2a',
    'dark-600': '#3a3a3a',
    'primary-900': '#004d4d',  // Teal dunkel
    'primary-800': '#006666',
    'primary-700': '#008080',
    'primary-600': '#009999',
    'primary-300': '#40d4d4',  // Teal hell
}
```

### Class Ordering (empfohlen)
1. Layout (flex, grid, etc.)
2. Sizing (w-, h-, etc.)
3. Spacing (p-, m-, etc.)
4. Colors (bg-, text-, etc.)
5. Typography (font-, text-size, etc.)
6. Effects (shadow-, etc.)
7. Transitions

```html
<!-- Gut geordnet -->
<div class="flex items-center justify-between w-full px-4 py-2 bg-dark-800 text-primary-300 rounded-lg shadow-md hover:bg-dark-700 transition-colors">
```

## Testing Konventionen

### Test File Naming
- **`test_*.py`** für Test-Dateien
- **Mirror der Source-Struktur** in `tests/`

```
api/
  services/
    exchange_proposal_service.py
tests/
  services/
    test_exchange_proposal_service.py
```

### Test Naming
```python
def test_create_exchange_proposal_success():
    """Test: Erfolgreiche Erstellung eines Tauschvorschlags"""
    pass

def test_create_exchange_proposal_invalid_appointment():
    """Test: Fehlschlag bei ungültigem Einsatz"""
    pass
```

## Code Formatting

### Black Configuration
```toml
[tool.black]
line-length = 100
target-version = ['py312']
```

### Isort Configuration
```toml
[tool.isort]
profile = "black"
line_length = 100
```

## Docstrings

### Google Style (für Funktionen/Methoden)
```python
def create_exchange_proposal(
    proposer_id: UUID,
    appointment_offered_id: UUID,
    notes: str
) -> ExchangeProposal:
    """
    Erstellt einen neuen Tauschvorschlag.
    
    Args:
        proposer_id: ID des vorschlagenden Actors
        appointment_offered_id: ID des angebotenen Einsatzes
        notes: Nachricht an CvO
        
    Returns:
        Erstellter Tauschvorschlag
        
    Raises:
        InvalidProposalError: Bei ungültigen Daten
        DatabaseError: Bei Datenbankfehlern
    """
    pass
```

### Für Klassen
```python
class ExchangeProposalService:
    """
    Service für Tauschvorschläge Business Logic.
    
    Verantwortlich für:
    - Erstellung von Tauschvorschlägen
    - Validierung von Vorschlägen
    - Benachrichtigung von CvOs
    """
    pass
```

## Import Ordering (isort)

```python
# Standard Library
import datetime
from typing import Optional
from uuid import UUID

# Third Party
from fastapi import APIRouter, Depends, HTTPException
from pony.orm import db_session
from pydantic import BaseModel

# Local Application
from api.models.schemas import ExchangeProposalCreate
from api.services.exchange_proposal_service import ExchangeProposalService
from database.models.entities import ExchangeProposal
```

## Git Commit Messages

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: Neues Feature
- `fix`: Bug Fix
- `docs`: Dokumentation
- `style`: Code-Formatierung
- `refactor`: Code-Refactoring
- `test`: Tests
- `chore`: Build-Prozess, Dependencies

### Beispiele
```
feat(collaboration): Tauschvorschläge erstellen und genehmigen

- ExchangeProposal Entity erstellt
- API Endpoints implementiert
- CvO Dashboard integriert

Closes #42
```

## Performance Best Practices

### Database Queries
```python
# Gut - Lazy Loading vermeiden mit select_related
@db_session
def get_proposals_with_details(plan_version_id: UUID):
    proposals = select(
        p for p in ExchangeProposal 
        if p.plan_version.id == plan_version_id
    ).prefetch(ExchangeProposal.proposer, ExchangeProposal.appointment_offered)
    return list(proposals)

# Schlecht - N+1 Query Problem
proposals = select(p for p in ExchangeProposal)
for p in proposals:
    print(p.proposer.name)  # Separate Query für jeden Proposer!
```

### Async/Await
```python
# Async Endpoints bevorzugen
@router.get("/appointments")
async def get_appointments(
    current_user: Person = Depends(get_current_user)
):
    # Async I/O Operationen
    return await some_async_function()
```

## Security Best Practices

### Password Hashing
```python
# Gut - Direkt mit bcrypt arbeiten
import bcrypt

# Password hashen
password_bytes = password.encode('utf-8')
hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

# Password verifizieren
is_valid = bcrypt.checkpw(password_bytes, hashed)

# WICHTIG: bcrypt verwenden, NICHT passlib (wird nicht mehr gewartet)
```

### Nie Passwörter loggen
```python
# Gut
logger.info(f"User {user.email} logged in")

# Schlecht
logger.info(f"User {user.email} with password {password} logged in")
```

### SQL Injection Prevention
```python
# Gut - PonyORM schützt automatisch
actors = select(a for a in Person if a.email == user_email)

# Schlecht - Raw SQL vermeiden (wenn nötig, Parameterized Queries)
# db.execute(f"SELECT * FROM Person WHERE email = '{user_email}'")
```
