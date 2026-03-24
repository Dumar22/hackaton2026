"""
Lógica de negocio de la aplicación
"""
from typing import Any, Dict
from app.integrations.gpt_client import GPTClient
from app.integrations.gemini_client import GeminiClient
from app.integrations.kimi_client import KimiClient

class BusinessLogic:
    """Clase para manejar la lógica de negocio"""
    
    def __init__(self):
        self.gpt_client = GPTClient()
        self.gemini_client = GeminiClient()
        self.kimi_client = KimiClient()
    
    async def process(self, content: str, model: str) -> dict:
        """
        Procesa contenido con el modelo especificado
        
        Args:
            content: Contenido a procesar
            model: Modelo a utilizar
        
        Returns:
            Resultado del procesamiento
        """
        if model == "gpt":
            return await self.gpt_client.process(content)
        elif model == "gemini":
            return await self.gemini_client.process(content)
        elif model == "kimi":
            return await self.kimi_client.process(content)
        else:
            raise ValueError(f"Modelo no soportado: {model}")
