"""
Business actions – executes concrete actions for each decision.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List

from .decisions import Decision


@dataclass
class ActionLog:
    timestamp: str
    action_type: str
    decision_priority: int
    status: str           # "executed" | "simulated" | "failed"
    summary: str
    details: Dict[str, Any] = field(default_factory=dict)


class BusinessAction:
    """
    Executes the business action that corresponds to each Decision.
    In production, plug in real notification / CRM / logging systems here.
    """

    def __init__(self, decisions: List[Decision]):
        self.decisions = decisions
        self.log: List[ActionLog] = []

    def execute_all(self) -> List[ActionLog]:
        for decision in self.decisions:
            handler = {
                "alert": self._send_alert,
                "campaign": self._launch_campaign,
                "recommend": self._push_recommendation,
                "monitor": self._create_monitor_task,
            }.get(decision.action_type, self._default_action)

            entry = handler(decision)
            self.log.append(entry)

        return self.log

    # ------------------------------------------------------------------
    # Handlers (simulated – replace with real integrations)
    # ------------------------------------------------------------------
    def _send_alert(self, d: Decision) -> ActionLog:
        users = d.affected_users or []
        print(f"  🚨 [ALERT] Sending alert to {len(users)} users → {d.description[:60]}…")
        return self._make_log(d, "simulated", f"Alert queued for {len(users)} users.")

    def _launch_campaign(self, d: Decision) -> ActionLog:
        users = d.affected_users or []
        print(f"  📣 [CAMPAIGN] Launching campaign for {len(users)} users → {d.description[:60]}…")
        return self._make_log(d, "simulated", f"Campaign scheduled for {len(users)} users.")

    def _push_recommendation(self, d: Decision) -> ActionLog:
        users = d.affected_users or []
        print(f"  💡 [RECOMMEND] Pushing recommendations to {len(users)} users → {d.description[:60]}…")
        return self._make_log(d, "simulated", f"Recommendations prepared for {len(users)} users.")

    def _create_monitor_task(self, d: Decision) -> ActionLog:
        print(f"  📊 [MONITOR] Monitor task created → {d.description[:60]}…")
        return self._make_log(d, "simulated", "Monitor task added to dashboard.")

    def _default_action(self, d: Decision) -> ActionLog:
        print(f"  ℹ️  [INFO] {d.description[:60]}…")
        return self._make_log(d, "simulated", "Logged.")

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    @staticmethod
    def _make_log(d: Decision, status: str, summary: str) -> ActionLog:
        return ActionLog(
            timestamp=datetime.now(timezone.utc).isoformat(),
            action_type=d.action_type,
            decision_priority=d.priority,
            status=status,
            summary=summary,
            details={"trigger": d.trigger_insight, "description": d.description},
        )

    def to_dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "timestamp": e.timestamp,
                "action_type": e.action_type,
                "priority": e.decision_priority,
                "status": e.status,
                "summary": e.summary,
            }
            for e in self.log
        ]
