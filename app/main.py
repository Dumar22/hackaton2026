"""
main.py – FastAPI server entry point.

Run with:
    uvicorn app.main:app --reload

Or directly:
    python -m app.main
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import uvicorn

from app.core.config import settings
from app.cleaners import CSVCleaner, ExcelCleaner
from app.analysis.exploratory import ExploratoryAnalysis
from app.analysis.adaptive import load_and_process
from app.pipeline import DataPipeline
from app.core.database import engine, SessionLocal, get_db
from app.engine import db_models
from app.engine.bot import AIChatBot
from sqlalchemy.orm import Session
from fastapi import Depends
from pydantic import BaseModel as PydanticBaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Initialize database tables
db_models.Base.metadata.create_all(bind=engine)

# Request schemas
class ChatRequest(PydanticBaseModel):
    message: str
    pipeline_context: dict = {} # Default to empty dict if not provided

# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Hackathon 2026 – Data Intelligence API",
    description=(
        "API for data cleaning, exploratory analysis and AI-driven insights. "
        "Built with FastAPI for the Hackathon Talentotest 2026."
    ),
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# CORS – allow local front-end during development
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Static Files & Frontend
# ---------------------------------------------------------------------------
# Mount the static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", tags=["UI"])
def serve_index():
    """Serves the main dashboard HTML."""
    return FileResponse("app/static/index.html")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}


# ---------------------------------------------------------------------------
# Data endpoints
# ---------------------------------------------------------------------------
@app.get("/data/summary", tags=["Data"])
def data_summary():
    """
    Returns a summary of the built-in sample datasets
    (usuarios, eventos, productos, interacciones).
    """
    data_dir = settings.DATA_DIR
    files = ["usuarios.csv", "eventos.csv", "productos.csv", "interacciones.csv"]
    summary = {}
    for fname in files:
        path = data_dir / fname
        if path.exists():
            df = pd.read_csv(path)
            summary[fname] = {
                "rows": df.shape[0],
                "columns": df.shape[1],
                "column_names": list(df.columns),
                "missing_values": int(df.isnull().sum().sum()),
            }
        else:
            summary[fname] = {"error": "File not found"}
    return summary


# ---------------------------------------------------------------------------
# Cleaning endpoints
# ---------------------------------------------------------------------------
@app.post("/clean/csv", tags=["Cleaning"])
async def clean_csv_upload(file: UploadFile = File(...)):
    """
    Uploads a CSV file, applies the full cleaning pipeline and
    returns the cleaned data as JSON.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported on this endpoint.")

    contents = await file.read()
    raw_df = pd.read_csv(io.BytesIO(contents))

    cleaner = CSVCleaner()

    # Run cleaning steps manually (no file I/O needed here)
    df = cleaner.handle_missing_data(raw_df)
    df = cleaner.remove_duplicates(df)
    df = cleaner.remove_outliers(df)
    df = cleaner.correct_typos(df)
    df = cleaner.check_logical_integrity(df)
    df = cleaner.normalize_text(df)

    return {
        "original_rows": raw_df.shape[0],
        "cleaned_rows": df.shape[0],
        "columns": list(df.columns),
        "data": df.head(50).to_dict(orient="records"),
    }


@app.post("/clean/excel", tags=["Cleaning"])
async def clean_excel_upload(file: UploadFile = File(...)):
    """
    Uploads an Excel file (.xlsx/.xls), applies the cleaning pipeline and
    returns the cleaned data as JSON.
    """
    if not (file.filename.endswith(".xlsx") or file.filename.endswith(".xls")):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx/.xls) are supported.")

    contents = await file.read()
    raw_df = pd.read_excel(io.BytesIO(contents))

    cleaner = ExcelCleaner()

    df = cleaner.handle_missing_data(raw_df)
    df = cleaner.remove_duplicates(df)
    df = cleaner.remove_outliers(df)
    df = cleaner.correct_typos(df)
    df = cleaner.check_logical_integrity(df)
    df = cleaner.normalize_text(df)

    return {
        "original_rows": raw_df.shape[0],
        "cleaned_rows": df.shape[0],
        "columns": list(df.columns),
        "data": df.head(50).to_dict(orient="records"),
    }


