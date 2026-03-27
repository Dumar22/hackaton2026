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
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "Hackathon 2026 API", "version": "0.1.0"}


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
def run_pipeline():
    """
    Executes the complete data intelligence pipeline on the built-in sample datasets:

    A. Raw Data  →  B. Cleaning & Validation  →  C. Exploratory Analysis
    →  D. AI Model  →  E. Insight Generation  →  F. Decision Making
    →  G. Business Action
    """
    pipeline = DataPipeline(data_dir=settings.DATA_DIR)
    result = pipeline.run()
    return {
        "success": result.success,
        "duration_ms": result.duration_ms,
        "error": result.error,
        "stages": result.stages,
    }


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
