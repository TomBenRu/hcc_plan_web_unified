"""
Script zur Erstellung eines Admin-Benutzers
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uuid import uuid4
from pony.orm import db_session

from database import setup_database
from database.models.entities import User
from api.auth import get_password_hash


@db_session
def create_admin_user(username, email, password, full_name=None):
    """
    Erstellt einen Admin-Benutzer in der Datenbank.
    
    Args:
        username: Der Benutzername.
        email: Die E-Mail-Adresse.
        password: Das Passwort im Klartext.
        full_name: Optionaler vollständiger Name.
        
    Returns:
        Das erstellte User-Objekt.
    """
    # Prüfen, ob der Benutzer bereits existiert
    existing_user = User.get(username=username)
    if existing_user:
        print(f"Benutzer '{username}' existiert bereits.")
        return existing_user
    
    # Neuen Benutzer erstellen
    password_hash = get_password_hash(password)
    user = User(
        id=uuid4(),
        username=username,
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        is_active=True,
        is_admin=True
    )
    
    print(f"Admin-Benutzer '{username}' erfolgreich erstellt.")
    return user


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Erstellt einen Admin-Benutzer")
    parser.add_argument("--username", required=True, help="Benutzername")
    parser.add_argument("--email", required=True, help="E-Mail-Adresse")
    parser.add_argument("--password", required=True, help="Passwort")
    parser.add_argument("--full-name", help="Vollständiger Name (optional)")
    
    args = parser.parse_args()
    
    # Datenbank initialisieren
    setup_database()
    
    # Admin-Benutzer erstellen
    create_admin_user(
        username=args.username,
        email=args.email,
        password=args.password,
        full_name=args.full_name
    )
