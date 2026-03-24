"""
Cliente para integración con Kimi AI
"""
from typing import Dict
import aiohttp
from app.core.config import settings

class KimiClient:
    """Cliente para Kimi"""
    
    def __init__(self):
        self.api_key = settings.KIMI_API_KEY
        self.base_url = "https://api.kimi.ai"
    
    async def process(self, content: str) -> dict:
        """
        Procesa contenido con Kimi
        
        Args:
            content: Contenido a procesar
        
        Returns:
            Resultado del procesamiento
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "messages": [
                        {"role": "user", "content": content}
                    ]
                }
                
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers
                ) as response:
                    result = await response.json()
                    
                    return {
                        "model": "kimi",
                        "response": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                        "status": response.status
                    }
        except Exception as e:
            return {"error": str(e), "model": "kimi"}
