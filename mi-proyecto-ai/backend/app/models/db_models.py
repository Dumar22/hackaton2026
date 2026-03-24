"""
Modelos de base de datos con SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ProcessingRequest(Base):
    """Modelo para solicitudes de procesamiento"""
    __tablename__ = "processing_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    file_name = Column(String)
    model_used = Column(String)
    status = Column(String, default="pending")
    result = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    """Modelo para usuarios"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
