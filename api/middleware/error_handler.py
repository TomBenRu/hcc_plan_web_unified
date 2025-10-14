"""
Global Exception Handler für FastAPI
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pony.orm import ObjectNotFound, TransactionIntegrityError


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Globaler Exception Handler für alle unbehandelten Exceptions.
    
    Args:
        request: FastAPI Request Objekt
        exc: Die geworfene Exception
        
    Returns:
        JSONResponse mit Error-Details
    """
    # PonyORM ObjectNotFound -> 404
    if isinstance(exc, ObjectNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": "Objekt nicht gefunden",
                "error_type": "NotFound"
            }
        )
    
    # PonyORM TransactionIntegrityError -> 400
    if isinstance(exc, TransactionIntegrityError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Datenbankfehler: Integritätsverletzung",
                "error_type": "IntegrityError"
            }
        )
    
    # Alle anderen Exceptions -> 500
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Interner Server-Fehler",
            "error_type": type(exc).__name__,
            "message": str(exc) if request.app.debug else None
        }
    )
