
# 🚀 Roadmap de Puesta en Marcha – Hack-2026

## 1. Preparar entorno

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Cargar datos reales

- Copia los archivos CSV/Excel reales en `app/data/`.
- Si los nombres cambian, ajusta el diccionario en `app/pipeline.py` (`_load_raw()`).

## 3. Adaptar columnas (si es necesario)

- Si los nombres de columnas cambian, edita el método `_build_features()` en `app/engine/models.py`.

## 4. Personalizar insights y acciones

- Agrega o ajusta métodos en `app/engine/insights.py` para nuevos hallazgos.
- Mapea nuevas acciones de negocio en `app/engine/decisions.py`.

## 5. Ejecutar pipeline y API

```bash
python run_pipeline.py
uvicorn app.main:app --reload --port 8000
# Docs interactivas: http://localhost:8000/docs
```

## 6. Endpoints principales

| Endpoint                | Descripción                        |
|-------------------------|------------------------------------|
| POST `/pipeline/run`    | Ejecuta el flujo completo          |
| GET `/pipeline/status`  | Estado de las etapas del pipeline  |
| GET `/data/summary`     | Resumen de los datasets cargados   |
| POST `/clean/csv`       | Limpia cualquier CSV subido        |
| POST `/analysis/explore`| Análisis exploratorio de archivos  |

## 7. Opcional: Base de datos

- No es obligatoria, pero puedes activar SQLite editando `.env` (`DATABASE_URL=sqlite:///./hackaton.db`).
- Solo necesario si el reto exige persistencia o histórico.

## 8. Estructura del proyecto

```
Hack-2026/
├── app/
│   ├── main.py              ← FastAPI
│   ├── pipeline.py          ← Orquestador
│   ├── core/config.py       ← Configuración
│   ├── data/                ← 📂 Datos reales
│   ├── cleaners/            ← Limpieza automática
│   ├── analysis/            ← Análisis exploratorio
│   └── engine/
│       ├── models.py        ← ⚠️ Adaptar columnas
│       ├── insights.py      ← ⚠️ Personalizar insights
│       ├── decisions.py     ← ⚠️ Reglas de negocio
│       └── actions.py       ← ⚠️ Acciones de negocio
├── run_pipeline.py          ← CLI de prueba rápida
├── .env                     ← Configuración
└── requirements.txt
```

---

Este documento resume el roadmap esencial para poner a funcionar el programa y adaptarlo rápidamente el día del reto. Elimina lo redundante y deja solo lo necesario para ejecución y adaptación.
