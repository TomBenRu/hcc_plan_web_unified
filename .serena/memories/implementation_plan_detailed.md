# Ausführlicher Implementierungsplan - hcc_plan_web_unified

## Executive Summary

Dieses Dokument beschreibt den vollständigen Implementierungsplan für die Entwicklung von **hcc_plan_web_unified**, einer kollaborativen Einsatzplanungs-Webapplikation. Der Plan basiert auf unseren Diskussionen und kombiniert die besten Features aus drei bestehenden Systemen.

**Projektziele:**
- Modernes, mobile-first Web-Interface
- Kollaborative Planungsworkflows (Tauschvorschläge, Review-Prozesse)
- Integration mit bestehender Desktop-App für komplexe Planung
- Verbesserte User Experience für alle Rollen (employees, CvOs, Dispatcher)

**Zeitrahmen:** 22 Wochen (ca. 5.5 Monate) für MVP + Full Feature Set
- **MVP**: 12 Wochen (3 Monate)
- **Full Feature Set**: Weitere 10 Wochen (2.5 Monate)

---

## Phase 1: Foundation & Setup (Wochen 1-2)

### Ziel
Projektgrundlage schaffen mit korrektem Setup und Infrastruktur.

### 1.1 Repository & Environment Setup (Woche 1)

#### Aufgaben
- [x] Repository erstellt (`hcc_plan_web_unified`)
- [ ] `.gitignore` konfigurieren
  - Python: `__pycache__/`, `.venv/`, `*.pyc`
  - IDE: `.idea/`, `.vscode/`
  - Environment: `.env`, `*.sqlite`
  - Build: `dist/`, `build/`
- [ ] `pyproject.toml` erstellen mit Dependencies:
  ```toml
  [project]
  name = "hcc-plan-web-unified"
  version = "0.1.0"
  requires-python = ">=3.12"
  dependencies = [
      "fastapi>=0.104.1",
      "uvicorn>=0.24.0",
      "pydantic>=2.4.2",
      "pydantic-settings>=2.0.0",
      "pony>=0.7.16",
      "python-jose>=3.3.0",
      "bcrypt>=5.0.0",
      "python-multipart>=0.0.6",
      "email-validator>=2.1.0",
      "jinja2>=3.1.2",
      "apscheduler>=3.10.0",
      "python-dotenv>=1.0.0",
  ]
  
  [project.optional-dependencies]
  dev = [
      "pytest>=7.4.0",
      "pytest-cov>=4.1.0",
      "black>=23.7.0",
      "isort>=5.12.0",
      "mypy>=1.5.1",
  ]
  ```
- [ ] Virtual Environment erstellen: `uv venv`
- [ ] Dependencies installieren: `uv sync`
- [ ] `.env.example` erstellen mit Template
- [ ] `.env` erstellen (nicht in Git) mit lokalen Werten
- [ ] README.md mit Setup-Anleitung

#### Deliverables
- ✅ Funktionierendes Python Environment
- ✅ Alle Dependencies installiert
- ✅ Git Repository initialisiert

### 1.2 Projektstruktur & Basis-App (Woche 1-2)

#### Aufgaben
- [ ] Verzeichnisstruktur erstellen (siehe project_structure.md)
- [ ] `main.py` mit FastAPI App Setup:
  ```python
  from fastapi import FastAPI
  from fastapi.staticfiles import StaticFiles
  from contextlib import asynccontextmanager
  
  from database.db_setup import init_db
  from api.routes.api import auth, appointments
  from api.routes.web import index
  from api.middleware.error_handler import setup_exception_handlers
  
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      # Startup
      init_db()
      yield
      # Shutdown
  
  app = FastAPI(
      title="HCC Plan Web Unified",
      description="Kollaborative Einsatzplanungs-Webapplikation",
      version="0.1.0",
      lifespan=lifespan
  )
  
  # Static Files
  app.mount("/static", StaticFiles(directory="static"), name="static")
  
  # Exception Handlers
  setup_exception_handlers(app)
  
  # Routes
  app.include_router(index.router)
  app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
  ```
- [ ] `database/db_setup.py` mit PonyORM Configuration:
  ```python
  from pony.orm import Database
  
  db = Database()
  
  def init_db():
      db.bind(
          provider='sqlite',
          filename='data/hcc_plan.sqlite',
          create_db=True
      )
      db.generate_mapping(create_tables=True)
  ```
- [ ] Basic `templates/base.html` mit Tailwind CSS
- [ ] Basic `static/` Struktur (css/, js/, images/)
- [ ] Health Check Endpoint:
  ```python
  @app.get("/health")
  async def health_check():
      return {"status": "healthy"}
  ```

#### Deliverables
- ✅ Lauffähige FastAPI App
- ✅ Basis-Projektstruktur
- ✅ Health Check funktioniert

### 1.3 Design-System etablieren (Woche 2)

