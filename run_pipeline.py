"""
run_pipeline.py – CLI entry point for the full data intelligence pipeline.

Usage:
    python run_pipeline.py
    python run_pipeline.py --data-dir app/data
"""
import argparse
import json
from pathlib import Path

from app.core.config import settings
from app.pipeline import DataPipeline


def main():
    parser = argparse.ArgumentParser(description="Hackathon 2026 – Run the full AI pipeline")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=settings.DATA_DIR,
        help="Path to the directory containing the CSV data files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to save the pipeline result as JSON.",
    )
    args = parser.parse_args()

    pipeline = DataPipeline(data_dir=args.data_dir)
    result = pipeline.run()

    print(f"\n⏱  Duration: {result.duration_ms} ms")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result.stages, f, ensure_ascii=False, indent=2, default=str)
        print(f"📄 Result saved to: {args.output}")

    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
