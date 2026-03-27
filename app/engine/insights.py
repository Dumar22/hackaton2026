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

    def __init__(self, feat: pd.DataFrame, productos: pd.DataFrame):
        self.feat = feat.copy()
        self.productos = productos

    def generate(self) -> List[Insight]:
        insights: List[Insight] = []
        insights.extend(self._at_risk_users())
        insights.extend(self._high_performers())
        insights.extend(self._low_engagement())
        insights.extend(self._product_popularity())
        return insights

    # ------------------------------------------------------------------
    # Internal generators
    # ------------------------------------------------------------------
    def _at_risk_users(self) -> List[Insight]:
        high_risk = self.feat[self.feat.get("risk_level", pd.Series()) == "high"]
        if high_risk.empty:
            return []
        pct = round(len(high_risk) / len(self.feat) * 100, 1)
        return [Insight(
            category="risk",
            severity="critical" if pct > 30 else "warning",
            title="High abandonment risk detected",
            description=(
                f"{len(high_risk)} users ({pct}% of total) show a high probability "
                "of abandoning simulations. Immediate retention action recommended."
            ),
            affected_users=high_risk.index.tolist(),
            metric=pct,
            metric_label="% high-risk users",
        )]

    def _high_performers(self) -> List[Insight]:
        top = self.feat[self.feat.get("segment_label", pd.Series()) == "high_performer"]
        if top.empty:
            return []
        avg_rate = round(top["completion_rate"].mean() * 100, 1)
        return [Insight(
            category="engagement",
            severity="info",
            title="High-performer segment identified",
            description=(
                f"{len(top)} users classified as high performers with an average "
                f"completion rate of {avg_rate}%. Good candidates for advanced content."
            ),
            affected_users=top.index.tolist(),
            metric=avg_rate,
            metric_label="avg completion rate %",
        )]

    def _low_engagement(self) -> List[Insight]:
        low = self.feat[self.feat.get("n_logins", 0) <= 1]
        if low.empty:
            return []
        pct = round(len(low) / len(self.feat) * 100, 1)
        return [Insight(
            category="engagement",
            severity="warning",
            title="Low-engagement users",
            description=(
                f"{len(low)} users ({pct}%) have only 1 or fewer login events. "
                "Re-engagement campaign or onboarding review suggested."
            ),
            affected_users=low.index.tolist(),
            metric=pct,
            metric_label="% low-engagement users",
        )]

    def _product_popularity(self) -> List[Insight]:
        if "producto_id" not in self.feat.columns:
            return []
        popular = self.feat["producto_id"].value_counts().idxmax()
        count = self.feat["producto_id"].value_counts().max()
        name = self.productos.set_index("producto_id")["nombre"].get(popular, str(popular))
        return [Insight(
            category="product",
            severity="info",
            title="Most popular simulation identified",
            description=(
                f'Product "{name}" (ID {popular}) is the most interacted with, '
                f"appearing in {count} interactions."
            ),
            metric=float(count),
            metric_label="interactions",
        )]

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
