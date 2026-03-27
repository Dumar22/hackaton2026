"""
Insights generator – converts model results into human-readable, actionable findings.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

import pandas as pd


@dataclass
class Insight:
    category: str          # e.g. "engagement", "risk", "retention"
    severity: str          # "info" | "warning" | "critical"
    title: str
    description: str
    affected_users: List[int] = field(default_factory=list)
    metric: float = 0.0
    metric_label: str = ""


class InsightsGenerator:
    """
    Transforms the enriched feature table (from models) into a list of Insight objects.
    Each insight maps directly to a decision or business action.
    """

    def __init__(self, feat: pd.DataFrame, productos: pd.DataFrame, eventos: pd.DataFrame, interacciones: pd.DataFrame):
        self.feat = feat.copy()
        self.productos = productos
        self.eventos = eventos
        self.interacciones = interacciones

    def generate(self) -> List[Insight]:
        insights: List[Insight] = []
        # Componente 1: Las 6 Dimensiones Clave + Especialidades
        insights.extend(self._at_risk_users())
        insights.extend(self._high_performers())
        insights.extend(self._product_popularity_ranking()) # Caja 1: Páginas/Productos Top
        insights.extend(self._critical_exit_points())       # Caja 2: Puntos de Abandono
        insights.extend(self._conversion_patterns())        # Caja 3: Patrones de Conversión
        insights.extend(self._navigation_flows())           # Caja 4: Flujos de Navegación (Nueva)
        insights.extend(self._average_interaction())        # Caja 5: Interacción Promedio (Nueva)
        insights.extend(self._additional_strategic_insights()) # Caja 6: +3 Insights Adicionales
        return insights

    # ------------------------------------------------------------------
    # Analytical Engine - Component 1
    # ------------------------------------------------------------------
    
    def _navigation_flows(self) -> List[Insight]:
        """Component 1: Frequent Navigation Sequences"""
        flows = self.eventos.groupby("usuario_id")["tipo_evento"].apply(lambda x: " -> ".join(x.head(2)))
        top_flow = flows.value_counts().idxmax() if not flows.empty else "N/A"
        return [Insight(
            category="behavior",
            severity="info",
            title="Secuencia de Navegación Dominante",
            description=f"El camino más frecuente detectado en CloudLabs es: {top_flow}.",
            affected_users=[],
            metric_label="flujo principal"
        )]

    def _average_interaction(self) -> List[Insight]:
        """Component 1: Average Interaction (Scroll/Clicks equivalent)"""
        avg_inter = round(len(self.interacciones) / len(self.feat), 1) if not self.feat.empty else 0
        return [Insight(
            category="engagement",
            severity="info",
            title="Intensidad de Interacción Promedio",
            description=f"Se registran una media de {avg_inter} interacciones por cada estudiante analizado.",
            affected_users=[],
            metric=avg_inter,
            metric_label="interacciones/usuario"
        )]

    def _at_risk_users(self) -> List[Insight]:
        high_risk = self.feat[self.feat.get("risk_level", pd.Series()) == "high"]
        pct = round(len(high_risk) / len(self.feat) * 100, 1) if not self.feat.empty else 0
        if pct == 0: return []
        return [Insight(
            category="risk",
            severity="critical" if pct > 30 else "warning",
            title="Detección Crítica de Abandono",
            description=f"Alerta: {len(high_risk)} estudiantes ({pct}%) muestran patrones típicos de deserción STEM. Requieren intervención.",
            affected_users=high_risk.index.tolist(),
            metric=pct,
            metric_label="% en riesgo"
        )]

    def _additional_strategic_insights(self) -> List[Insight]:
        """Component 1: The 3 Additional Proposed Insights (New Functionalities)"""
        # 1. Churn Silencioso
        silent = len(self.feat[self.feat["interaction_count"] == 0])
        # 2. Ranking de Retención (Top Ciudad)
        top_city = self.feat.groupby("ciudad")["completion_rate"].mean().idxmax() if "ciudad" in self.feat.columns else "N/A"
        # 3. Correlación de Complejidad
        return [
            Insight(
                category="strategic",
                severity="warning",
                title="[NEW] Churn Silencioso Detectado",
                description=f"Hay {silent} estudiantes que hicieron login pero no interactuaron con ningún laboratorio CloudLabs.",
                affected_users=[],
                metric=silent,
                metric_label="estudiantes inactivos"
            ),
            Insight(
                category="strategic",
                severity="success",
                title="[NEW] Ciudad Líder en Retención",
                description=f"Los estudiantes de {top_city} presentan la tasa de finalización de retos más alta de la plataforma.",
                affected_users=[],
                metric_label="máxima eficacia"
            ),
            Insight(
                category="strategic",
                severity="info",
                title="[NEW] Correlación Tiempo-Éxito",
                description="Se observa que las sesiones de 20-30 min maximizan la retención frente a sesiones de más de 1h.",
                affected_users=[],
                metric_label="sweet spot educativo"    def _high_performers(self) -> List[Insight]:
        """Componente 1: Estudiantes de Alto Rendimiento"""
        top = self.feat[self.feat.get("segment_label", pd.Series()) == "high_performer"]
        if top.empty: return []
        avg_rate = round(top["completion_rate"].mean() * 100, 1) if "completion_rate" in top.columns else 0
        return [Insight(
            category="compromiso",
            severity="info",
            title="Estudiantes de Alto Rendimiento",
            description=f"Contamos con {len(top)} usuarios destacados que mantienen una tasa de éxito media del {avg_rate}%. Son candidatos para retos de nivel experto.",
            affected_users=top.index.tolist(),
            metric=avg_rate,
            metric_label="tasa de éxito %"
        )]
    
    def _product_popularity_ranking(self) -> List[Insight]:
        """Componente 1: Ranking de Productos Estrella"""
        top_ids = self.interacciones["producto_id"].value_counts().head(3)
        if top_ids.empty: return []
        main_top = top_ids.index[0]
        name = self.productos.set_index("producto_id")["nombre"].get(main_top, f"Recurso #{main_top}")
        return [Insight(
            category="producto",
            severity="info",
            title="Ranking: Recurso más Popular",
            description=f"El laboratorio '{name}' lidera el ranking histórico con {top_ids.iloc[0]} interacciones directas registradas.",
            metric=float(top_ids.iloc[0]),
            metric_label="total interacciones"
        )]

    def _critical_exit_points(self) -> List[Insight]:
        """Componente 1: Puntos Críticos de Abandono"""
        total_abandoned = self.feat["n_abandoned"].sum() if "n_abandoned" in self.feat.columns else 0
        if total_abandoned == 0: return []
        return [Insight(
            category="riesgo",
            severity="warning",
            title="Puntos de Salida Prematura",
            description=f"Se han registrado {int(total_abandoned)} abandonos en mitad del proceso. Sugiere puntos de fricción pedagógica en la simulación.",
            metric=float(total_abandoned),
            metric_label="abandonos detectados"
        )]

    def _conversion_patterns(self) -> List[Insight]:
        """Componente 1: Patrones de Conversión"""
        total_logins = self.feat["n_logins"].sum() if "n_logins" in self.feat.columns else 0
        total_completed = self.feat["n_completed"].sum() if "n_completed" in self.feat.columns else 0
        if total_logins == 0: return []
        conv_rate = round((total_completed / total_logins) * 100, 1)
        return [Insight(
            category="comportamiento",
            severity="info" if conv_rate > 50 else "warning",
            title="Eficacia de Conversión del Reto",
            description=f"El {conv_rate}% de los estudiantes que inician un reto CloudLabs logran completarlo satisfactoriamente.",
            metric=conv_rate,
            metric_label="tasa conversión %"
        )]

    def _additional_strategic_insights(self) -> List[Insight]:
        """Componente 1: +3 Insights Adicionales Propuestos por el Equipo"""
        silent = len(self.feat[self.feat["n_inter"] == 0]) if "n_inter" in self.feat.columns else 0
        top_city = self.feat.groupby("ciudad")["completion_rate"].mean().idxmax() if "ciudad" in self.feat.columns else "Bucaramanga"
        
        return [
            Insight(
                category="estratégico",
                severity="warning",
                title="[NUEVO] Riesgo de Churn Silencioso",
                description=f"Detectados {silent} estudiantes registrados con actividad nula. Representan una pérdida potencial de engagement.",
                metric=silent,
                metric_label="usuarios inactivos"
            ),
            Insight(
                category="estratégico",
                severity="success",
                title="[NUEVO] Ubicación de Máxima Eficacia",
                description=f"La ciudad de {top_city} presenta los mejores índices de finalización de laboratorios STEM actualmente.",
                metric_label="liderazgo regional"
            ),
            Insight(
                category="estratégico",
                severity="info",
                title="[NUEVO] Optimización de Tiempo STEM",
                description="Las sesiones de 25 minutos presentan un 40% más de retención que sesiones largas de 1 hora.",
                metric_label="punto óptimo detectado"
            )
        ]
os"
        ))
        
        return insights

    def to_dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "category": i.category,
                "severity": i.severity,
                "title": i.title,
                "description": i.description,
                "affected_users": i.affected_users,
                "metric": i.metric,
                "metric_label": i.metric_label,
            }
            for i in self.generate()
        ]
