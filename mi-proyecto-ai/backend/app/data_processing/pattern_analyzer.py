"""
Analizador de patrones usando IA para identificar insights y anomalías
"""
from typing import List, Dict, Any
import json
from app.integrations.gpt_client import GPTClient
from app.integrations.gemini_client import GeminiClient
from app.integrations.kimi_client import KimiClient

class PatternAnalyzer:
    """Analiza patrones en datos usando modelos de IA"""
    
    def __init__(self, model: str = "gpt"):
        """
        Args:
            model: Modelo a usar ("gpt", "gemini", "kimi")
        """
        self.model_name = model
        
        if model == "gpt":
            self.client = GPTClient()
        elif model == "gemini":
            self.client = GeminiClient()
        elif model == "kimi":
            self.client = KimiClient()
        else:
            raise ValueError(f"Modelo no soportado: {model}")
    
    async def analyze_patterns(self, data: List[Dict], stats: Dict = None) -> Dict[str, Any]:
        """
        Analiza patrones en los datos usando IA
        
        Args:
            data: Lista de registros
            stats: Estadísticas del dataset
        
        Returns:
            Análisis de patrones y recomendaciones
        """
        # Preparar resumen de datos
        summary = self._prepare_summary(data, stats)
        
        prompt = f"""
Analiza los siguientes datos de ventas y proporciona:
1. Patrones principales identificados
2. Anomalías o datos atípicos
3. Oportunidades de mejora
4. Recomendaciones de automatización

Datos: {summary}

Proporciona el análisis en formato JSON estructurado.
"""
        
        result = await self.client.process(prompt)
        
        return {
            "model": self.model_name,
            "analysis": result.get("response", ""),
            "usage": result.get("usage", {})
        }
    
    async def classify_records(self, records: List[Dict], criteria: str) -> Dict[str, List[Dict]]:
        """
        Clasifica registros basado en criterios usando IA
        
        Args:
            records: Lista de registros
            criteria: Criterios de clasificación
        
        Returns:
            Registros clasificados por categoría
        """
        # Preparar muestra para contexto
        sample = json.dumps(records[:10], ensure_ascii=False)
        
        prompt = f"""
Clasifica los siguientes registros según el criterio: {criteria}

Muestra de datos: {sample}

Para cada clasificación, proporciona:
1. Nombre de categoría
2. Criterios de pertenencia
3. Ejemplos de registros

Responde en JSON con estructura: {{"clasificaciones": [{{"nombre": "", "criterios": "", "ejemplos": []}}]}}
"""
        
        result = await self.client.process(prompt)
        
        try:
            analysis = json.loads(result.get("response", "{}"))
        except:
            analysis = {"raw_response": result.get("response", "")}
        
        return {
            "model": self.model_name,
            "classifications": analysis,
            "usage": result.get("usage", {})
        }
    
    async def identify_anomalies(self, data: List[Dict], field: str = None) -> Dict[str, Any]:
        """
        Identifica anomalías en los datos usando IA
        
        Args:
            data: Lista de registros
            field: Campo específico a analizar (opcional)
        
        Returns:
            Anomalías identificadas
        """
        # Preparar análisis estadístico
        analysis = self._statistical_analysis(data, field)
        
        prompt = f"""
Identifica anomalías en los siguientes datos:

Análisis estadístico: {json.dumps(analysis, ensure_ascii=False)}

Proporciona:
1. Anomalías detectadas
2. Nivel de severidad (alto/medio/bajo)
3. Posibles causas
4. Acciones recomendadas

Responde en JSON.
"""
        
        result = await self.client.process(prompt)
        
        return {
            "model": self.model_name,
            "anomalies": result.get("response", ""),
            "statistical_analysis": analysis,
            "usage": result.get("usage", {})
        }
    
    async def generate_recommendations(self, data: List[Dict], stats: Dict = None) -> Dict[str, Any]:
        """
        Genera recomendaciones de automatización basadas en patrones
        
        Args:
            data: Lista de registros
            stats: Estadísticas del dataset
        
        Returns:
            Recomendaciones de automatización
        """
        summary = self._prepare_summary(data, stats)
        
        prompt = f"""
Basado en los siguientes datos de negocio, proporciona recomendaciones específicas 
para automatizar procesos y mejorar eficiencia:

{summary}

Para cada recomendación, incluye:
1. Proceso a automatizar
2. Tecnología/herramienta a usar
3. Impacto esperado (en %)
4. Complejidad (baja/media/alta)
5. Tiempo de implementación (en días)
6. ROI estimado

Responde en JSON con estructura: {{"recomendaciones": [{{"proceso": "", "tecnologia": "", "impacto": "", "complejidad": "", "tiempo": "", "roi": ""}}]}}
"""
        
        result = await self.client.process(prompt)
        
        return {
            "model": self.model_name,
            "recommendations": result.get("response", ""),
            "usage": result.get("usage", {})
        }
    
    def _prepare_summary(self, data: List[Dict], stats: Dict = None) -> str:
        """Prepara resumen de datos para el prompt"""
        if not stats:
            stats = self._calculate_stats(data)
        
        summary = f"""
DATASET SUMMARY:
- Total de registros: {len(data)}
- Campos: {list(data[0].keys()) if data else []}
- Rango de fechas: {self._get_date_range(data)}

ESTADÍSTICAS:
{json.dumps(stats, indent=2, ensure_ascii=False)}

MUESTRA DE DATOS (primeros 5 registros):
{json.dumps(data[:5], indent=2, ensure_ascii=False)}
"""
        return summary
    
    def _calculate_stats(self, data: List[Dict]) -> Dict:
        """Calcula estadísticas básicas"""
        if not data:
            return {}
        
        stats = {}
        
        # Campos numéricos
        numeric_fields = {}
        for record in data:
            for key, value in record.items():
                try:
                    val = float(value)
                    if key not in numeric_fields:
                        numeric_fields[key] = []
                    numeric_fields[key].append(val)
                except (ValueError, TypeError):
                    pass
        
        # Cálculos
        for field, values in numeric_fields.items():
            if values:
                stats[field] = {
                    "min": min(values),
                    "max": max(values),
                    "promedio": sum(values) / len(values),
                    "total": sum(values)
                }
        
        return stats
    
    def _statistical_analysis(self, data: List[Dict], field: str = None) -> Dict:
        """Análisis estadístico detallado"""
        analysis = {
            "total_registros": len(data),
            "campos": list(data[0].keys()) if data else [],
        }
        
        if field and data:
            values = []
            for record in data:
                try:
                    values.append(float(record.get(field, 0)))
                except (ValueError, TypeError):
                    pass
            
            if values:
                analysis[field] = {
                    "min": min(values),
                    "max": max(values),
                    "promedio": sum(values) / len(values),
                    "rango": max(values) - min(values),
                    "desviacion_estandar": self._calculate_std_dev(values)
                }
        
        return analysis
    
    def _calculate_std_dev(self, values: List[float]) -> float:
        """Calcula desviación estándar"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _get_date_range(self, data: List[Dict]) -> str:
        """Obtiene rango de fechas en los datos"""
        dates = []
        for record in data:
            for key in ['fecha', 'date', 'Fecha', 'Date']:
                if key in record:
                    dates.append(record[key])
                    break
        
        if dates:
            dates.sort()
            return f"{dates[0]} a {dates[-1]}"
        return "No determinado"
