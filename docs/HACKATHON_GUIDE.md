# 🚀 Guía de Adaptación al Hackathon 2026

> **Para el equipo** – Este documento explica qué tenemos listo, qué puede cambiar el día del evento y cómo adaptar el proyecto en minutos a cualquier base de datos que nos entreguen.

---

## 📋 Contexto del Reto

El reto de CloudLabs Learning no es hacer dashboards. Es **convertir el comportamiento digital de usuarios en decisiones de negocio accionables**. Ej.:

- ¿Qué usuarios van a abandonar la plataforma? → acción de retención
- ¿Qué simulaciones generan más engagement? → recomendación de contenido
- ¿Qué segmento de usuarios tiene mayor potencial de conversión? → campaña dirigida

**La clave diferenciadora:** no solo analizar, sino que el sistema *decida qué hacer* con ese análisis.

---

## ✅ Lo que ya tenemos listo (ventaja del día 1)

### Pipeline completo A → G funcionando

```
A. Datos crudos       → app/data/          (cualquier CSV/Excel/JSON)
B. Limpieza           → app/cleaners/      (duplicados, nulos, outliers, typos)
C. Análisis exploratorio → app/analysis/   (estadísticas, correlaciones, nulos)
D. Modelos IA         → app/engine/models.py  (segmentación + riesgo de abandono)
E. Insights           → app/engine/insights.py (hallazgos categorizados)
F. Decisiones         → app/engine/decisions.py (reglas de negocio priorizadas)
G. Acciones           → app/engine/actions.py  (alertas, campañas, recomendaciones)
```

### API REST con FastAPI (ejecutable en el acto)
```bash
uvicorn app.main:app --reload
# → http://localhost:8000/docs  (Swagger interactivo)
```

| Endpoint | Qué hace |
|---|---|
| `POST /pipeline/run` | Ejecuta el flujo completo A→G |
| `GET  /pipeline/status` | Lista las etapas del pipeline |
| `GET  /data/summary` | Resumen de los datasets cargados |
| `POST /clean/csv` | Limpia cualquier CSV subido |
| `POST /clean/excel` | Limpia cualquier Excel subido |
| `POST /analysis/explore` | Análisis exploratorio de cualquier archivo |

### Limpieza automática (sin configuración)
Maneja automáticamente:
- ✅ Valores nulos (imputación por mediana/moda)
- ✅ Duplicados
- ✅ Outliers (IQR)
- ✅ Errores tipográficos (espacios, mayúsculas)
- ✅ Integridad lógica (edades, fechas)
- ✅ Normalización de texto

---

## 🔁 Cómo adaptar cuando llegan los datos reales

### Paso 1 – Reemplazar los CSVs (< 1 minuto)

Simplemente pega los archivos reales en `app/data/`. El pipeline los carga automáticamente si se llaman igual. Si los nombres cambian:

```python
# app/pipeline.py → método _load_raw()
files = {
    "usuarios":      "NUEVO_NOMBRE_USUARIOS.csv",   # ← cambiar aquí
    "eventos":       "NUEVO_NOMBRE_EVENTOS.csv",
    "productos":     "NUEVO_NOMBRE_PRODUCTOS.csv",
    "interacciones": "NUEVO_NOMBRE_INTERACCIONES.csv",
}
```

### Paso 2 – Adaptar las columnas del modelo (5-10 minutos)

Si las columnas cambian, ajusta el método `_build_features()` en `app/engine/models.py`:

```python
# Ejemplo: si en el reto real la columna se llama "user_id" en vez de "usuario_id"
usuarios[["user_id", "age"]]   # ajustar nombres de columnas
.set_index("user_id")
```

> **Tip:** El análisis exploratorio (`POST /analysis/explore`) te dice exactamente qué columnas tiene cada archivo al subirlo.

### Paso 3 – Ajustar los insights al dominio del reto (5-10 minutos)

Edita `app/engine/insights.py` → agrega métodos `_nombre_del_insight()` siguiendo el mismo patrón:

```python
def _nueva_metrica(self) -> List[Insight]:
    # tu lógica aquí
    return [Insight(
        category="retention",
        severity="critical",
        title="...",
        description="...",
        affected_users=[...],
    )]
```

### Paso 4 – Mapear nuevas acciones de negocio (2-5 minutos)

En `app/engine/decisions.py` → método `_map_to_action()`:

```python
if insight.category == "nueva_categoria":
    return ("campaign", "Descripción de la acción de negocio…")
```

---

## ❓ ¿Necesitamos base de datos?

### Respuesta corta: **No es obligatoria, pero sí agrega valor**

