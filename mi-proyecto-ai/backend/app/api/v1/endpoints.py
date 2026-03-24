"""
Endpoints principales de la API v1
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict
from datetime import datetime, timezone
import uuid
from app.services.business_logic import BusinessLogic
from app.services.file_converter import FileConverter

router = APIRouter()

business_logic = BusinessLogic()
file_converter = FileConverter()
_process_history: List[Dict] = []


def _build_result_preview(result: Dict) -> str:
    """Construye una vista corta del resultado para historial."""
    text = str(result)
    return text[:200] + ("..." if len(text) > 200 else "")

@router.post("/process-ai")
async def process_ai(file: UploadFile = File(...), model: str = "gpt"):
    """
    Procesa un archivo con el modelo de IA especificado
    
    Args:
        file: Archivo a procesar
        model: Modelo a utilizar (gpt, gemini, kimi)
    
    Returns:
        Resultado del procesamiento
    """
    try:
        # Convertir archivo
        content = await file_converter.convert(file)
        
        # Procesar con lógica de negocio
        result = await business_logic.process(content, model)
        has_model_error = isinstance(result, dict) and bool(result.get("error"))

        history_item = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "file_name": file.filename,
            "model": model,
            "success": not has_model_error,
            "error": result.get("error") if has_model_error and isinstance(result, dict) else None,
            "result_preview": _build_result_preview(result)
        }
        _process_history.insert(0, history_item)
        del _process_history[200:]
        
        request_success = "error" not in result
        return {"success": request_success, "result": result, "history_id": history_item["id"]}
    except Exception as e:
        _process_history.insert(0, {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "file_name": file.filename,
            "model": model,
            "success": False,
            "error": str(e),
            "result_preview": None
        })
        del _process_history[200:]
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/process-history")
async def get_process_history(limit: int = 50):
    """Retorna historial de ejecuciones de /process-ai."""
    safe_limit = min(max(limit, 1), 200)
    return {
        "total": len(_process_history),
        "items": _process_history[:safe_limit]
    }

@router.get("/models")
async def get_available_models():
    """Retorna los modelos disponibles"""
    return {
        "models": ["gpt", "gemini", "kimi"],
        "description": "Modelos de IA disponibles"
    }
