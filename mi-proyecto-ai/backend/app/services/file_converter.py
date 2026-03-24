"""
Servicio para convertir archivos a diferentes formatos
"""
from fastapi import UploadFile
import mimetypes

class FileConverter:
    """Clase para convertir archivos"""
    
    SUPPORTED_TYPES = {
        "text/plain": ".txt",
        "application/pdf": ".pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        "text/csv": ".csv"
    }
    
    async def convert(self, file: UploadFile) -> str:
        """
        Convierte un archivo a texto
        
        Args:
            file: Archivo a convertir
        
        Returns:
            Contenido del archivo en formato texto
        """
        content = await file.read()
        
        # Validar tipo de archivo
        if file.content_type not in self.SUPPORTED_TYPES:
            raise ValueError(f"Tipo de archivo no soportado: {file.content_type}")
        
        # Aquí iría la lógica específica de conversión
        return content.decode("utf-8")
