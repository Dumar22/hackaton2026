"""
SQLAlchemy models for persisting pipeline results.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base

class ChatMessageModel(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)  # 'user' or 'bot'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class PipelineExecution(Base):
    __tablename__ = "pipeline_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    duration_ms = Column(Float)
    status = Column(String)  # success / failed
    error_message = Column(String, nullable=True)

class InsightModel(Base):
    __tablename__ = "persistent_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("pipeline_executions.id"))
    category = Column(String)
    severity = Column(String)
    title = Column(String)
    description = Column(String)
    affected_users = Column(JSON)
    metric = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ActionLogModel(Base):
    __tablename__ = "persistent_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("pipeline_executions.id"))
    action_type = Column(String)
    priority = Column(Integer)
    status = Column(String)
    summary = Column(String)
    details = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

# Tablas para el almacenamiento de los DATOS LIMPIOS (Cleaned Data)
# Esto nos permite auditar qué exactamente cambió tras la limpieza.

class CleanedUser(Base):
    __tablename__ = "cleaned_users"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, unique=True, index=True)
    edad = Column(Float)
    genero = Column(String)
    ciudad = Column(String)
    fecha_registro = Column(String)
    execution_id = Column(Integer, ForeignKey("pipeline_executions.id"))

class CleanedEvent(Base):
    __tablename__ = "cleaned_events"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, index=True)
    fecha_evento = Column(String)
    tipo_evento = Column(String)
    detalle = Column(Text)
    execution_id = Column(Integer, ForeignKey("pipeline_executions.id"))

class CleanedProduct(Base):
    __tablename__ = "cleaned_products"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, unique=True, index=True)
    nombre = Column(String)
    categoria = Column(String)
    execution_id = Column(Integer, ForeignKey("pipeline_executions.id"))

class CleanedInteraction(Base):
    __tablename__ = "cleaned_interactions"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, index=True)
    producto_id = Column(Integer, index=True)
    fecha = Column(String)
    accion = Column(String)
    execution_id = Column(Integer, ForeignKey("pipeline_executions.id"))
