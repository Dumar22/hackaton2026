"""
Decision engine – maps insights to prioritised decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .insights import Insight


# Severity weights for priority sorting
_SEVERITY_WEIGHT = {"critical": 3, "warning": 2, "info": 1}


@dataclass
class Decision:
    priority: int          # 1 = highest
    trigger_insight: str   # title of the insight that caused this decision
    action_type: str       # "alert" | "campaign" | "recommend" | "monitor"
    description: str
    affected_users: List[int]


class DecisionEngine:
    """
    Converts a list of Insight objects into prioritised Decision objects.
    Each decision type maps to a concrete BusinessAction.
    """

    def __init__(self, insights: List[Insight]):
        self.insights = sorted(
            insights, key=lambda i: _SEVERITY_WEIGHT.get(i.severity, 0), reverse=True
        )

    def decide(self) -> List[Decision]:
        decisions: List[Decision] = []
        priority = 1

        for insight in self.insights:
            action_type, description = self._map_to_action(insight)
            decisions.append(Decision(
                priority=priority,
                trigger_insight=insight.title,
                action_type=action_type,
                description=description,
                affected_users=insight.affected_users,
            ))
            priority += 1

        return decisions

    # ------------------------------------------------------------------
    # Mapping rules
    # ------------------------------------------------------------------
    def _map_to_action(self, insight: Insight):
        if insight.category == "risk" and insight.severity in ("critical", "warning"):
            return (
                "alert",
                f"Send immediate re-engagement alert to {len(insight.affected_users)} at-risk users. "
                "Offer personalised support or easier entry-point simulations.",
            )
        if insight.category == "engagement" and "high_performer" in insight.title.lower():
            return (
                "recommend",
                "Recommend advanced or premium simulations to high-performer users. "
                "Consider badge/reward system to sustain motivation.",
            )
        if insight.category == "engagement" and "low-engagement" in insight.title.lower():
            return (
                "campaign",
                f"Launch re-engagement email/push campaign for {len(insight.affected_users)} "
                "low-activity users. Include a tutorial or guided first simulation.",
            )
        if insight.category == "product":
            return (
                "monitor",
                "Monitor the most popular simulation for quality and availability. "
                "Highlight it in the home screen to drive further completions.",
            )
        return ("monitor", f"Monitor: {insight.title}")

    def to_dict(self):
        return [
            {
                "priority": d.priority,
                "trigger_insight": d.trigger_insight,
                "action_type": d.action_type,
                "description": d.description,
                "affected_users_count": len(d.affected_users),
            }
            for d in self.decide()
        ]
