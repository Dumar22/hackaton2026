"""
Endpoints para procesamiento de datos, análisis de patrones y automatización
"""
from fastapi import APIRouter, File, UploadFile, Query, HTTPException, BackgroundTasks
from typing import List, Dict, Optional
import io
import csv
import json
from app.data_processing import (
    DataGenerator,
    DataExporter,
    PatternAnalyzer,
    ProcessClassifier
)

router = APIRouter(prefix="/data", tags=["data-processing"])

# Cache en memoria para datos generados (en producción usar cache distribuido)
_generated_data_cache = {}

@router.post("/generate")
async def generate_data(
    rows: int = Query(5000, ge=1, le=50000),
    export_formats: List[str] = Query(["csv", "json"])
):
    """
    Genera datos realistas de ejemplo
    
    Args:
        rows: Número de registros a generar (1-50,000)
        export_formats: Formatos a exportar (csv, json, sql, excel, pdf)
    
    Returns:
        Datos generados y estadísticas
    """
    try:
        # Generar datos
        generator = DataGenerator(rows=rows)
        data = generator.get_data()
        headers = generator.get_headers()
        stats = generator.get_stats()
        
        # Crear key para cache
        cache_key = f"data_{rows}"
        _generated_data_cache[cache_key] = {
            "data": data,
            "headers": headers,
            "stats": stats
        }
        
        return {
            "success": True,
            "message": f"Datos generados: {rows} registros",
            "cache_key": cache_key,
            "total_records": rows,
            "columns": len(headers),
            "statistics": stats,
            "sample": data[:5]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/export")
async def export_data(
    cache_key: str = Query(...),
    formats: List[str] = Query(["csv", "json"])
):
    """
    Exporta datos generados a múltiples formatos
    
    Args:
        cache_key: Clave del cache con los datos generados
        formats: Formatos a exportar (csv, json, sql, excel, pdf)
    
    Returns:
        URLs de archivos generados
    """
    if cache_key not in _generated_data_cache:
        raise HTTPException(status_code=404, detail="Datos no encontrados en cache")
    
    try:
        data = _generated_data_cache[cache_key]["data"]
        headers = _generated_data_cache[cache_key]["headers"]
        
        exporter = DataExporter(data, headers)
        results = {}
        
        for fmt in formats:
            if fmt == "csv":
                results["csv"] = _export_csv(data, headers)
            elif fmt == "json":
                results["json"] = _export_json(data)
            elif fmt == "sql":
                results["sql"] = _export_sql(data, headers)
            elif fmt == "excel":
                results["excel"] = "(Se requiere pandas)"
            elif fmt == "pdf":
                results["pdf"] = "(Se requiere reportlab)"
        
        return {
            "success": True,
            "cache_key": cache_key,
            "total_records": len(data),
            "formats_exported": list(results.keys()),
            "exports": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze")
async def analyze_patterns(
    cache_key: str = Query(...),
    model: str = Query("gpt", regex="^(gpt|gemini|kimi)$")
):
    """
    Analiza patrones en los datos usando IA
    
    Args:
        cache_key: Clave del cache con los datos
        model: Modelo a utilizar (gpt, gemini, kimi)
    
    Returns:
        Análisis de patrones y recomendaciones
    """
    if cache_key not in _generated_data_cache:
        raise HTTPException(status_code=404, detail="Datos no encontrados en cache")
    
    try:
        data = _generated_data_cache[cache_key]["data"]
        stats = _generated_data_cache[cache_key]["stats"]
        
        analyzer = PatternAnalyzer(model=model)
        
        # Realizar análisis
        analysis = await analyzer.analyze_patterns(data, stats)
        
        return {
            "success": True,
            "model": model,
            "cache_key": cache_key,
            "total_records": len(data),
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/classify")
async def classify_processes(
    cache_key: str = Query(...)
):
    """
    Clasifica registros por prioridad y automatización
    
    Args:
        cache_key: Clave del cache con los datos
    
    Returns:
        Registros clasificados y métricas
    """
    if cache_key not in _generated_data_cache:
        raise HTTPException(status_code=404, detail="Datos no encontrados en cache")
    
    try:
        data = _generated_data_cache[cache_key]["data"]
        
        classifier = ProcessClassifier()
        classified = classifier.classify_all(data)
        metrics = classifier.get_metrics()
        workflow = classifier.generate_workflow(classified)
        
        return {
            "success": True,
            "cache_key": cache_key,
            "total_records": len(data),
            "classification_summary": {
                "urgentes": len(classified.get("urgentes", [])),
                "alta_prioridad": len(classified.get("alta_prioridad", [])),
                "media_prioridad": len(classified.get("media_prioridad", [])),
                "baja_prioridad": len(classified.get("baja_prioridad", [])),
                "anomalias": len(classified.get("anomalias", [])),
                "automatizable": len(classified.get("automatizable", []))
            },
            "metrics": metrics,
            "workflow": workflow,
            "samples": {
                "urgentes_sample": classified.get("urgentes", [])[:3],
                "automatizable_sample": classified.get("automatizable", [])[:3]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze-file")
async def analyze_uploaded_file(
    file: UploadFile = File(...),
    model: str = Query("gpt", regex="^(gpt|gemini|kimi)$")
):
    """
    Analiza un archivo CSV cargado
    
    Args:
        file: Archivo CSV a analizar
        model: Modelo de IA a usar
    
    Returns:
        Análisis de patrones del archivo
    """
    try:
        contents = await file.read()
        
        # Parsecar CSV
        reader = csv.DictReader(io.StringIO(contents.decode('utf-8')))
        data = list(reader)
        
        if not data:
            raise HTTPException(status_code=400, detail="Archivo vacío")
        
        # Clasificar
        classifier = ProcessClassifier()
        classified = classifier.classify_all(data)
        metrics = classifier.get_metrics()
        
        # Analizar patrones
        analyzer = PatternAnalyzer(model=model)
        analysis = await analyzer.analyze_patterns(data)
        
        return {
            "success": True,
            "filename": file.filename,
            "total_records": len(data),
            "columns": list(data[0].keys()) if data else [],
            "classification": {
                "urgentes": len(classified.get("urgentes", [])),
                "alta_prioridad": len(classified.get("alta_prioridad", [])),
                "automatizable": len(classified.get("automatizable", []))
            },
            "metrics": metrics,
            "pattern_analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
async def get_cache_status():
    """Obtiene estado del cache de datos"""
    return {
        "cached_datasets": len(_generated_data_cache),
        "datasets": {
            key: {
                "total_records": len(v["data"]),
                "columns": len(v["headers"])
            }
            for key, v in _generated_data_cache.items()
        }
    }

@router.delete("/cache/{cache_key}")
async def clear_cache(cache_key: str):
    """Limpia datos del cache"""
    if cache_key in _generated_data_cache:
        del _generated_data_cache[cache_key]
        return {"success": True, "message": f"Cache {cache_key} eliminado"}
    return {"success": False, "message": "Cache no encontrado"}

# Funciones auxiliares de exportación

def _export_csv(data: List[Dict], headers: List[str]) -> str:
    """Exporta datos a CSV en memoria"""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(data[0].keys()) if data else [])
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()[:500] + "..."  # Preview

def _export_json(data: List[Dict]) -> str:
    """Exporta datos a JSON en memoria"""
    return json.dumps(data[:5], ensure_ascii=False) + "\n... y más registros"

def _export_sql(data: List[Dict], headers: List[str]) -> str:
    """Exporta datos a SQL en memoria"""
    table_name = "datos"
    sql = f"CREATE TABLE {table_name} (\n"
    
    for field in (list(data[0].keys()) if data else []):
        sql += f"    {field.lower()} VARCHAR(255),\n"
    
    sql = sql.rstrip(",\n") + "\n);\n\n"
    sql += f"-- {len(data)} INSERT statements seguirían...\n"
    
    return sql