#### Aufgaben
- [ ] Tailwind CSS Setup in `static/js/tailwind-config.js`:
  ```javascript
  tailwind.config = {
      theme: {
          extend: {
              colors: {
                  'dark-900': '#121212',
                  'dark-800': '#1a1a1a',
                  'dark-700': '#2a2a2a',
                  'dark-600': '#3a3a3a',
                  'primary-900': '#004d4d',
                  'primary-800': '#006666',
                  'primary-700': '#008080',
                  'primary-600': '#009999',
                  'primary-300': '#40d4d4',
              }
          }
      }
  }
  ```
- [ ] `templates/base.html` mit Dark Theme & Navigation
- [ ] `templates/components/` für wiederverwendbare Komponenten:
  - `navigation.html`
  - `loading_spinner.html`
  - `breadcrumbs.html`
- [ ] `static/css/styles.css` für Custom CSS
- [ ] HTMX Integration in base.html
- [ ] Alpine.js Integration in base.html
- [ ] Color Utilities (`static/js/colorUtils.js`) von appointment_plan_api_cl portieren

#### Deliverables
- ✅ Konsistentes Dark Theme Design
- ✅ Responsive Navigation
- ✅ HTMX & Alpine.js funktionsfähig

### Phase 1 Success Criteria
- [ ] FastAPI App läuft auf http://localhost:8000
- [ ] `/health` Endpoint gibt 200 zurück
- [ ] Dark Theme wird korrekt gerendert
- [ ] Tailwind CSS Klassen funktionieren
- [ ] Verzeichnisstruktur vollständig

---

## Phase 2: Database & Core Entities (Wochen 3-6)

### Ziel
Unified Database Schema erstellen mit allen Entities aus allen drei Projekten.

### 2.1 Core Entities (Woche 3)

#### Aufgaben
- [ ] `database/models/base.py` mit Database Instance
- [ ] `database/models/auth.py` mit User Entity:
  ```python
  class User(db.Entity):
      id = PrimaryKey(UUID, auto=True)
      email = Required(str, unique=True)
      hashed_password = Required(str)
      is_active = Required(bool, default=True)
      is_admin = Required(bool, default=False)
      person = Optional('Person')
      created_at = Required(datetime, default=utcnow_naive)
  ```
- [ ] `database/models/core.py` mit Person, Team, Project:
  ```python
  class Person(db.Entity):
      id = PrimaryKey(UUID, auto=True)
      f_name = Required(str)
      l_name = Required(str)
      email = Optional(str)
      project = Optional('Project')
      team_of_employee = Optional('Team')
      teams_of_dispatcher = Set('Team')
      user = Optional('User')
      # ... weitere Felder
  
  class Team(db.Entity):
      id = PrimaryKey(UUID, auto=True)
      name = Required(str, 50)
      employees = Set(Person, reverse='team_of_employee')
      dispatcher = Required(Person, reverse='teams_of_dispatcher')
      project = Required('Project')
      # ... weitere Felder
  
  class Project(db.Entity):
      id = PrimaryKey(UUID, auto=True)
      name = Required(str, 50, unique=True)
      active = Required(bool, default=True)
      persons = Set('Person')
      teams = Set('Team')
      admin = Optional('Person')
  ```

#### Deliverables
- ✅ Core Entities funktionsfähig
- ✅ Relationships korrekt definiert
- ✅ Database Tables werden erstellt

### 2.2 Planning Entities (Woche 4)

#### Aufgaben
- [ ] `database/models/planning.py`:
  ```python
  class PlanPeriod(db.Entity):
      id = PrimaryKey(UUID, auto=True)
      name = Required(str)
      start_date = Required(date)
      end_date = Required(date)
      project = Required('Project')
      teams = Set('Team')
      plans = Set('Plan')
      appointments = Set('Appointment')
      # ... weitere Felder
  
  class Plan(db.Entity):
      id = PrimaryKey(UUID, auto=True)
      name = Required(str)
      notes = Optional(str)
      plan_period = Required('PlanPeriod')
      appointments = Set('Appointment')
      # ... weitere Felder
  
  class Appointment(db.Entity):
      id = PrimaryKey(UUID, auto=True)
      plan_period = Required('PlanPeriod')
      date = Required(date)
      start_time = Required(time)
      delta = Required(timedelta)
      location = Required('LocationOfWork')
      persons = Set('Person')
      guests = Required(Json, default=[])
      plans = Set('Plan')
      # ... weitere Felder
  ```
- [ ] `database/models/location.py`:
  ```python
  class Address(db.Entity):
      id = PrimaryKey(UUID, auto=True)
      street = Required(str)
      postal_code = Required(str)
      city = Required(str)
      locations = Set('LocationOfWork')
  
  class LocationOfWork(db.Entity):
      id = PrimaryKey(UUID, auto=True)
      name = Required(str)
      address = Required(Address)
      appointments = Set('Appointment')
  ```

