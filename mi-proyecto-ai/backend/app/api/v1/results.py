"""
Endpoints para servir resultados del análisis de patrones y automatización
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
import json
import os

router = APIRouter(prefix="/results", tags=["results"])

# Ruta base para los archivos de resultados
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '../../../../output_data_processing')


def _ensure_results_dir():
    """Verifica que el directorio de resultados exista"""
    if not os.path.exists(RESULTS_DIR):
        raise HTTPException(
            status_code=404,
            detail="Directorio de resultados no encontrado. Ejecuta el notebook primero."
        )


@router.get("/metadata")
async def get_metadata():
    """
    Obtiene los metadatos del análisis (accuracy, confianza, distribuciones, etc.)
    
    Returns:
        Diccionario con metadatos del pipeline
    """
    _ensure_results_dir()
    
    metadata_file = os.path.join(RESULTS_DIR, 'metadata_completo.json')
    
    if not os.path.exists(metadata_file):
        raise HTTPException(
            status_code=404,
            detail="Archivo de metadatos no encontrado"
        )
    
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        return metadata
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo metadatos: {str(e)}"
        )


@router.get("/predictions", response_class=PlainTextResponse)
async def get_predictions():
    """
    Obtiene las predicciones en formato CSV
    
    Returns:
        CSV con todas las predicciones y acciones automáticas
    """
    _ensure_results_dir()
    
    predictions_file = os.path.join(RESULTS_DIR, 'predicciones_automatizacion.csv')
    
    if not os.path.exists(predictions_file):
        raise HTTPException(
            status_code=404,
            detail="Archivo de predicciones no encontrado"
        )
    
    try:
        with open(predictions_file, 'r', encoding='utf-8') as f:
            csv_content = f.read()
        
        return csv_content
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo predicciones: {str(e)}"
        )


@router.get("/summary")
async def get_summary():
    """
    Obtiene un resumen ejecutivo de los resultados
    
    Returns:
        Resumen con KPIs principales
    """
    _ensure_results_dir()
    
    metadata_file = os.path.join(RESULTS_DIR, 'metadata_completo.json')
    
    if not os.path.exists(metadata_file):
        raise HTTPException(
            status_code=404,
            detail="Archivo de metadatos no encontrado"
        )
    
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        summary = {
            "success": True,
            "version": metadata.get("metadata", {}).get("versión", "N/A"),
            "total_records": metadata.get("metadata", {}).get("total_registros", 0),
            "model_accuracy": metadata.get("metadata", {}).get("accuracy", 0),
            "average_confidence": metadata.get("metadata", {}).get("confianza_promedio", 0),
            "actions_summary": metadata.get("acciones_automáticas", {}),
            "predictions_distribution": metadata.get("distribución_predicciones", {}),
            "model_name": metadata.get("metadata", {}).get("modelo", "N/A"),
            "pipeline_execution_date": metadata.get("metadata", {}).get("fecha_ejecución", "N/A"),
        }
        
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando resumen: {str(e)}"
        )


@router.get("/files")
async def list_available_files():
    """
    Lista todos los archivos de resultados disponibles
    
    Returns:
        Lista de archivos disponibles
    """
    _ensure_results_dir()
    
    try:
        files = os.listdir(RESULTS_DIR)
        file_info = []
        
        for filename in sorted(files):
            filepath = os.path.join(RESULTS_DIR, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                file_info.append({
                    "filename": filename,
                    "size": size,
                    "size_mb": round(size / (1024 * 1024), 2)
                })
        
        return {
            "success": True,
            "total_files": len(file_info),
            "files": file_info
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listando archivos: {str(e)}"
        )