# ---------------------------------------------------------------------------
# Analysis endpoints
# ---------------------------------------------------------------------------
@app.post("/analysis/explore", tags=["Analysis"])
async def explore_upload(file: UploadFile = File(...)):
    """
    Uploads a CSV or Excel file and returns an exploratory analysis report:
    statistical summary, missing values report and correlation matrix.
    """
    contents = await file.read()
    ext = file.filename.rsplit(".", 1)[-1].lower()

    if ext == "csv":
        df = pd.read_csv(io.BytesIO(contents))
    elif ext in ("xlsx", "xls"):
        df = pd.read_excel(io.BytesIO(contents))
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Use CSV or Excel.")

    analyst = ExploratoryAnalysis(df)

    return {
        "shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "columns": list(df.columns),
        "statistical_summary": analyst.statistical_summary().to_dict(),
        "missing_report": analyst.missing_report().to_dict(),
        "correlations": analyst.correlations().to_dict(),
    }


# ---------------------------------------------------------------------------
# Pipeline endpoint – full A→G flow
# ---------------------------------------------------------------------------
@app.post("/pipeline/run", tags=["Pipeline"])
def run_pipeline(db: Session = Depends(get_db)):
    """
    Executes the complete data intelligence pipeline on the built-in sample datasets:

    A. Raw Data  →  B. Cleaning & Validation  →  C. Exploratory Analysis
    →  D. AI Model  →  E. Insight Generation  →  F. Decision Making
    →  G. Business Action
    """
    pipeline = DataPipeline(data_dir=settings.DATA_DIR)
    result = pipeline.run()
    
    if result.success:
        # Save execution summary
        execution = db_models.PipelineExecution(
            duration_ms=result.duration_ms,
            status="success"
        )
        db.add(execution)
        db.commit()
        db.refresh(execution)
        
        # Save insights
        insights = result.stages.get("E_insights", {}).get("insights", [])
        for i in insights:
            # Aseguramos que metric sea un float nativo de Python (no np.float64)
            metric_val = i.get("metric")
            if hasattr(metric_val, "item"): # Si es un tipo de numpy
                metric_val = metric_val.item()
            elif metric_val is not None:
                metric_val = float(metric_val)

            db_insight = db_models.InsightModel(
                execution_id=execution.id,
                category=i.get("category"),
                severity=i.get("severity"),
                title=i.get("title"),
                description=i.get("description"),
                affected_users=i.get("affected_users"),
                metric=metric_val
            )
            db.add(db_insight)
            
        # Save actions
        actions = result.stages.get("G_actions", {}).get("actions", [])
        for a in actions:
            db_action = db_models.ActionLogModel(
                execution_id=execution.id,
                action_type=a.get("action_type"),
                priority=a.get("priority"),
                status=a.get("status"),
                summary=a.get("summary"),
                details=a.get("details", {})
            )
                 # ── GUARDAR DATOS LIMPIOS CON MOTOR UPSERT DE ALTA VELOCIDAD ──
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        clean_data = result.stages.get("_raw_clean_dfs", {})

        # A. Usuarios (Upsert por usuario_id)
        users_df = clean_data.get("usuarios", pd.DataFrame())
        if not users_df.empty:
            data = users_df.assign(execution_id=execution.id).to_dict(orient="records")
            for chunk in [data[i:i + 1000] for i in range(0, len(data), 1000)]:
                stmt = pg_insert(db_models.CleanedUser).values(chunk)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["usuario_id"],
                    set_={c.name: c for c in stmt.excluded if c.name not in ["id", "usuario_id"]}
                )
                db.execute(stmt)

        # B. Productos (Upsert por producto_id)
        prods_df = clean_data.get("productos", pd.DataFrame())
        if not prods_df.empty:
            data = prods_df.assign(execution_id=execution.id).to_dict(orient="records")
            for chunk in [data[i:i + 1000] for i in range(0, len(data), 1000)]:
                stmt = pg_insert(db_models.CleanedProduct).values(chunk)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["producto_id"],
                    set_={c.name: c for c in stmt.excluded if c.name not in ["id", "producto_id"]}
                )
                db.execute(stmt)

        # C. Eventos e Interacciones (Append optimizado)
        # Para tablas masivas de series temporales, usamos bulk_insert_mappings
        for key, model in [("eventos", db_models.CleanedEvent), ("interacciones", db_models.CleanedInteraction)]:
            df_to_save = clean_data.get(key, pd.DataFrame())
            if not df_to_save.empty:
                data = df_to_save.assign(execution_id=execution.id).to_dict(orient="records")
                for chunk in [data[i:i + 1000] for i in range(0, len(data), 1000)]:
                    db.bulk_insert_mappings(model, chunk)
        
        db.commit()
  
        db.commit()

    return {
        "success": result.success,
        "execution_id": execution.id if result.success else None,
        "duration_ms": result.duration_ms,
        "error": result.error,
        "stages": result.stages,
    }

