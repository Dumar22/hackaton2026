# Detalles de Implementación: Pipeline A→G de Inteligencia Educativa

## 🎯 Objetivo Logrado
Construir una arquitectura de datos escalable, modular y basada en el paradigma **A→G**, capaz de procesar cientos de miles de registros de plataformas educativas (CloudLabs) en segundos y devolver no solo gráficas, sino **recomendaciones accionables para el negocio**.

---

## 🏛️ Decisiones Arquitecturales

### 1. Motor de Ingesta Adaptable (Fuzzy Mapping)
- **Problema:** En contextos reales (hackathons/clientes), los nombres de las columnas suelen variar (ej: `User_ID` vs `CC`).
- **Decisión:** Implementamos un motor de **Fuzzy Mapping** en `adaptive.py`. Este utiliza palabras clave con prioridades para renombrar columnas al vuelo, garantizando que el pipeline nunca se rompa y sea 100% agnóstico al archivo fuente.

### 2. Optimización para Grandes Volúmenes (Bulk Processing)
- **Problema:** SQLAlchemy puede ser lento al insertar millones de filas de forma individual.
- **Decisión:** Refactorizamos el flujo de guardado en `main.py` para usar **operaciones Bulk (`bulk_save_objects`)**. Esto permite procesar lotes masivos de objetos en un solo viaje a la base de datos PostgreSQL, eliminando los cuellos de botella de red e IO.

### 3. IA Generativa con Contexto de Datos (RAG Simplificado)
- **Problema:** Los chatbots genéricos no conocen la situación actual de los datos analizados.
- **Decisión:** Implementamos una arquitectura en `bot.py` que inyecta los resultados del pipeline (insights y decisiones) directamente en el prompt del sistema (OpenAI). Esto convierte al chat en un **Experto de Dominio** capaz de explicar los datos en lenguaje natural.

### 4. Segmentación Proactiva (KMeans)
- **Problema:** Saber "quién abandonó" no es suficiente para evitar el riesgo futuro.
- **Decisión:** Utilizamos **Clustering (KMeans)** en la etapa [D] para detectar patrones invisibles. Identificamos grupos de "Alto Riesgo" incluso antes de que dejen la plataforma, basándonos en su frecuencia de logins y éxito en simulaciones anteriores.

---

## 🛠️ Stack Tecnológico
- **Backend:** FastAPI (alto rendimiento, asíncrono).
- **Persistencia:** PostgreSQL + SQLAlchemy 2.0.
- **Análisis:** Pandas + Scikit-learn (procesamiento vectorizado).
- **IA:** OpenAI API (GPT-4o-mini).
- **Despliegue:** Docker Compose (aislamiento y reproducibilidad total).

## 🚀 Impacto de Negocio
- **Retención:** Detección temprana de churn en el Top 20% de usuarios en riesgo.
- **Valor al Usuario:** Rutas de aprendizaje personalizadas generadas por el `Recommender`.
- **Gobernanza:** Trazabilidad completa desde el dato crudo hasta la acción final guardada en BD.
