"""
User-Centric Recommendation Engine.
Provides personalized learning paths for students based on their behavior.
"""
import pandas as pd
from typing import List, Dict, Any

class Recommender:
    def __init__(self, cleaned_data: Dict[str, pd.DataFrame]):
        self.users = cleaned_data.get("usuarios")
        self.interactions = cleaned_data.get("interacciones")
        self.products = cleaned_data.get("productos")
        self.events = cleaned_data.get("eventos")

    def get_student_recommendations(self, user_id: int) -> Dict[str, Any]:
        """
        Generates a personalized recommendation for a specific student.
        """
        user_ints = self.interactions[self.interactions["usuario_id"] == user_id]
        
        if user_ints.empty:
            return {
                "message": "¡Bienvenido a CloudLabs! Comienza con nuestra simulación más popular: Física Mecánica.",
                "type": "onboarding"
            }
            
        # Analizar qué ha completado
        completed = user_ints[user_ints["accion"] == "completado"]
        abandoned = user_ints[user_ints["accion"] == "abandonado"]
        
        if not abandoned.empty:
            last_abandoned = abandoned.iloc[-1]["producto_id"]
            prod_name = self.products[self.products["producto_id"] == last_abandoned]["nombre"].values[0]
            return {
                "message": f"Vimos que tuviste problemas con '{prod_name}'. ¿Quieres ver un tutorial antes de intentarlo de nuevo?",
                "type": "support",
                "target_product": prod_name
            }
            
        if not completed.empty:
            # Recomendar algo de la misma categoría
            last_prod = completed.iloc[-1]["producto_id"]
            cat = self.products[self.products["producto_id"] == last_prod]["categoria"].values[0]
            suggested = self.products[self.products["categoria"] == cat].sample(1)
            
            return {
                "message": f"Eres un experto en {cat}. Basado en tu éxito, te recomendamos avanzar a: {suggested['nombre'].values[0]}.",
                "type": "growth",
                "target_product": suggested['nombre'].values[0]
            }

        return {"message": "Sigue explorando nuestras simulaciones STEM.", "type": "general"}
