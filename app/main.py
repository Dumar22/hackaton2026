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
            db.add(db_action)

        # GUARDAR LOS DATOS LIMPIOS (CLEANED DATA) EN TABLAS USANDO BULK
        # Obtenemos los dataframes procesados
        raw_data = pipeline._load_raw()
        clean_data = pipeline._clean(raw_data)
        
        # 1. Usuarios
        users_to_save = [
            db_models.CleanedUser(
                execution_id=execution.id,
                usuario_id=int(row["usuario_id"]),
                edad=float(row["edad"]) if pd.notnull(row["edad"]) else None,
                genero=str(row.get("genero", "Desconocido")),
                ciudad=str(row.get("ciudad", "Desconocida")),
                fecha_registro=str(row.get("fecha_registro", row.get("fecha", "")))
            ) for _, row in clean_data["usuarios"].iterrows()
        ]
        db.bulk_save_objects(users_to_save)
            
        # 2. Eventos (Proceso masivo sin límite artificial)
        events_to_save = [
            db_models.CleanedEvent(
                execution_id=execution.id,
                usuario_id=int(row["usuario_id"]),
                fecha_evento=str(row.get("fecha_evento", row.get("fecha", ""))),
                tipo_evento=str(row["tipo_evento"]),
                detalle=str(row.get("detalle", ""))
            ) for _, row in clean_data["eventos"].iterrows()
        ]
        db.bulk_save_objects(events_to_save)

        # 3. Productos
        prods_to_save = [
            db_models.CleanedProduct(
                execution_id=execution.id,
                producto_id=int(row["producto_id"]),
                nombre=str(row["nombre"]),
                categoria=str(row["categoria"])
            ) for _, row in clean_data["productos"].iterrows()
        ]
        db.bulk_save_objects(prods_to_save)

        # 4. Interacciones
        ints_to_save = [
            db_models.CleanedInteraction(
                execution_id=execution.id,
                usuario_id=int(row["usuario_id"]),
                producto_id=int(row["producto_id"]),
                fecha=str(row["fecha"]),
                accion=str(row["accion"])
            ) for _, row in clean_data["interacciones"].iterrows()
        ]
        db.bulk_save_objects(ints_to_save)
            
        db.commit()

    return {
        "success": result.success,
        "execution_id": execution.id if result.success else None,
        "duration_ms": result.duration_ms,
        "error": result.error,
        "stages": result.stages,
    }

@app.post("/pipeline/chat", tags=["AI Chat"])
def chat_with_data(request: ChatRequest):
    """
    Ask Gemini questions about the data and the pipeline findings.
    Requires a valid GEMINI_API_KEY in .env.
    """
    bot = AIChatBot()
    response = bot.chat(request.message, request.pipeline_context)
    return {"response": response}

@app.get("/pipeline/history", tags=["Pipeline"])
def get_pipeline_history(db: Session = Depends(get_db), limit: int = 10):
    """Returns a list of past pipeline executions and insights."""
    executions = db.query(db_models.PipelineExecution).order_by(db_models.PipelineExecution.timestamp.desc()).limit(limit).all()
    return executions

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
