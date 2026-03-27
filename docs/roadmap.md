 Fase 0: Preparación (T-menos 30 min)
Antes de que entreguen los datos reales.

Levantar el entorno: docker compose up --build -d
Verificar API: Entra a http://localhost:8000/docs para ver que todo esté verde.
Verificar Dashboard: Entra a http://localhost:8000 para tener la interfaz lista.
🚀 Fase 1: [A] Datos Crudos e Ingesta
Cuando el jurado entrega los archivos (CSV/Excel).

Carga: Copia los archivos reales a app/data/.
Mapeo Inteligente: Si los nombres de columnas son distintos a nuestros ejemplos (ej: "ID_Estudiante" en vez de "usuario_id"), abre app/analysis/adaptive.py y añade el nuevo nombre al diccionario mappings.
Verificación: Ejecuta el endpoint GET /data/summary para confirmar que el sistema "ve" los datos reales.
🧹 Fase 2: [B] Limpieza y Validación (SOLID)
Garantizar la calidad de la información.

Ejecución: Corre el pipeline desde el Dashboard o mediante POST /pipeline/run.
Transparencia: Abre Adminer (http://localhost:8080) y revisa las tablas cleaned_users, cleaned_events, etc.
Auditoría: Verifica si el sistema eliminó duplicados o corrigió nulos. Si hay errores lógicos nuevos (ej: notas negativas), ajusta el BaseCleaner en app/cleaners/base_cleaner.py.
📈 Fase 3: [C] Análisis Exploratorio (EDA)
Entender qué nos dicen los números antes de la IA.

Estadísticas: Revisa el endpoint POST /analysis/explore con los archivos nuevos.
Hallazgos: Mira las correlaciones. ¿Hay alguna materia donde todos los estudiantes abandonen? (Esto te servirá para tu pitch).
Visualización: Usa el Dashboard para ver el resumen rápido de nulos y tipos de datos.
🤖 Fase 4: [D] Modelo IA / Algoritmo
Segmentación y Predicción.

Entrenamiento: El sistema ejecutará KMeans automáticamente sobre los nuevos datos.
Ajuste de Atributos: Si los datos nuevos tienen columnas geniales como "Sueldo" o "Promedio Académico", añádelas al modelo en el método _build_features de app/engine/models.py para que la segmentación sea más precisa.
Riesgo: Verifica el avg_risk_score global. ¿Es alto (> 0.6) o bajo?
💡 Fase 5: [E] Generación de Insights
Convertir datos en hallazgos narrativos.

Revisión: Mira la sección de "Insights" del Dashboard.
Personalización: Si descubres un patrón nuevo (ej: "Los estudiantes de la ciudad X tienen 50% más éxito"), añade una regla rápida en app/engine/insights.py.
Diferencial: Asegúrate de que los insights mencionen la retención y el engagement (las palabras clave del reto).
⚖️ Fase 6: [F] Toma de Decisiones
Priorización estratégica.

Asignación: Mira cómo el sistema mapea insights a acciones en app/engine/decisions.py.
Prioridad: Asegúrate de que las acciones de "Riesgo Alto" tengan la prioridad 1 (Crítica).
🎯 Fase 7: [G] Acción de Negocio
El valor real para CloudLabs.

Ejecución Simulada: Muestra los logs de acciones en el Dashboard.
El "Wow" Factor (Chat): Abre el Chat de IA y pregunta: "Tengo 100 estudiantes en riesgo, ¿qué tres acciones de negocio debo ejecutar YA para salvar su semestre?". Deja que el bot use los resultados del pipeline para responder.
Demo Final: Muestra cómo el sistema detectó un problema crudo (A) y terminó en una acción concreta (G).
🚩 Checklist de Entrega Final para el Jurado
 Docker corriendo: (Indica que es auto-gestionado).
 Adminer abierto: (Muestra las tablas limpias para probar transparencia).
 Dashboard con datos reales: (Visualización impecable).
 Módulo de recomendaciones: (Muestra el valor al estudiante).
 Pitch de 3 min: (Practicado y con seguridad).
Ventaja estratégica: Mientras otros equipos estén peleando con Pandas para limpiar sus primeros datos, tú ya habrás pasado por las fases A, B y C en los primeros 10 minutos. ¡Tu ventaja competitiva es el tiempo!

He guardado esta hoja de ruta en docs/ROADMAP_HACKATHON.md para que la tengas a mano. ¿Quieres que te explique cómo ajustar el modelo de IA rápidamente si te dan datos muy diferentes a los esperados?