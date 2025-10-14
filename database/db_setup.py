"""
Database Setup und Konfiguration mit PonyORM
"""

from pony.orm import Database

from api.utils.config import settings

# Globale Database-Instanz
db = Database()


def init_database() -> None:
    """
    Initialisiert die Datenbank-Verbindung.
    
    Bindet die Database an die konfigurierte URL und erstellt
    die Tabellen falls sie nicht existieren.
    
    Wird beim Startup der Applikation aufgerufen.
    """
    # Parse Database URL
    database_url = settings.database_url
    
    if database_url.startswith("sqlite"):
        # SQLite: Extrahiere Pfad
        db_path = database_url.replace("sqlite:///", "")
        db.bind(provider="sqlite", filename=db_path, create_db=True)
    elif database_url.startswith("postgresql"):
        # PostgreSQL: Parse Connection String
        # Format: postgresql://user:password@host:port/dbname
        db.bind(provider="postgres", dsn=database_url)
    else:
        raise ValueError(f"Unsupported database URL: {database_url}")
    
    # Import aller Entities (wird später erweitert wenn Entities erstellt werden)
    # from database.models.entities import Person, Team, ...
    
    # Generate Mapping (erstellt SQL-Queries aus Entity-Definitionen)
    db.generate_mapping(create_tables=True)
    
    print(f"✅ Database initialisiert: {database_url}")


def close_database() -> None:
    """
    Schließt die Datenbank-Verbindung.
    
    Wird beim Shutdown der Applikation aufgerufen.
    """
    if db.provider:
        db.disconnect()
        print("✅ Database Verbindung geschlossen")
