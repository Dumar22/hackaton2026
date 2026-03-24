"""
Dependencias globales para inyección en rutas
"""
from sqlalchemy.orm import Session
from app.db.session import get_db

def get_database() -> Session:
    """Obtiene la sesión de base de datos"""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()
