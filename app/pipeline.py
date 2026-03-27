"""
pipeline.py – Full data intelligence pipeline orchestrator.

Flow (matches the Hackathon 2026 diagram):
  A. Raw Data
     ↓
  B. Cleaning & Validation      (app.cleaners)
     ↓
  C. Exploratory Analysis       (app.analysis.exploratory)
     ↓
  D. AI / Algorithm             (app.engine.models)
     ↓
  E. Insight Generation         (app.engine.insights)
     ↓
  F. Decision Making            (app.engine.decisions)
     ↓
  G. Business Action            (app.engine.actions)
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from app.cleaners.base_cleaner import BaseCleaner
from app.cleaners.csv_cleaner import CSVCleaner
from app.analysis.exploratory import ExploratoryAnalysis
from app.engine.models import UserSegmentationModel, AbandonmentRiskModel
from app.engine.insights import InsightsGenerator
from app.engine.decisions import DecisionEngine
from app.engine.actions import BusinessAction
from app.analysis.adaptive import dynamic_column_mapping


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------
@dataclass
class PipelineResult:
    duration_ms: float = 0.0
    stages: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
class DataPipeline:
    """
    Orchestrates all 7 stages of the data intelligence flow.
    Can be used from the CLI (run_pipeline.py) or via the FastAPI endpoint.
    """

    def __init__(self, data_dir: Path, cleaner: Optional[BaseCleaner] = None):
        self.data_dir = data_dir
        self.cleaner = cleaner or CSVCleaner()

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------
    def run(self) -> PipelineResult:
        result = PipelineResult()
        t0 = time.perf_counter()

        try:
            # ── A. Raw Data ──────────────────────────────────────────────
            print("\n" + "═" * 60)
            print("  HACKATHON 2026 – DATA INTELLIGENCE PIPELINE")
            print("═" * 60)
            print("\n[A] Loading raw data…")
            raw = self._load_raw()
            result.stages["A_raw_data"] = {
                "files_loaded": list(raw.keys()),
                "total_raw_rows": {k: len(v) for k, v in raw.items()},
            }

            # ── B. Cleaning & Validation ─────────────────────────────────
            print("[B] Cleaning & validation…")
            clean = self._clean(raw)
            result.stages["B_cleaning"] = {
                "rows_after_cleaning": {k: len(v) for k, v in clean.items()},
                "rows_removed": {
                    k: raw[k].shape[0] - clean[k].shape[0] for k in raw
                },
            }

            # ── C. Exploratory Analysis ──────────────────────────────────
            print("[C] Exploratory analysis…")
            eda = self._explore(clean)
            result.stages["C_exploratory"] = eda

            # ── D. AI / Algorithm ────────────────────────────────────────
            print("[D] Running AI models…")
            feat = self._model(clean)
            result.stages["D_model"] = {
                "segment_distribution": feat["segment_label"].value_counts().to_dict()
                if "segment_label" in feat.columns else {},
                "avg_risk_score": round(feat["risk_score"].mean(), 3)
                if "risk_score" in feat.columns else None,
                "users_analysed": len(feat),
            }

            # ── E. Insight Generation ────────────────────────────────────
            print("[E] Generating insights…")
            insights_gen = InsightsGenerator(feat, clean["productos"])
            insights = insights_gen.generate()
            result.stages["E_insights"] = {
                "total_insights": len(insights),
                "insights": insights_gen.to_dict(),
            }

            # ── F. Decision Making ───────────────────────────────────────
            print("[F] Making decisions…")
            decision_engine = DecisionEngine(insights)
            decisions = decision_engine.decide()
            result.stages["F_decisions"] = {
                "total_decisions": len(decisions),
                "decisions": decision_engine.to_dict(),
            }

            # ── G. Business Action ───────────────────────────────────────
            print("[G] Executing business actions…")
            action_executor = BusinessAction(decisions)
            logs = action_executor.execute_all()
            result.stages["G_actions"] = {
                "total_actions": len(logs),
                "actions": action_executor.to_dict(),
            }

            print("\n" + "═" * 60)
            print("  ✅ Pipeline completed successfully")
            print("═" * 60)

        except Exception as exc:
            result.success = False
            result.error = str(exc)
            print(f"\n❌ Pipeline failed: {exc}")
            raise

        finally:
            result.duration_ms = round((time.perf_counter() - t0) * 1000, 2)

        return result

    # ------------------------------------------------------------------
    # Stage implementations
    # ------------------------------------------------------------------
    def _load_raw(self) -> Dict[str, pd.DataFrame]:
        files = {
            "usuarios": "usuarios.csv",
            "eventos": "eventos.csv",
            "productos": "productos.csv",
            "interacciones": "interacciones.csv",
        }
        data = {}
        for name, fname in files.items():
            path = self.data_dir / fname
            if not path.exists():
                # Búsqueda flexible de archivos por patrón en caso de que el nombre cambie un poco
                found_files = list(self.data_dir.glob(f"*{name}*.csv"))
                if found_files:
                    path = found_files[0]
                    print(f"   ⚠️ Archivo exacto no hallado, cargando alternativo: {path.name}")
                else:
                    raise FileNotFoundError(f"Data file not found: {path} (ni patrones parecidos)")
            
            df = pd.read_csv(path)
            
            # Aplicar MAPEO DINAMICO DE COLUMNAS (Punto 2 y 3 del Stage 1)
            # Esto corrige 'User_ID' -> 'usuario_id', etc.
            df = dynamic_column_mapping(df, {})
            
            print(f"   ↳ {path.name}: {df.shape[0]} rows × {df.shape[1]} cols")
            data[name] = df
        return data

    def _clean(self, raw: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        cleaned = {}
        for name, df in raw.items():
            before = df.shape[0]
            df_c = self.cleaner.remove_duplicates(df)
            df_c = self.cleaner.handle_missing_data(df_c)
            df_c = self.cleaner.remove_outliers(df_c)
            df_c = self.cleaner.correct_typos(df_c)
            df_c = self.cleaner.check_logical_integrity(df_c)
            df_c = self.cleaner.normalize_text(df_c)
            after = df_c.shape[0]
            print(f"   ↳ {name}: {before} → {after} rows (removed {before - after})")
            cleaned[name] = df_c
        return cleaned

    def _explore(self, clean: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        summary = {}
        for name, df in clean.items():
            analyst = ExploratoryAnalysis(df)
            missing = analyst.missing_report()
            summary[name] = {
                "shape": list(df.shape),
                "missing_fields": missing.to_dict() if not missing.empty else {},
                "dtypes": df.dtypes.astype(str).to_dict(),
            }
            print(f"   ↳ {name}: {df.shape[0]} rows, "
                  f"{int(missing['missing_count'].sum()) if not missing.empty else 0} missing vals")
        return summary

    def _model(self, clean: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        seg_model = UserSegmentationModel(n_clusters=3)
        feat = seg_model.train(
            clean["usuarios"],
            clean["eventos"],
            clean["interacciones"],
        )
        print(f"   ↳ Segmentation: {feat['segment_label'].value_counts().to_dict()}")

        risk_model = AbandonmentRiskModel()
        feat = risk_model.train(feat)
        avg_risk = feat["risk_score"].mean()
        print(f"   ↳ Avg risk score: {avg_risk:.3f}")

        return feat