| Escenario | Recomendación |
|---|---|
| Hackathon corto (< 8h) | ❌ No la configures, usa solo CSVs. Perderás tiempo valioso. |
| Demo con persistencia o chat conversacional | ✅ Sí agrega SQLite (sin servidor, archivo local) |
| Datos muy grandes o varios archivos | ✅ Considera PostgreSQL o DuckDB |

### Opción recomendada si se necesita: SQLite (cero configuración)

```python
# En .env cambia:
DATABASE_URL=sqlite:///./hackaton.db   # ← ya está por defecto

# Para guardar resultados del pipeline:
# app/engine/actions.py → método _send_alert()
# → en vez de print(), insertar en tabla "action_logs"
```

**Cuándo activar la BD:**
- Si el reto pide histórico de ejecuciones
- Si construyes una interfaz conversacional que recuerde contexto
- Si necesitas cruzar múltiples corridas del pipeline

**Si decides activarla**, dime y creo el esquema completo (`app/db/`) en 10 minutos.

---

## 📊 ¿Qué nos falta para el día del reto?

### Listo ✅
- [x] Pipeline completo A→G funcional
- [x] Limpieza robusta multi-formato (CSV, Excel, PDF, SQL)
- [x] API REST documentada con Swagger
- [x] Modelos de segmentación y riesgo de abandono
- [x] Motor de insights + decisiones + acciones
- [x] Script CLI para pruebas rápidas (`python run_pipeline.py`)
- [x] Configuración por entorno (`.env`)

### Por hacer / mejorar 🔧

| Item | Prioridad | Tiempo estimado |
|---|---|---|
| **Interfaz conversacional** (chat que explique los insights) | 🔴 Alta | 1-2h |
| **Reporte PDF/HTML** con los resultados del pipeline | 🟡 Media | 30min |
| **Visualizaciones** (gráficas de segmentos, riesgo) | 🟡 Media | 1h |
| **Métricas de cohortes** (retención por semana/mes) | 🟡 Media | 30min |
| **Endpoint `/analyze/chat`** con OpenAI/Gemini | 🔴 Alta | 1h |
| **Base de datos** (si el reto lo pide) | 🟢 Baja | 30min |
| **Tests automáticos** (pytest) | 🟢 Baja | 45min |

### El diferenciador más importante 🏆

El reto dice explícitamente: **"no se trata de crear dashboards, sino de una experiencia conversacional"**.

El item más impactante sería un endpoint `/chat` donde el usuario pregunta en lenguaje natural y el sistema responde con insights del pipeline:

```
Usuario: "¿Cuál es el riesgo de abandono esta semana?"
Sistema: "3 de tus 7 usuarios activos muestran riesgo alto de 
          abandono. Los usuarios 1, 4 y 6 no han completado 
          ninguna simulación en 5 días. Se recomienda enviarles 
          un recordatorio personalizado."
```

Esto se puede hacer con **Gemini API** (ya tienes la clave en `.env`) + los resultados del pipeline como contexto.

---

## ⚡ Comandos rápidos para el día del reto

```bash
# 1. Activar entorno
source .venv/bin/activate

# 2. Pegar los CSVs reales en app/data/
# (reemplazar los de ejemplo)

# 3. Probar el pipeline inmediatamente
python run_pipeline.py

# 4. Levantar el servidor
uvicorn app.main:app --reload --port 8000

# 5. Ver docs interactivas
open http://localhost:8000/docs

# 6. Ejecutar pipeline completo vía API
curl -X POST http://localhost:8000/pipeline/run
```

---

## 🗂 Estructura del proyecto (referencia rápida)

```
Hack-2026/
├── app/
│   ├── main.py              ← FastAPI (uvicorn app.main:app --reload)
│   ├── pipeline.py          ← Orquestador A→G  ← AQUÍ EMPIEZA TODO
│   ├── core/config.py       ← Variables de entorno
│   ├── data/                ← 📂 REEMPLAZAR CON DATOS REALES DEL RETO
│   ├── cleaners/            ← Limpieza (no tocar, funciona solo)
│   ├── analysis/            ← EDA genérico (no tocar)
│   └── engine/
│       ├── models.py        ← ⚠️ Adaptar columnas si cambian
│       ├── insights.py      ← ⚠️ Agregar insights del dominio real
│       ├── decisions.py     ← ⚠️ Adaptar reglas de negocio
│       └── actions.py       ← ⚠️ Conectar con canales reales (email, notif.)
├── docs/                    ← Documentación del equipo
├── run_pipeline.py          ← CLI de prueba rápida
├── .env                     ← API keys y configuración
└── requirements.txt
```

> Los módulos marcados con ⚠️ son los únicos que deben adaptarse al reto. Los demás son genéricos y reutilizables.
