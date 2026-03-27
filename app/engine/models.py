"""
AI / ML models for the Hackathon 2026 pipeline.

Current models:
- UserSegmentationModel  : KMeans clustering to segment users by activity
- AbandonmentRiskModel   : Rule-based risk score for users who abandon simulations
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------
@dataclass
class ModelResult:
    model_name: str
    predictions: pd.Series
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class BaseModel:
    name: str = "base_model"

    def train(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> None:
        raise NotImplementedError

    def predict(self, X: pd.DataFrame) -> ModelResult:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Model 1: User Segmentation (unsupervised – KMeans)
# ---------------------------------------------------------------------------
class UserSegmentationModel(BaseModel):
    """
    Segments users into behavioural clusters based on:
      - Number of logins
      - Number of simulations started
      - Number of simulations completed
      - Completion rate
    Uses KMeans from sklearn (graceful fallback to rule-based if not installed).
    """

    name = "user_segmentation"

    def __init__(self, n_clusters: int = 3):
        self.n_clusters = n_clusters
        self._model: Any = None
        self._feature_cols: List[str] = []

    def _build_features(self, usuarios: pd.DataFrame, eventos: pd.DataFrame,
                         interacciones: pd.DataFrame) -> pd.DataFrame:
        """Builds a per-user feature matrix from the three datasets."""
        # --- Detect columns dynamically for robustness ---
        evt_col = "tipo_evento" if "tipo_evento" in eventos.columns else (eventos.columns[0] if not eventos.empty else "")
        act_col = "accion" if "accion" in interacciones.columns else (interacciones.columns[-1] if not interacciones.empty else "")
        
        # --- event counts per user ---
        login_counts = pd.Series(0, index=usuarios["usuario_id"].unique())
        if evt_col in eventos.columns:
            login_counts = (
                eventos[eventos[evt_col] == "login"]
                .groupby("usuario_id").size()
            )
            
        sim_start = pd.Series(0, index=usuarios["usuario_id"].unique())
        if evt_col in eventos.columns and "detalle" in eventos.columns:
            sim_start = (
                eventos[(eventos[evt_col] == "simulacion") & (eventos["detalle"] == "inicio")]
                .groupby("usuario_id").size()
            )

        # --- interaction outcomes ---
        completados = pd.Series(0, index=usuarios["usuario_id"].unique())
        if act_col in interacciones.columns:
            completados = (
                interacciones[interacciones[act_col] == "completado"]
                .groupby("usuario_id").size()
            )
            
        abandonados = pd.Series(0, index=usuarios["usuario_id"].unique())
        if act_col in interacciones.columns:
            abandonados = (
                interacciones[interacciones[act_col] == "abandonado"]
                .groupby("usuario_id").size()
            )

        feat = (
            usuarios[["usuario_id", "edad"]]
            .set_index("usuario_id")
            .join(login_counts.rename("n_logins"), how="left")
            .join(sim_start.rename("n_sim_start"), how="left")
            .join(completados.rename("n_completed"), how="left")
            .join(abandonados.rename("n_abandoned"), how="left")
            .fillna(0)
        )
        feat["completion_rate"] = feat["n_completed"] / (
            feat["n_completed"] + feat["n_abandoned"] + 1e-9
        )
        self._feature_cols = ["edad", "n_logins", "n_sim_start", "n_completed",
                               "n_abandoned", "completion_rate"]
        return feat

    def train(self, usuarios: pd.DataFrame, eventos: pd.DataFrame,  # type: ignore[override]
              interacciones: pd.DataFrame) -> pd.DataFrame:
        feat = self._build_features(usuarios, eventos, interacciones)
        X = feat[self._feature_cols].values

        try:
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            km = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
            km.fit(X_scaled)
            labels = km.labels_
            self._scaler = scaler
            self._model = km
        except ImportError:
            # Fallback: simple rule-based segmentation
            completion = feat["completion_rate"].values
            labels = np.where(completion >= 0.8, 0, np.where(completion >= 0.4, 1, 2))

        feat["segment"] = labels
        label_map = {0: "high_performer", 1: "moderate", 2: "at_risk"}
        feat["segment_label"] = feat["segment"].map(label_map)
        return feat

    def predict(self, X: pd.DataFrame) -> ModelResult:  # type: ignore[override]
        # For the pipeline we return the already-trained feature table
        return ModelResult(model_name=self.name, predictions=X.get("segment_label", pd.Series()))


# ---------------------------------------------------------------------------
# Model 2: Abandonment Risk (rule-based scoring)
# ---------------------------------------------------------------------------
class AbandonmentRiskModel(BaseModel):
    """
    Assigns each user a risk score [0-1] for dropping out of simulations.
    Higher = more likely to abandon.
    """

    name = "abandonment_risk"

    def train(self, feat: pd.DataFrame) -> pd.DataFrame:  # type: ignore[override]
        """Computes risk score from feature table produced by UserSegmentationModel."""
        risk = pd.Series(0.0, index=feat.index)

        # More abandonments relative to completions → higher risk
        abandon_ratio = feat["n_abandoned"] / (feat["n_completed"] + feat["n_abandoned"] + 1e-9)
        risk += abandon_ratio * 0.6

        # Low login count → lower engagement → higher risk
        max_logins = feat["n_logins"].max() or 1
        risk += (1 - feat["n_logins"] / max_logins) * 0.2

        # Low completion rate → higher risk
        risk += (1 - feat["completion_rate"]) * 0.2

        feat = feat.copy()
        feat["risk_score"] = risk.clip(0, 1).round(3)
        feat["risk_level"] = pd.cut(
            feat["risk_score"],
            bins=[0, 0.33, 0.66, 1.01],
            labels=["low", "medium", "high"],
            right=False,
        )
        return feat

    def predict(self, X: pd.DataFrame) -> ModelResult:  # type: ignore[override]
        return ModelResult(model_name=self.name, predictions=X.get("risk_level", pd.Series()))
