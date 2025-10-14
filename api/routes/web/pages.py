"""
Basic Web Routes: Health Check, Landing Page, etc.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.utils.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=settings.templates_dir)


@router.get("/health", tags=["System"])
async def health_check():
    """
    Health Check Endpoint für Monitoring.
    
    Returns:
        Status-Informationen über das System
    """
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment
    }


@router.get("/", response_class=HTMLResponse, tags=["Web"])
async def landing_page(request: Request):
    """
    Landing Page der Applikation.
    
    TODO: Template erstellen und erweitern wenn Templates vorhanden sind.
    
    Args:
        request: FastAPI Request Objekt
        
    Returns:
        HTML Response mit Landing Page
    """
    # Einfache HTML-Antwort bis Templates erstellt sind
    return """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HCC Plan Web Unified</title>
        <style>
            body {
                font-family: system-ui, -apple-system, sans-serif;
                background: #121212;
                color: #e0e0e0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
            }
            h1 {
                color: #40d4d4;
                font-size: 3rem;
                margin-bottom: 1rem;
            }
            p {
                font-size: 1.2rem;
                color: #a0a0a0;
            }
            .status {
                margin-top: 2rem;
                padding: 1rem;
                background: #1a1a1a;
                border-radius: 8px;
            }
            .badge {
                display: inline-block;
                padding: 0.5rem 1rem;
                background: #008080;
                color: white;
                border-radius: 4px;
                margin: 0.5rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 HCC Plan Web Unified</h1>
            <p>Kollaborative Einsatzplanungs-Webapplikation</p>
            <div class="status">
                <div class="badge">✅ Server läuft</div>
                <div class="badge">📊 Phase 1: Setup</div>
                <div class="badge">🚀 v0.1.0</div>
            </div>
        </div>
    </body>
    </html>
    """
