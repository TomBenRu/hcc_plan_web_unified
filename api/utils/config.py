"""
Konfiguration und Settings für HCC Plan Web Unified
Verwendet Pydantic Settings für Environment Variables
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Applikations-Settings aus Environment Variables.
    
    Lädt automatisch aus .env Datei.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application Settings
    app_name: str = "HCC Plan Web Unified"
    app_version: str = "0.1.0"
    debug: bool = True
    environment: str = "development"
    
    # Database Configuration
    database_url: str = "sqlite:///data/hcc_plan.sqlite"
    
    # Security & Authentication
    secret_key: str
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"
    
    # SMTP / E-Mail Configuration
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    smtp_from_email: str = "noreply@hccplan.de"
    smtp_from_name: str = "HCC Plan System"
    
    # CORS Settings
    cors_origins: str = "http://localhost:3000,http://localhost:8000"
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Konvertiert CORS Origins String zu Liste"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # APScheduler Settings
    scheduler_enabled: bool = True
    reminder_schedule_hour: int = 8
    reminder_schedule_minute: int = 0
    
    # WebSocket Settings
    websocket_enabled: bool = False
    websocket_port: int = 8001
    
    # Frontend Settings
    static_files_dir: str = "static"
    templates_dir: str = "templates"
    
    # Pagination & Limits
    default_page_size: int = 50
    max_page_size: int = 1000
    
    # File Upload Settings
    max_upload_size_mb: int = 10
    allowed_upload_extensions: str = ".xlsx,.xls,.csv"
    
    @property
    def allowed_extensions_list(self) -> list[str]:
        """Konvertiert Allowed Extensions String zu Liste"""
        return [ext.strip() for ext in self.allowed_upload_extensions.split(",")]
    
    # Desktop App Integration Settings
    desktop_api_enabled: bool = False
    desktop_api_key: Optional[str] = None


@lru_cache
def get_settings() -> Settings:
    """
    Singleton Pattern für Settings.
    
    Cached die Settings-Instanz, sodass .env nur einmal gelesen wird.
    
    Returns:
        Settings Instanz
    """
    return Settings()


# Convenience Export
settings = get_settings()
