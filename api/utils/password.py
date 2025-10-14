"""
Password Hashing Utilities mit bcrypt

Verwendet bcrypt für sicheres Password Hashing.
WICHTIG: bcrypt verwenden, NICHT passlib (wird nicht mehr gewartet)
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hasht ein Passwort mit bcrypt.
    
    Verwendet bcrypt.gensalt() für automatisches Salt-Generation.
    Der Hash enthält Salt und Hashing-Parameter.
    
    Args:
        password: Klartext-Passwort
        
    Returns:
        Gehashtes Passwort als bytes
        
    Example:
        >>> hashed = hash_password("my_secure_password")
        >>> type(hashed)
        <class 'bytes'>
    """
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    """
    Verifiziert ein Passwort gegen einen bcrypt Hash.
    
    Args:
        password: Klartext-Passwort zum Verifizieren
        hashed: Gehashtes Passwort (bytes) aus der Datenbank
        
    Returns:
        True wenn Passwort korrekt, False sonst
        
    Example:
        >>> hashed = hash_password("my_password")
        >>> verify_password("my_password", hashed)
        True
        >>> verify_password("wrong_password", hashed)
        False
    """
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed)


def hash_password_to_string(password: str) -> str:
    """
    Hasht ein Passwort und gibt es als String zurück.
    
    Nützlich wenn der Hash als String in der Datenbank gespeichert werden soll.
    
    Args:
        password: Klartext-Passwort
        
    Returns:
        Gehashtes Passwort als UTF-8 String
        
    Example:
        >>> hashed_str = hash_password_to_string("my_password")
        >>> type(hashed_str)
        <class 'str'>
    """
    hashed_bytes = hash_password(password)
    return hashed_bytes.decode('utf-8')


def verify_password_from_string(password: str, hashed_str: str) -> bool:
    """
    Verifiziert ein Passwort gegen einen String-Hash.
    
    Args:
        password: Klartext-Passwort zum Verifizieren
        hashed_str: Gehashtes Passwort als String aus der Datenbank
        
    Returns:
        True wenn Passwort korrekt, False sonst
        
    Example:
        >>> hashed_str = hash_password_to_string("my_password")
        >>> verify_password_from_string("my_password", hashed_str)
        True
    """
    hashed_bytes = hashed_str.encode('utf-8')
    return verify_password(password, hashed_bytes)