#### Deliverables
- ✅ Planning Entities vollständig
- ✅ Location Entities integriert
- ✅ Relationships funktionieren

### 2.3 Availability Entities (Woche 5)

#### Aufgaben
- [ ] `database/models/availability.py`:
  ```python
  class Availables(db.Entity):
      """Verfügbarkeit eines employees für eine Planperiode"""
      id = PrimaryKey(UUID, auto=True)
      person = Required('Person')
      plan_period = Required('PlanPeriod')
      created_at = Required(datetime, default=utcnow_naive)
      last_modified = Required(datetime, default=utcnow_naive)
      avail_days = Set('AvailDay')
      # ... weitere Felder
  
  class AvailDay(db.Entity):
      """Spezifischer verfügbarer Tag"""
      id = PrimaryKey(UUID, auto=True)
      availables = Required('Availables')
      date = Required(date)
      time_of_day = Required(str)  # 'morning', 'afternoon', 'evening'
      notes = Optional(str)
  ```

#### Deliverables
- ✅ Availability System funktionsfähig
- ✅ Integration mit Person und PlanPeriod

### 2.4 Collaboration Entities (Woche 6) - NEU

#### Aufgaben
- [ ] `database/models/collaboration.py`:
  ```python
  class PlanVersion(db.Entity):
      """Versionierung von Plänen"""
      id = PrimaryKey(UUID, auto=True)
      plan = Required('Plan')
      version_number = Required(int)
      status = Required(str)  # 'draft', 'in_review', 'approved', 'final'
      created_at = Required(datetime, default=utcnow_naive)
      created_by = Required('Person')
      notes = Optional(str)
      exchange_proposals = Set('ExchangeProposal')
      comments = Set('PlanComment')
  
  class ExchangeProposal(db.Entity):
      """Tauschvorschläge"""
      id = PrimaryKey(UUID, auto=True)
      plan_version = Required('PlanVersion')
      proposer = Required('Person')
      appointment_offered = Required('Appointment')
      appointment_wanted = Optional('Appointment')
      status = Required(str)  # 'pending', 'approved', 'rejected'
      created_at = Required(datetime, default=utcnow_naive)
      reviewed_by = Optional('Person')
      reviewed_at = Optional(datetime)
      review_notes = Optional(str)
  
  class PlanComment(db.Entity):
      """Kommentare zu Plänen"""
      id = PrimaryKey(UUID, auto=True)
      plan_version = Required('PlanVersion')
      appointment = Optional('Appointment')
      author = Required('Person')
      text = Required(str)
      created_at = Required(datetime, default=utcnow_naive)
      parent_comment = Optional('PlanComment')
  
  class CvORole(db.Entity):
      """Chief-Verantwortliche für Einrichtungen"""
      id = PrimaryKey(UUID, auto=True)
      person = Required('Person')
      location = Required('LocationOfWork')
      team = Required('Team')
      active = Required(bool, default=True)
  
  class Notification(db.Entity):
      """Push-Benachrichtigungen"""
      id = PrimaryKey(UUID, auto=True)
      recipient = Required('Person')
      type = Required(str)
      title = Required(str)
      message = Required(str)
      link = Optional(str)
      read = Required(bool, default=False)
      created_at = Required(datetime, default=utcnow_naive)
  ```

#### Deliverables
- ✅ Collaboration Entities vollständig
- ✅ Alle Relationships definiert
- ✅ Database Schema komplett

### Phase 2 Success Criteria
- [ ] Alle Entities erstellt und getestet
- [ ] Database Migrations funktionieren
- [ ] Seed Script erstellt für Test-Daten
- [ ] ER-Diagramm dokumentiert

---

## Phase 3: Authentication & Authorization (Wochen 7-8)

### Ziel
Vollständiges Auth-System mit JWT und rollenbasierter Zugriffskontrolle.

### 3.1 JWT Authentication (Woche 7)

#### Aufgaben
- [ ] `api/auth/jwt.py` mit Token-Generierung:
  ```python
  from jose import JWTError, jwt
  from datetime import datetime, timedelta
  
  def create_access_token(data: dict, expires_delta: timedelta = None):
      to_encode = data.copy()
      if expires_delta:
          expire = datetime.utcnow() + expires_delta
      else:
          expire = datetime.utcnow() + timedelta(minutes=15)
      to_encode.update({"exp": expire})
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt
  ```
- [ ] `api/auth/cookie_auth.py` für Cookie-based Auth
- [ ] Password Hashing mit bcrypt
- [ ] `api/models/auth.py` mit Login/Register Schemas:
  ```python
  class UserLogin(BaseModel):
      email: EmailStr
      password: str
  
  class UserRegister(BaseModel):
      email: EmailStr
      password: str
      f_name: str
      l_name: str
  
  class Token(BaseModel):
      access_token: str
      token_type: str = "bearer"
  ```
