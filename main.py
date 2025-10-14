"""
HCC Plan Web Unified - Haupteinstiegspunkt

FastAPI Applikation mit:
- Lifespan Events (Startup/Shutdown)
- Static Files Mounting
- CORS Middleware
- Exception Handlers
- Route Includes
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.middleware.error_handler import global_exception_handler
from api.routes.web.pages import router as web_pages_router
from api.utils.config import settings
from database.db_setup import close_database, init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan Context Manager für Startup und Shutdown Events.
    
    Startup:
    - Initialisiere Datenbank
    - Erstelle notwendige Verzeichnisse
    - Lade Konfiguration
    
    Shutdown:
    - Schließe Datenbank-Verbindung
    - Cleanup
    """
    # Startup
    print("🚀 Starte HCC Plan Web Unified...")
    
    # Erstelle notwendige Verzeichnisse
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path(settings.static_files_dir).mkdir(exist_ok=True)
    Path(settings.templates_dir).mkdir(exist_ok=True)
    
    # Initialisiere Datenbank
    init_database()
    
    print(f"✅ {settings.app_name} v{settings.app_version} gestartet!")
    print(f"🌍 Environment: {settings.environment}")
    print(f"🐛 Debug Mode: {settings.debug}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down HCC Plan Web Unified...")
    close_database()
    print("✅ Shutdown abgeschlossen")


# FastAPI App Initialisierung
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Kollaborative Einsatzplanungs-Webapplikation für Theater-Teams",
    debug=settings.debug,
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
app.add_exception_handler(Exception, global_exception_handler)

# Static Files
app.mount(
    "/static",
    StaticFiles(directory=settings.static_files_dir),
    name="static"
)

# Include Routers
app.include_router(web_pages_router, tags=["Web"])
# Weitere Router werden später hinzugefügt:
# app.include_router(api_router, prefix="/api/v1", tags=["API"])
# app.include_router(employee_router, prefix="/employee", tags=["Employee"])
# app.include_router(cvo_router, prefix="/cvo", tags=["CvO"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )