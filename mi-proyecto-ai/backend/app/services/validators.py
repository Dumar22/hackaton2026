"""
Validadores personalizados
"""
from pydantic import BaseModel, validator

class FileUploadValidator(BaseModel):
    """Validador para carga de archivos"""
    
    filename: str
    file_size: int
    content_type: str
    
    @validator('file_size')
    def validate_file_size(cls, v):
        max_size = 50 * 1024 * 1024  # 50MB
        if v > max_size:
            raise ValueError(f"Archivo demasiado grande: {v} bytes")
        return v
    
    @validator('content_type')
    def validate_content_type(cls, v):
        allowed = ['text/plain', 'application/pdf', 'text/csv']
        if v not in allowed:
            raise ValueError(f"Tipo de contenido no permitido: {v}")
        return v