- [ ] `api/routes/api/auth.py` mit Login/Logout/Register Endpoints
- [ ] `templates/login_modal.html` von appointment_plan_api_cl portieren

#### Deliverables
- ✅ Login funktioniert
- ✅ JWT Tokens werden generiert
- ✅ Password Hashing sicher

### 3.2 Role-Based Access Control (Woche 8)

#### Aufgaben
- [ ] `api/auth/roles.py` mit Role-Definitionen:
  ```python
  class Role(str, Enum):
      ADMIN = "admin"
      DISPATCHER = "dispatcher"
      CVO = "cvo"
      EMPLOYEE = "employee"
  
  def require_role(required_roles: list[Role]):
      async def role_checker(
          current_user: User = Depends(get_current_user)
      ):
          if current_user.role not in required_roles:
              raise HTTPException(
                  status_code=403,
                  detail="Insufficient permissions"
              )
          return current_user
      return role_checker
  ```
- [ ] `api/auth/dependencies.py` mit Auth Dependencies:
  ```python
  async def get_current_user(
      token: str = Depends(oauth2_scheme)
  ) -> User:
      # Token validation
      # User lookup
      return user
  
  async def get_current_employee(
      current_user: User = Depends(get_current_user)
  ):
      if current_user.role != Role.EMPLOYEE:
          raise HTTPException(403)
      return current_user
  
  # Analog: get_current_cvo, get_current_dispatcher, get_current_admin
  ```
- [ ] Permission Decorators für Routes
- [ ] Integration in alle Protected Routes

#### Deliverables
- ✅ RBAC funktioniert
- ✅ Unauthorized Requests werden abgelehnt
- ✅ Role-spezifische Endpoints geschützt

### Phase 3 Success Criteria
- [ ] Login/Logout funktioniert
- [ ] JWT Tokens validieren korrekt
- [ ] RBAC verhindert unauthorized Zugriff
- [ ] Password Reset funktioniert

---

## Phase 4: Verfügbarkeitserfassung (Wochen 9-10)

### Ziel
employees können ihre Verfügbarkeiten für Planperioden eingeben (Feature von hcc_plan_api).

### 4.1 Verfügbarkeits-API (Woche 9)

#### Aufgaben
- [ ] `api/models/availability.py` mit Schemas
- [ ] `api/services/availability_service.py` mit Business Logic:
  ```python
  class AvailabilityService:
      @staticmethod
      @db_session
      def create_availability(
          person_id: UUID,
          plan_period_id: UUID,
          avail_days: list[AvailDayCreate]
      ) -> Availables:
          # Validierung
          # Erstellung
          # E-Mail-Benachrichtigung
          return availables
  
      @staticmethod
      @db_session
      def get_availability(
          person_id: UUID,
          plan_period_id: UUID
      ) -> Optional[Availables]:
          return select(...)
  ```
- [ ] `api/routes/api/availability.py` mit CRUD Endpoints
- [ ] E-Mail-Benachrichtigung bei Bestätigung

#### Deliverables
- ✅ Verfügbarkeits-API funktioniert
- ✅ CRUD Operations vollständig
- ✅ E-Mail bei Bestätigung

### 4.2 Verfügbarkeits-UI (Woche 10)

#### Aufgaben
- [ ] `templates/employee/availability.html` mit Kalenderansicht
- [ ] HTMX für Interaktivität:
  ```html
  <button 
      hx-post="/api/v1/availability"
      hx-target="#confirmation"
      hx-swap="innerHTML"
      class="btn-primary"
  >
      Verfügbarkeit speichern
  </button>
  ```
- [ ] Alpine.js für Client-Side State
- [ ] Responsive Design (Mobile-First)
- [ ] APScheduler für Erinnerungen:
  ```python
  @db_session
  def send_availability_reminders():
      # Finde alle offenen PlanPeriods mit Deadline < 7 Tage
      # Sende Reminder an employees ohne Verfügbarkeit
      pass
  ```

#### Deliverables
- ✅ Employees können Verfügbarkeit eingeben
- ✅ Mobile-responsive
- ✅ Reminder-E-Mails funktionieren

### Phase 4 Success Criteria
- [ ] Verfügbarkeitserfassung funktioniert End-to-End
- [ ] E-Mail-Bestätigung kommt an
- [ ] Reminder-System funktioniert
- [ ] Mobile-UI ist nutzbar

---

## Phase 5: Einsatzplan-Kalender (Wochen 11-12)

### Ziel
Employees sehen ihre Einsätze in moderner Kalenderansicht (Design von appointment_plan_api_cl).

### 5.1 Calendar Service & API (Woche 11)

