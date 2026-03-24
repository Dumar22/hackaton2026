from fastapi import APIRouter

router = APIRouter()

# Importar rutas específicas
from app.api.v1 import endpoints
from app.api.v1 import data_processing
from app.api.v1 import results

# Incluir endpoints
router.include_router(endpoints.router)
router.include_router(data_processing.router)
router.include_router(results.router)
