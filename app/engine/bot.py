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
        self._active = False
        if api_key and (api_key.startswith("sk-") or len(api_key) > 20):
            try:
                self.client = OpenAI(api_key=api_key)
                self._active = True
            except Exception:
                self._active = False

    def chat(self, user_query: str, pipeline_data: Dict[str, Any]) -> str:
        """
        AI Analyst with Dual Response format (Data + Interpretation).
        """
        if not self._active:
            return "⚠️ IA Desconectada: Configura tu OPENAI_API_KEY en el archivo .env correctamente."
            
        # Contexto de CloudLabs basado en el PDF de la empresa
        cloudlabs_context = """
        CONTEXTO EMPRESA: CloudLabs Learning es una plataforma EdTech colombiana presente en 32 países. 
        Misión: Revolucionar la educación STEM mediante simulaciones inmersivas y aprendizaje basado en retos.
        Impacto: +900,000 estudiantes y +5,000 instituciones.
        Metodología: Aprendizaje centrado en el estudiante, multidisciplinar y centrado en resultados reales.
        """
        
        # Limpiar datos masivos para ahorrar tokens (No enviar listas de 50k IDs)
        clean_insights = []
        for i in pipeline_data.get("E_insights", {}).get("insights", []):
            clean_insights.append({
                "titulo": i.get("title"),
                "descripcion": i.get("description"),
                "metrica": i.get("metric")
            })
            
        clean_decisions = []
        for d in pipeline_data.get("F_decisions", {}).get("decisions", []):
            clean_decisions.append({
                "prioridad": d.get("priority"),
                "tipo_accion": d.get("action_type"),
                "resumen": d.get("summary")
            })

        risk_summary = pipeline_data.get("D_model", {})
        
        system_prompt = f"""
        {cloudlabs_context}
        
        ROL: Eres el Copiloto de Inteligencia de Negocio de CloudLabs. 
        TU MISIÓN: Ayudar a los tomadores de decisiones a convertir datos en acciones de retención de estudiantes.
        
        FORMATO DE RESPUESTA OBLIGATORIO:
        1. 📊 RESPUESTA DIRECTA: Un dato estadístico preciso. Nota: El 'Ranking de Producto Estrella' provisto en los hallazgos REPRESENTA la actividad más reciente/del día. Úsalo para responder preguntas sobre tendencias actuales.
        2. 💡 INTERPRETACIÓN: Una lectura estratégica del dato basada en la misión de CloudLabs.
        
        RESTRICCIONES:
        - No te disculpes por falta de datos si el Ranking contiene información relevante.
        - Sé proactivo y experto.
        - Datos del pipeline:
          - Riesgo: {risk_summary}
          - Hallazgos Críticos: {clean_insights}
          - Acciones Sugeridas: {clean_decisions}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=500,
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error en el motor de IA: {str(e)}"
