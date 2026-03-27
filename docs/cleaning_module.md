# Cleaning Module Documentation

This directory contains documentation and guidelines for the cleaning (limpieza) module.

## Structure
- `csv.py` and `sql.py`: Main cleaning logic for tabular data.
- `etl_orchestrator.py`: Orchestrates the ETL flow for tabular data.
- Only keep what is strictly necessary for the hackathon.

## How to extend
- To add new cleaning steps, create a new class in `csv.py` and add it to the pipeline.
- For new data sources, add a new file and update the orchestrator.

## Notes
- Image and PDF cleaning are not included by default. Add them only if required by the challenge.
- Keep all code and documentation in English for consistency.
