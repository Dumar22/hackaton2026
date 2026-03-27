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
        insights.extend(self._at_risk_users())
        insights.extend(self._high_performers())
        insights.extend(self._product_popularity_ranking())
        insights.extend(self._critical_exit_points())
        insights.extend(self._conversion_patterns())
        insights.extend(self._additional_strategic_insights())
        return insights

    # ------------------------------------------------------------------
    # Analytical Engine - Component 1
    # ------------------------------------------------------------------
    def _at_risk_users(self) -> List[Insight]:
        high_risk = self.feat[self.feat.get("risk_level", pd.Series()) == "high"]
        if high_risk.empty:
            return []
        pct = round(len(high_risk) / len(self.feat) * 100, 1)
        return [Insight(
            category="risk",
            severity="critical" if pct > 30 else "warning",
            title="Detección de Riesgo de Abandono",
            description=(
                f"Hemos identificado {len(high_risk)} usuarios ({pct}%) con alta probabilidad "
                "de abandonar sus retos STEM. Requieren intervención inmediata."
            ),
            affected_users=high_risk.index.tolist(),
            metric=pct,
            metric_label="% usuarios en riesgo",
        )]

    def _high_performers(self) -> List[Insight]:
        top = self.feat[self.feat.get("segment_label", pd.Series()) == "high_performer"]
        if top.empty:
            return []
        avg_rate = round(top["completion_rate"].mean() * 100, 1)
        return [Insight(
            category="engagement",
            severity="info",
            title="Segmento de Alto Rendimiento",
            description=(
                f"Contamos con {len(top)} estudiantes destacados con una tasa de finalización "
                f"del {avg_rate}%. Listos para retos de nivel experto."
            ),
            affected_users=top.index.tolist(),
            metric=avg_rate,
            metric_label="tasa de éxito promedio %",
        )]
    
    def _product_popularity_ranking(self) -> List[Insight]:
        """Component 1: Ranking of Top Products/Pages"""
        top_ids = self.interacciones["producto_id"].value_counts().head(3)
        if top_ids.empty: return []
        
        main_top = top_ids.index[0]
        name = self.productos.set_index("producto_id")["nombre"].get(main_top, str(main_top))
        
        return [Insight(
            category="product",
            severity="info",
            title="Ranking: Producto Estrella Identificado",
            description=(
                f"El recurso '{name}' lidera el ranking con {top_ids.iloc[0]} interacciones. "
                "Representa el punto de mayor interés para la comunidad CloudLabs."
            ),
            metric=float(top_ids.iloc[0]),
            metric_label="interacciones totales"
        )]

    def _critical_exit_points(self) -> List[Insight]:
        """Component 1: Critical Abandonment Points"""
        # Comparar inicios vs completados por producto
        starts = self.eventos[self.eventos["tipo_evento"] == "simulacion"].groupby("usuario_id").size()
        # En una demo real cruzaríamos con el ID del producto si estuviera en eventos
        # Por ahora, usamos el ratio global de abandono del feat
        total_abandoned = self.feat["n_abandoned"].sum()
        if total_abandoned == 0: return []
        
        return [Insight(
            category="risk",
            severity="warning",
            title="Puntos Críticos de Abandono",
            description=(
                f"Se detectaron {int(total_abandoned)} sesiones interrumpidas. "
                "Los estudiantes tienden a salir antes de los resultados de aprendizaje finales."
            ),
            metric=float(total_abandoned),
            metric_label="abandonos totales"
        )]

    def _conversion_patterns(self) -> List[Insight]:
        """Component 1: Conversion Patterns"""
        total_logins = self.feat["n_logins"].sum()
        total_completions = self.feat["n_completed"].sum()
        if total_logins == 0: return []
        
        conv_rate = round((total_completions / total_logins) * 100, 1)
        return [Insight(
            category="retention",
            severity="info" if conv_rate > 50 else "warning",
            title="Patrón de Conversión Educativa",
            description=(
                f"Tasa de Conversión (Login -> Éxito) del {conv_rate}%. "
                "Esta métrica mide la efectividad de nuestra metodología basada en retos."
            ),
            metric=conv_rate,
            metric_label="conversión %"
        )]

    def _additional_strategic_insights(self) -> List[Insight]:
        """Component 1: +3 Additional Insights justified by the team"""
        insights = []
        
        # 1. Éxito por Rango de Edad (Insights 1)
        if "edad" in self.feat.columns:
            age_success = self.feat.groupby(pd.cut(self.feat["edad"], bins=[0, 25, 45, 100]))["completion_rate"].mean()
            best_age = age_success.idxmax()
            insights.append(Insight(
                category="demographics",
                severity="info",
                title="Insight Adicional #1: Segmento Generacional",
                description=f"El grupo de edad {best_age} presenta el mayor índice de éxito con nuestra metodología.",
                metric=float(age_success.max() * 100),
                metric_label="éxito %"
            ))
            
        # 2. Correlación de Actividad (Logins vs Completados) (Insights 2)
        corr = self.feat["n_logins"].corr(self.feat["n_completed"])
        insights.append(Insight(
            category="engagement",
            severity="info",
            title="Insight Adicional #2: Predictor de Éxito",
            description=f"Existe una correlación de {round(corr, 2)} entre el acceso a la plataforma y la finalización de retos.",
            metric=round(corr, 2),
            metric_label="coeficiente de correlación"
        ))
        
        # 3. Alerta de Inactividad (Insights 3)
        zero_activity = self.feat[self.feat["n_logins"] == 0]
        insights.append(Insight(
            category="retention",
            severity="critical" if len(zero_activity) > 0 else "info",
            title="Insight Adicional #3: Riesgo de Churn Silencioso",
            description=f"Detectados {len(zero_activity)} usuarios con 0 actividad tras el registro inicial.",
            metric=float(len(zero_activity)),
            metric_label="usuarios inactivos"
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
