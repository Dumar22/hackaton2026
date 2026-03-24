"""
Punto de entrada principal de la aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Inicializar aplicación
app = FastAPI(
    title="AI Project API",
    description="API para procesamiento de IA integrado con múltiples modelos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar routers
from app.api.v1 import router as api_v1_router

# Incluir routers
app.include_router(api_v1_router, prefix="/api/v1", tags=["v1"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