#### Aufgaben
- [ ] `api/services/calendar_service.py`:
  ```python
  class CalendarService:
      @staticmethod
      @db_session
      def get_employee_appointments(
          person_id: UUID,
          start_date: date,
          end_date: date
      ) -> list[Appointment]:
          return select(...)
  
      @staticmethod
      def build_calendar_matrix(
          year: int,
          month: int,
          appointments: list[Appointment]
      ) -> list[list[CalendarDay]]:
          # Baut Kalender-Matrix für UI
          pass
  ```
- [ ] `api/routes/web/employee/calendar.py` mit Routes
- [ ] Filter-Funktionalität (Person, Location)

#### Deliverables
- ✅ Calendar Service funktioniert
- ✅ API gibt korrekte Daten zurück

### 5.2 Calendar UI (Woche 12)

#### Aufgaben
- [ ] `templates/employee/calendar.html` von appointment_plan_api_cl portieren
- [ ] `templates/employee/calendar_partial.html` für HTMX Updates
- [ ] Color-Coding für Locations (colorUtils.js)
- [ ] Modal für Appointment Details:
  ```html
  <div 
      hx-get="/calendar/hx/appointments/{{appointment.id}}/detail"
      hx-target="#modal-container"
      hx-swap="innerHTML"
  >
  ```
- [ ] Navigation (Monat vor/zurück, Heute-Button)
- [ ] Responsive Design & Touch-Optimierung

#### Deliverables
- ✅ Kalenderansicht funktioniert
- ✅ Filter funktionieren
- ✅ Modals öffnen sich
- ✅ Mobile-optimiert

### Phase 5 Success Criteria
- [ ] Employees sehen ihre Einsätze im Kalender
- [ ] Filter nach Person/Location funktioniert
- [ ] Detail-Modal zeigt alle Infos
- [ ] Navigation flüssig und responsive

---

## **MVP ERREICHT nach Phase 5 (Woche 12)** 🎉

### MVP Funktionen vollständig:
- ✅ Modernes Design mit Tailwind CSS
- ✅ Authentication & Authorization
- ✅ Verfügbarkeitserfassung
- ✅ Einsatzplan-Kalenderansicht
- ✅ E-Mail-Benachrichtigungen
- ✅ Mobile-responsive

**Entscheidungspunkt:** MVP testen mit echten Benutzern, Feedback sammeln, vor weiterer Entwicklung.

---

## Phase 6: Collaboration - Tauschvorschläge (Wochen 13-14)

### Ziel
Employees können Einsätze tauschen und CvOs können genehmigen.

### 6.1 Exchange Proposal Service & API (Woche 13)

#### Aufgaben
- [ ] `api/models/collaboration.py` mit Schemas:
  ```python
  class ExchangeProposalCreate(BaseModel):
      appointment_offered_id: UUID
      appointment_wanted_id: Optional[UUID] = None
      notes: str
  
  class ExchangeProposalResponse(BaseModel):
      id: UUID
      status: str
      proposer: PersonResponse
      appointment_offered: AppointmentResponse
      appointment_wanted: Optional[AppointmentResponse]
      created_at: datetime
  ```
- [ ] `api/services/collaboration/exchange_proposal_service.py`:
  ```python
  class ExchangeProposalService:
      @staticmethod
      @db_session
      def create_proposal(...) -> ExchangeProposal:
          # Validierung
          # Erstellung
          # Notification an CvO
          pass
  
      @staticmethod
      @db_session
      def approve_proposal(proposal_id: UUID, cvo_id: UUID):
          # Genehmigung
          # Einsatz tauschen
          # Notification an Employee
          pass
  
      @staticmethod
      @db_session
      def reject_proposal(proposal_id: UUID, cvo_id: UUID, reason: str):
          # Ablehnung
          # Notification an Employee
          pass
  ```
- [ ] `api/routes/api/collaboration/exchange_proposals.py` mit CRUD
- [ ] Notification Service Integration

#### Deliverables
- ✅ Exchange Proposal API funktioniert
- ✅ Business Logic korrekt
- ✅ Notifications werden gesendet

### 6.2 Exchange Proposal UI (Woche 14)

#### Aufgaben
- [ ] `templates/employee/exchange_proposal_modal.html`:
  - "Ich biete an" zeigt current Appointment
  - "Ich möchte" Dropdown mit verfügbaren Appointments
  - Nachricht an CvO Textarea
  - Submit Button
- [ ] "Tauschen"-Button in Calendar View
- [ ] Tauschvorschläge-Liste für Employee (eigene Vorschläge)
- [ ] Status-Anzeige (pending, approved, rejected)

#### Deliverables
- ✅ Employees können Tauschvorschläge erstellen
- ✅ UI intuitiv und mobile-friendly
- ✅ Status wird korrekt angezeigt

### Phase 6 Success Criteria
- [ ] Employee kann Tauschvorschlag erstellen
- [ ] CvO erhält Notification
- [ ] Status wird korrekt getrackt
- [ ] E-Mail-Benachrichtigungen funktionieren

