# Hackathon 2026 – Data Intelligence API

> **Hackathon Talentotest 2026** – Universidad de Caldas · Universidad de Antioquia · Ubicua Technology · CloudLabs Learning

## Project Structure

```
Hack-2026/
├── app/                      # Main application package
│   ├── main.py               # ← FastAPI server entry point
│   ├── core/
│   │   └── config.py         # Environment settings (reads .env)
│   ├── data/                 # Sample CSV datasets
│   │   ├── usuarios.csv
│   │   ├── eventos.csv
│   │   ├── productos.csv
│   │   └── interacciones.csv
│   ├── cleaners/             # Data cleaning pipeline (SOLID)
│   │   ├── base_cleaner.py   # Abstract base with all cleaning steps
│   │   ├── csv_cleaner.py
│   │   ├── excel_cleaner.py
│   │   ├── pdf_cleaner.py
│   │   └── sql_cleaner.py
│   ├── analysis/             # Data analysis utilities
│   │   ├── exploratory.py    # Statistical summaries, correlations
│   │   └── adaptive.py       # Multi-format file loader
│   └── engine/               # AI decision pipeline
│       ├── models.py         # Base ML model interface
│       ├── insights.py       # Insight generator
│       ├── decisions.py      # Decision engine
│       └── actions.py        # Business action executor
├── docs/                     # Project documentation
│   ├── estrategias.md
│   ├── resumen.md
│   ├── reto_simulado.md
│   ├── diagramas.mmd
│   └── cleaning_module.md
├── .env                      # Environment variables (not committed)
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment
Copy `.env` and fill in your credentials:
```bash
cp .env .env.local   # Never commit real keys!
```

### 3. Run the server
```bash
uvicorn app.main:app --reload
```
API docs available at → **http://localhost:8000/docs**

## Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Health status |
| GET | `/data/summary` | Summary of built-in datasets |
| POST | `/clean/csv` | Upload & clean a CSV file |
| POST | `/clean/excel` | Upload & clean an Excel file |
| POST | `/analysis/explore` | Upload file & get exploratory analysis |

## Pipeline Flow

```
Raw Data → Cleaners → Analysis → Engine (Models → Insights → Decisions → Actions)
```
