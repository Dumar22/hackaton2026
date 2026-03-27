"""
AI Chat Bot – Uses Gemini API to answer natural language questions about the pipeline results.
"""
from typing import Any, Dict, List, Optional
import google.generativeai as genai
from app.core.config import settings

class AIChatBot:
    """
    Takes pipeline results and allows querying them with natural language
    via Google's Gemini Pro.
    """
    
    def __init__(self, api_key: str = settings.GEMINI_API_KEY):
        if api_key and api_key != "":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self._active = True
        else:
            self._active = False
    
    def chat(self, user_query: str, pipeline_data: Dict[str, Any]) -> str:
        """
        Sends a query to Gemini including findings from the pipeline as context.
        """
        if not self._active:
            return "AI Chat disabled: GEMINI_API_KEY is missing in .env."
            
        # Extract main findings for the context
        insights = pipeline_data.get("E_insights", {}).get("insights", [])
        decisions = pipeline_data.get("F_decisions", {}).get("decisions", [])
        risk_summary = pipeline_data.get("D_model", {})
        
        # Build context prompt
        context = f"""
        You are an Educational Data Analyst assistant for CloudLabs. 
        Current pipeline results:
        - Risk Summary: {risk_summary}
        - Key Insights: {insights[:5]}
        - Key Decisions to take: {decisions[:5]}
        
        Based on this data, answer the user's question concisely and accurately.
        """
        
        prompt = f"{context}\n\nUser Question: {user_query}\nAnswer:"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"
