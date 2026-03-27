"""
Core configuration using pydantic-settings.
All settings are read from the .env file in the project root.
"""
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Hack-2026/


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./hackaton.db"

    # AI API Keys
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    KIMI_API_KEY: str = ""

    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Data paths
    DATA_DIR: Path = BASE_DIR / "app" / "data"

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"


settings = Settings()
