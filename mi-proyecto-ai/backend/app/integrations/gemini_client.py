"""
Cliente para integración con Google Gemini
"""
from typing import Dict
import google.generativeai as genai
from app.core.config import settings

class GeminiClient:
    """Cliente para Gemini"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def process(self, content: str) -> dict:
        """
        Procesa contenido con Gemini
        
        Args:
            content: Contenido a procesar
        
        Returns:
            Resultado del procesamiento
        """
        try:
            response = self.model.generate_content(content)
            
            return {
                "model": "gemini-pro",
                "response": response.text,
                "finish_reason": response.candidates[0].finish_reason
            }
        except Exception as e:
            return {"error": str(e), "model": "gemini-pro"}
