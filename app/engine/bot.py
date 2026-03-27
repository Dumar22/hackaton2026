"""
AI Chat Bot – Uses OpenAI GPT-4o-mini to answer natural language questions about the pipeline results.
"""
from typing import Any, Dict, List, Optional
from openai import OpenAI
from app.core.config import settings

class AIChatBot:
    """
    Takes pipeline results and allows querying them with natural language
    via OpenAI's GPT-4o-mini.
    """
    
    def __init__(self, api_key: str = settings.OPENAI_API_KEY):
        if api_key and api_key.startswith("sk-"):
            self.client = OpenAI(api_key=api_key)
            self._active = True
        else:
            self._active = False
    
    def chat(self, user_query: str, pipeline_data: Dict[str, Any]) -> str:
        """
        Sends a query to OpenAI including findings from the pipeline as context.
        """
        if not self._active:
            return "AI Chat disabled: A valid OPENAI_API_KEY is missing in .env."
            
        # Extract main findings for the context
        insights = pipeline_data.get("E_insights", {}).get("insights", [])
        decisions = pipeline_data.get("F_decisions", {}).get("decisions", [])
        risk_summary = pipeline_data.get("D_model", {})
        
        # Build strict system prompt
        system_prompt = f"""
        ROL: Eres el Asistente Experto en Inteligencia Educativa de CloudLabs.
        
        RESTRICCIONES CRÍTICAS: 
        1. SOLO puedes responder preguntas relacionadas con el análisis de datos de los estudiantes y el rendimiento de la plataforma CloudLabs.
        2. Si la pregunta es ajena a CloudLabs o a los datos provistos, responde: "Como asistente de análisis de CloudLabs, solo puedo ayudarte con información sobre el rendimiento académico y de negocio de nuestra plataforma."
        3. NO inventes datos. Usa solo la información del CONTEXTO DE DATOS.
        
        CONTEXTO DE DATOS ACTUALES:
        - Resumen de Riesgo: {risk_summary}
        - Insights clave: {insights}
        - Decisiones sugeridas con prioridad: {decisions}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=300,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error comunicando con la IA de OpenAI: {str(e)}"