---

## Phase 7: CvO Dashboard (Wochen 15-16)

### Ziel
CvOs haben Dashboard zur Verwaltung von Tauschvorschlägen und Team-Verfügbarkeit.

### 7.1 CvO Services (Woche 15)

#### Aufgaben
- [ ] `api/services/collaboration/cvo_service.py`:
  ```python
  class CvOService:
      @staticmethod
      @db_session
      def get_pending_proposals(cvo_id: UUID) -> list[ExchangeProposal]:
          # Hole alle offenen Tauschvorschläge für CvOs Einrichtungen
          pass
  
      @staticmethod
      @db_session
      def get_availability_matrix(
          location_id: UUID,
          start_date: date,
          end_date: date
      ) -> AvailabilityMatrix:
          # Wer ist wann verfügbar?
          pass
  
      @staticmethod
      def identify_critical_days(
          location_id: UUID,
          plan_period_id: UUID
      ) -> list[CriticalDay]:
          # Engpass-Erkennung
          pass
  ```
- [ ] `api/routes/web/cvo/dashboard.py` mit Routes

#### Deliverables
- ✅ CvO Services implementiert
- ✅ API Endpoints funktionieren

### 7.2 CvO Dashboard UI (Woche 16)

#### Aufgaben
- [ ] `templates/cvo/dashboard.html` (siehe Design im Implementierungsplan)
- [ ] Statistik-Cards (Offene Vorschläge, Verfügbare Employees, etc.)
- [ ] Tauschvorschläge-Liste mit Approve/Reject Buttons:
  ```html
  <button 
      hx-post="/api/v1/collaboration/proposals/{{proposal.id}}/approve"
      hx-target="#proposal-{{proposal.id}}"
      hx-swap="outerHTML"
      class="btn-approve"
  >
      ✓ Genehmigen
  </button>
  ```
- [ ] Verfügbarkeitsmatrix-Tabelle
- [ ] Engpass-Warnungen (farbliche Hervorhebung)
- [ ] Filter nach Zeitraum

#### Deliverables
- ✅ CvO Dashboard funktioniert
- ✅ Tauschvorschläge können genehmigt/abgelehnt werden
- ✅ Verfügbarkeitsmatrix übersichtlich

### Phase 7 Success Criteria
- [ ] CvO sieht alle offenen Tauschvorschläge
- [ ] Approve/Reject funktioniert
- [ ] Verfügbarkeitsmatrix ist hilfreich
- [ ] Engpässe werden erkannt

---

## Phase 8: Real-Time Updates (WebSocket) (Wochen 17-18)

### Ziel
Echtzeit-Benachrichtigungen für Tauschvorschläge und Planänderungen.

### 8.1 WebSocket Infrastructure (Woche 17)

#### Aufgaben
- [ ] `api/routes/websockets/connection_manager.py`:
  ```python
  class ConnectionManager:
      def __init__(self):
          self.active_connections: dict[UUID, list[WebSocket]] = {}
      
      async def connect(self, websocket: WebSocket, user_id: UUID):
          await websocket.accept()
          if user_id not in self.active_connections:
              self.active_connections[user_id] = []
          self.active_connections[user_id].append(websocket)
      
      async def broadcast_to_user(self, user_id: UUID, message: dict):
          if user_id in self.active_connections:
              for connection in self.active_connections[user_id]:
                  await connection.send_json(message)
  
      async def broadcast_to_team(self, team_id: UUID, message: dict):
          # Alle Team-Mitglieder benachrichtigen
          pass
  ```
- [ ] `api/routes/websockets/notifications.py` mit WebSocket Endpoint:
  ```python
  @router.websocket("/ws/{user_id}")
  async def websocket_endpoint(
      websocket: WebSocket,
      user_id: UUID,
      token: str = Query(...)
  ):
      # Auth via Token
      await manager.connect(websocket, user_id)
      try:
          while True:
              data = await websocket.receive_text()
              # Keepalive
      except WebSocketDisconnect:
          manager.disconnect(user_id, websocket)
  ```
- [ ] Integration in Services (bei Proposal Create/Approve/Reject)

#### Deliverables
- ✅ WebSocket Server funktioniert
- ✅ Connections werden verwaltet
- ✅ Broadcasts funktionieren

### 8.2 Frontend WebSocket Client (Woche 18)