@app.post("/pipeline/chat", tags=["AI Chat"])
def chat_with_data(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Ask AI questions about the data and the pipeline findings.
    """
    # 1. Save User Message
    user_msg = db_models.ChatMessageModel(role="user", content=request.message)
    db.add(user_msg)
    
    bot = AIChatBot()
    response = bot.chat(request.message, request.pipeline_context)
    
    # 2. Save Bot Response
    bot_msg = db_models.ChatMessageModel(role="bot", content=response)
    db.add(bot_msg)
    db.commit()
    
    return {"response": response}

@app.get("/chat/history", tags=["AI Chat"])
def get_chat_history(db: Session = Depends(get_db)):
    """Returns the stored conversation history."""
    messages = db.query(db_models.ChatMessageModel).order_by(db_models.ChatMessageModel.timestamp.asc()).all()
    # Map to the format React expects { role, text }
    return [{"role": m.role, "text": m.content} for m in messages]

@app.get("/pipeline/latest_results", tags=["Pipeline"])
def get_latest_pipeline_results(db: Session = Depends(get_db)):
    """Recupera la última ejecución con todos sus detalles para cargar el Dashboard al inicio."""
    execution = db.query(db_models.PipelineExecution).order_by(db_models.PipelineExecution.timestamp.desc()).first()
    if not execution:
        return {"success": False, "message": "No hay ejecuciones previas."}
    
    insights = db.query(db_models.InsightModel).filter_by(execution_id=execution.id).all()
    actions = db.query(db_models.ActionLogModel).filter_by(execution_id=execution.id).all()
    
    # Intentamos obtener un resumen de riesgo/usuarios para el dashboard
    user_count = db.query(db_models.CleanedUser).count()
    
    return {
        "success": True,
        "stages": {
            "D_model": {"users_analysed": user_count},
            "E_insights": {"insights": [{"title": i.title, "description": i.description, "metric": i.metric, "severity": i.severity, "category": i.category} for i in insights]},
            "G_actions": {"actions": [{"action_type": a.action_type, "summary": a.summary} for a in actions]}
        }
    }

@app.get("/pipeline/insights/all", tags=["Pipeline"])
def get_all_insights(db: Session = Depends(get_db)):
    """Returns all insights stored in the database."""
    return db.query(db_models.InsightModel).order_by(db_models.InsightModel.timestamp.desc()).all()


# ---------------------------------------------------------------------------
# User specific endpoints
# ---------------------------------------------------------------------------
@app.get("/user/{user_id}/stats", tags=["User"])
def get_user_stats(user_id: int):
    """
    Returns statistics and recommendations for a single user.
    """
    data_dir = settings.DATA_DIR
    ints_path = data_dir / "interacciones.csv"
    if not ints_path.exists():
        return {"error": "Interactions data not found"}
        
    df_ints = pd.read_csv(ints_path)
    user_data = df_ints[df_ints["usuario_id"] == user_id]
    
    if user_data.empty:
        return {"message": "No data found for this user", "user_id": user_id}
        
    stats = {
        "user_id": user_id,
        "total_interactions": len(user_data),
        "completions": len(user_data[user_data["accion"] == "completado"]),
        "abandonments": len(user_data[user_data["accion"] == "abandonado"]),
        "completion_rate": (len(user_data[user_data["accion"] == "completado"]) / len(user_data)) * 100 if len(user_data) > 0 else 0
    }
    
    return stats


@app.get("/pipeline/status", tags=["Pipeline"])
def pipeline_status():
    """Returns the list of pipeline stages and their descriptions."""
    return {
        "stages": [
            {"id": "A", "name": "Raw Data",             "module": "app.data"},
            {"id": "B", "name": "Cleaning & Validation", "module": "app.cleaners"},
            {"id": "C", "name": "Exploratory Analysis",  "module": "app.analysis.exploratory"},
            {"id": "D", "name": "AI / Algorithm",        "module": "app.engine.models"},
            {"id": "E", "name": "Insight Generation",    "module": "app.engine.insights"},
            {"id": "F", "name": "Decision Making",       "module": "app.engine.decisions"},
            {"id": "G", "name": "Business Action",       "module": "app.engine.actions"},
        ]
    }


# ---------------------------------------------------------------------------
# Entry point (for running directly with `python -m app.main`)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
