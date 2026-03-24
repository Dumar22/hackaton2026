"""
Configuración global de la aplicación
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API
    API_TITLE: str = "AI Project API"
    DEBUG: bool = False
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3002",
        "http://localhost:5173",
        "http://localhost:8000",
        "https://vercel-deploy-url.com",
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/ai_project_db"
    
    # API Keys
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    KIMI_API_KEY: str = ""
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
