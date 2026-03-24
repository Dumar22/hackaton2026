"""
Funciones de seguridad (autenticación y autorización)
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from app.core.config import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT
    
    Args:
        data: Datos a codificar
        expires_delta: Tiempo de expiración
    
    Returns:
        Token JWT
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def decode_token(token: str) -> dict:
    """
    Decodifica un token JWT
    
    Args:
        token: Token a decodificar
    
    Returns:
        Datos del token
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.InvalidTokenError:
        return None