#### Aufgaben
- [ ] `static/js/collaboration.js`:
  ```javascript
  class CollaborationClient {
      constructor(wsUrl, apiUrl, userId, token) {
          this.ws = new WebSocket(`${wsUrl}?token=${token}`);
          this.setupWebSocket();
      }
      
      setupWebSocket() {
          this.ws.onmessage = (event) => {
              const data = JSON.parse(event.data);
              this.handleMessage(data);
          };
      }
      
      handleMessage(data) {
          if (data.type === 'NEW_EXCHANGE_PROPOSAL') {
              this.showNotification('Neuer Tauschvorschlag', data);
              this.refreshProposalsList();
          }
          if (data.type === 'PROPOSAL_APPROVED') {
              this.showNotification('Tauschvorschlag genehmigt', data);
              this.refreshCalendar();
          }
      }
      
      showNotification(title, data) {
          // Toast-Notification anzeigen
      }
  }
  ```
- [ ] Integration in base.html
- [ ] Toast-Notifications für WebSocket Events
- [ ] Auto-Refresh von betroffenen UI-Elementen

#### Deliverables
- ✅ WebSocket Client funktioniert
- ✅ Notifications werden angezeigt
- ✅ UI aktualisiert sich automatisch

### Phase 8 Success Criteria
- [ ] WebSocket Verbindung stabil
- [ ] Echtzeit-Benachrichtigungen funktionieren
- [ ] UI aktualisiert sich ohne Manual Refresh
- [ ] Toast-Notifications sind benutzerfreundlich

---

## Phase 9: Desktop-App Integration (Wochen 19-20)

### Ziel
Desktop-App (hcc_plan_db_playground) kann Pläne hochladen und Tauschvorschläge abrufen.

### 9.1 API für Desktop-App (Woche 19)

#### Aufgaben
- [ ] `api/routes/api/integration/desktop.py` mit Endpoints:
  ```python
  @router.post("/plan-versions")
  async def upload_plan_version(
      plan_data: PlanVersionUpload,
      current_user: User = Depends(get_current_dispatcher)
  ):
      # Validierung
      # Plan-Upload
      # Status: "draft"
      pass
  
  @router.get("/plan-versions/{version_id}/proposals")
  async def get_proposals_for_version(
      version_id: UUID,
      current_user: User = Depends(get_current_dispatcher)
  ):
      # Tauschvorschläge für diese Planversion
      pass
  
  @router.put("/plan-versions/{version_id}/sync")
  async def sync_plan_version(
      version_id: UUID,
      sync_data: PlanVersionSync,
      current_user: User = Depends(get_current_dispatcher)
  ):
      # Synchronisiere Änderungen von Desktop-App
      pass
  ```
- [ ] `api/models/integration.py` mit Schemas
- [ ] API-Key Authentication für Desktop-App (zusätzlich zu JWT)

#### Deliverables
- ✅ Desktop-Integration API funktioniert
- ✅ Plan-Upload möglich
- ✅ Tauschvorschläge abrufbar

### 9.2 Desktop-App API Client (Woche 20)

**Hinweis:** Dies wird im Desktop-Projekt implementiert, nicht hier. Nur zur Dokumentation.

#### Geplante Integration in Desktop-App:
```python
# In hcc_plan_db_playground
# gui/services/api_client.py

class HCCPlanAPIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
    
    def upload_plan(self, plan: Plan) -> PlanVersion:
        response = requests.post(
            f'{self.base_url}/api/v1/integration/plan-versions',
            headers={'X-API-Key': self.api_key},
            json=plan.to_dict()
        )
        return PlanVersion(**response.json())
    
    def get_proposals(self, version_id: UUID) -> list[ExchangeProposal]:
        response = requests.get(
            f'{self.base_url}/api/v1/integration/plan-versions/{version_id}/proposals',
            headers={'X-API-Key': self.api_key}
        )
        return [ExchangeProposal(**p) for p in response.json()]
```

#### Deliverables
- ✅ API Client in Desktop-App
- ✅ Plan-Upload funktioniert
- ✅ Tauschvorschläge werden abgerufen

### Phase 9 Success Criteria
- [ ] Desktop-App kann Plan hochladen
- [ ] Web-App empfängt Plan korrekt
- [ ] Tauschvorschläge werden synchronisiert
- [ ] Bidirektionale Kommunikation funktioniert

---

## Phase 10: Polish & Optimization (Wochen 21-22)

### Ziel
Finalisierung, Testing, Performance-Optimierung, Dokumentation.

### 10.1 Performance Optimization (Woche 21)

#### Aufgaben
- [ ] Database Query Optimization:
  - Prefetch in kritischen Queries
  - Indexes hinzufügen
  - N+1 Probleme eliminieren
- [ ] Caching implementieren:
  - Template Caching
  - Query Result Caching (für häufige Queries)
- [ ] Frontend Optimization:
  - Image Optimization
  - CSS/JS Minification
  - Lazy Loading
- [ ] Load Testing mit Locust/pytest-benchmark
- [ ] Performance Monitoring Setup

#### Deliverables
- ✅ App läuft schnell (< 200ms Response Time)
- ✅ Database Queries optimiert
- ✅ Caching funktioniert

### 10.2 Testing & Documentation (Woche 22)

