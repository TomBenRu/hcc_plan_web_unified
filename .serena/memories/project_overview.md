# HCC Plan Web Unified - Projektübersicht

## Projektzweck
Das `hcc_plan_web_unified` Projekt ist eine **moderne, kollaborative Einsatzplanungs-Webapplikation** für Teams von Klinikclowns und ähnliche Organisationen. Es vereint die besten Features aus drei bestehenden Projekten:

- **Design & UX**: Von `appointment_plan_api_cl` (modernes Dark Theme mit Tailwind CSS)
- **Features**: Von `hcc_plan_api` (Verfügbarkeitserfassung, APScheduler, E-Mail-System)
- **Kollaboration**: Neue Features für teambasierte Planungsworkflows

## Hauptfunktionen

### Für Actors (Mitarbeiter)
- **Einsatzplan-Kalenderansicht**: Übersicht aller eigenen Einsätze
- **Verfügbarkeitserfassung**: Eingabe von Verfügbarkeiten für Planperioden
- **Tauschbörse**: Vorschlagen und Verwalten von Einsatztausch mit Kollegen
- **Mobile-First**: Responsive Design für unterwegs
- **Push-Benachrichtigungen**: Real-Time Updates über Änderungen

### Für CvOs (Chief-Verantwortliche)
- **CvO-Dashboard**: Übersicht über Tauschvorschläge und Team-Status
- **Verfügbarkeitsmatrix**: Wer ist wann verfügbar?
- **Tauschvorschläge genehmigen**: Approve/Reject von Einsatztauschen
- **Engpass-Erkennung**: Automatische Warnung bei kritischen Tagen
- **Team-Koordination**: Kommunikation mit Teammitgliedern

### Für Dispatcher/Planer
- **Plan-Upload**: Integration mit Desktop-App (hcc_plan_db_playground)
- **Planversions-Management**: Entwurf → Review → Final
- **Künstlerische Präferenzen**: Hinterlegung von Besetzungswünschen
- **Reporting**: Statistiken und Auswertungen

## Projekthintergrund

### Evolution aus bestehenden Systemen
1. **hcc_plan_db_playground** (Desktop-App)
   - Windows-only PySide6 Desktop-App
   - OR-Tools SAT-Solver für automatische Planoptimierung
   - Komplexe Planungsfunktionen
   - Problem: Nicht plattformübergreifend, keine mobile Nutzung

2. **hcc_plan_api** (Web-App v1)
   - Verfügbarkeitserfassung funktioniert gut
   - Rollenbasierte Auth
   - APScheduler für Automatisierung
   - Problem: Veraltetes Design, keine Einsatzplan-Ansicht für Actors

3. **appointment_plan_api_cl** (Web-App v2 - Studie)
   - Modernes Design mit Tailwind CSS
   - Excellente Kalenderansicht
   - HTMX für schnelle Interaktionen
   - Problem: Nur Planansicht, keine Verfügbarkeitserfassung, keine Kollaboration

### Ziel: Unified System
**hcc_plan_web_unified** kombiniert die Stärken aller drei Systeme:
- ✅ Modernes Design (appointment_plan_api_cl)
- ✅ Vollständige Features (hcc_plan_api + NEU)
- ✅ Desktop-Integration (hcc_plan_db_playground via API)
- ✅ Kollaborative Workflows (NEU)
- ✅ Mobile-First (NEU)

## Use Case: Kollaborativer Planungsprozess

### Szenario
Ein Theater-Team plant die Einsätze für 6 Monate im Voraus:

1. **Verfügbarkeitserfassung (Woche 1-2)**
   - Actors geben ihre Verfügbarkeiten in der Web-App ein
   - Deadline wird per E-Mail erinnert (APScheduler)

2. **Erstentwurf (Woche 3)**
   - Planer erstellt Erstentwurf in Desktop-App (OR-Tools Optimierung)
   - Plan wird via API an Web-App hochgeladen
   - Status: "Entwurf"

3. **Review-Phase (Woche 4)**
   - Actors sehen ihre Einsätze im Kalender (Web-App)
   - CvOs prüfen Besetzung ihrer Einrichtungen
   - Actors können Tauschvorschläge erstellen
   - CvOs genehmigen/lehnen Tauschvorschläge ab
   - Künstlerische Leitung gibt Präferenzen an

4. **Optimierung (Woche 5)**
   - Planer sieht genehmigte Tauschvorschläge in Desktop-App
   - Desktop-App synchronisiert Änderungen
   - Finale Optimierung mit allen Constraints

5. **Finalisierung (Woche 6)**
   - Plan wird als "Final" markiert
   - Alle erhalten E-Mail-Benachrichtigung
   - Plan ist verbindlich
   - Actors sehen finalen Einsatzplan in Web-App

## Zielgruppe
- **Actors/Klinikclowns**: Freiberufliche Mitarbeiter, oft unterwegs, benötigen mobile Zugriff
- **CvOs (Chief-Verantwortliche)**: Teamleiter für bestimmte Einrichtungen
- **Dispatcher**: Koordinieren Teams und Planungsprozesse
- **Planer**: Erstellen komplexe Pläne mit OR-Tools
- **Künstlerische Leitung**: Geben Präferenzen für Besetzungen an
- **Administratoren**: Projektverwaltung und Systemkonfiguration

## Technologische Vision
- **API-First**: Alle Features über REST API zugänglich
- **Real-Time**: WebSocket für sofortige Updates
- **Mobile-First**: Responsive Design mit Touch-Optimierung
- **Progressive Enhancement**: Funktioniert auch ohne JavaScript (HTMX)
- **Type-Safe**: Pydantic Schemas für alle API-Contracts
- **Testable**: Umfangreiche Test-Coverage
- **Dokumentiert**: OpenAPI/Swagger Docs für alle Endpoints
