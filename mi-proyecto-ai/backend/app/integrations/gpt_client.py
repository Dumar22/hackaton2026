"""
Cliente para integración con OpenAI GPT
"""
from openai import AsyncOpenAI
from app.core.config import settings

class GPTClient:
    """Cliente para GPT"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.default_model = "gpt-4o-mini"
    
    async def process(self, content: str) -> dict:
        """
        Procesa contenido con GPT
        
        Args:
            content: Contenido a procesar
        
        Returns:
            Resultado del procesamiento
        """
        try:
            if not settings.OPENAI_API_KEY:
                return {"error": "OPENAI_API_KEY no configurada", "model": self.default_model}

            response = await self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "Eres un asistente de IA útil"},
                    {"role": "user", "content": content}
                ],
                temperature=0.7,
            )

            usage = response.usage.model_dump() if response.usage else None
            message = response.choices[0].message.content if response.choices else ""
            
            return {
                "model": response.model or self.default_model,
                "response": message,
                "usage": usage
            }
        except Exception as e:
            return {"error": str(e), "model": self.default_model}