#### Aufgaben
- [ ] Unit Tests für alle Services (80%+ Coverage)
- [ ] Integration Tests für API Endpoints
- [ ] E2E Tests für kritische User Flows:
  - Employee: Verfügbarkeit eingeben
  - Employee: Tauschvorschlag erstellen
  - CvO: Tauschvorschlag genehmigen
  - Desktop: Plan hochladen
- [ ] API Documentation (OpenAPI/Swagger) vervollständigen
- [ ] README.md vervollständigen
- [ ] Deployment Guide erstellen (`docs/DEPLOYMENT.md`)
- [ ] Architecture Documentation (`docs/ARCHITECTURE.md`)
- [ ] User Guide erstellen

#### Deliverables
- ✅ Test Coverage > 80%
- ✅ Alle kritischen Flows getestet
- ✅ Dokumentation vollständig
- ✅ Deployment Guide vorhanden

### Phase 10 Success Criteria
- [ ] Alle Tests grün
- [ ] Performance zufriedenstellend
- [ ] Dokumentation vollständig
- [ ] Bereit für Production Deployment

---

## **FULL FEATURE SET ERREICHT nach Phase 10 (Woche 22)** 🎉

### Vollständige Features:
- ✅ Alle MVP Features
- ✅ WebSocket Real-Time Updates
- ✅ Desktop-App Integration
- ✅ CvO Dashboard mit vollem Feature-Set
- ✅ Performance optimiert
- ✅ Umfassend getestet
- ✅ Vollständig dokumentiert

---

## Optionale Erweiterungen (Post-Launch)

### Zukünftige Features (nicht in initialem Scope)

#### Kommentarsystem
- Diskussionen zu Plänen und Appointments
- Threading von Kommentaren
- @-Mentions

#### Erweiterte Statistiken
- Dashboard mit Auslastungsstatistiken
- Heatmaps für beliebte Zeiträume
- Export von Reports (PDF, Excel)

#### Künstlerische Präferenzen
- Management von Besetzungswünschen
- Integration in Planungsprozess
- Präferenz-Scoring

#### Mobile App (Native)
- iOS/Android App mit React Native
- Push-Notifications
- Offline-Modus

#### Automatische Tauschvorschläge
- AI-basierte Vorschläge für optimale Tausche
- Matching-Algorithmus
- Fairness-Scoring

---

## Deployment Strategy

### Development Environment
- SQLite Database
- uvicorn with --reload
- Debug Mode enabled
- Local Testing

### Staging Environment
- PostgreSQL Database
- Docker Containers
- Nginx Reverse Proxy
- SSL/TLS Certificates
- Monitoring Setup

### Production Environment
- PostgreSQL with Replication
- Load Balancer
- CDN for Static Files
- Automated Backups
- Full Monitoring (Logs, Metrics, Alerts)
- CI/CD Pipeline

---

## Success Metrics

### Technical Metrics
- [ ] API Response Time < 200ms (95th percentile)
- [ ] Page Load Time < 2 seconds
- [ ] Test Coverage > 80%
- [ ] Zero Critical Security Issues
- [ ] 99.9% Uptime

### User Metrics
- [ ] User Registration Rate
- [ ] Daily Active Users
- [ ] Tauschvorschlag Success Rate
- [ ] User Satisfaction Score
- [ ] Mobile Usage Percentage

### Business Metrics
- [ ] Reduction in Planning Time
- [ ] Increase in Plan Compliance
- [ ] Reduction in Last-Minute Cancellations
- [ ] User Adoption Rate

---

## Risk Management

### Technical Risks
- **Database Migration Issues**: Mitigation durch ausführliche Tests und Rollback-Plan
- **Performance Problems**: Mitigation durch Load Testing und Optimization
- **WebSocket Stability**: Mitigation durch Fallback zu Polling
- **Desktop Integration Failures**: Mitigation durch robuste Error Handling

### Project Risks
- **Scope Creep**: Mitigation durch klare Priorisierung und MVP-Fokus
- **Timeline Delays**: Mitigation durch Puffer-Wochen und flexible Planung
- **Resource Availability**: Mitigation durch gute Dokumentation und Knowledge Sharing

---

## Conclusion

Dieser Implementierungsplan ist ehrgeizig aber realistisch. Mit **12 Wochen für MVP** und weiteren **10 Wochen für Full Feature Set** erreichen wir ein modernes, kollaboratives Planungssystem.

**Key Success Factors:**
- KEEP IT SIMPLE Philosophie befolgen
- Früh und oft testen
- User Feedback einholen
- Iterativ entwickeln
- Dokumentieren während der Entwicklung

**Next Steps:**
1. Projektsetup (Phase 1) starten
2. Meilensteine im Tracking-Tool einpflegen
3. Team-Kickoff Meeting
4. Los geht's! 🚀
