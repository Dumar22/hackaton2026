"""
Database Reset Script – Truncates all tables for a clean start.
"""
from sqlalchemy import text
from app.core.database import SessionLocal, engine
from app.engine import db_models

def reset_database():
    print("🧹 Iniciando la limpieza de la base de datos...")
    
    db = SessionLocal()
    try:
        # En PostgreSQL, es mejor usar TRUNCATE con CASCADE para limpiar todo de golpe
        # Si es SQLite, usamos DELETE FROM (aunque SQLAlchemy maneja ambos bien)
        tables = [
            "cleaned_interactions", "cleaned_events", "cleaned_products", "cleaned_users",
            "persistent_actions", "persistent_insights", "pipeline_executions"
        ]
        
        for table in tables:
            print(f"   ↳ Vaciando tabla: {table}")
            db.execute(text(f"DELETE FROM {table}"))
            
        db.commit()
        print("✅ Base de datos reseteada con éxito.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al resetear la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_database()
