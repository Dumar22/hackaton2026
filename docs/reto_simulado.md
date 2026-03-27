# Reto Simulado Hackathon 2026

## Enunciado
CloudLabs Learning te entrega una base de datos con registros de uso de su plataforma educativa. El objetivo es diseñar una solución que convierta el comportamiento digital de los usuarios en recomendaciones accionables para el negocio, más allá de simples dashboards.

## Objetivo
- Analizar los datos de uso y proponer insights que ayuden a mejorar la retención, el engagement y la conversión de usuarios.
- Presentar los resultados de forma clara, preferiblemente mediante una interfaz conversacional o un reporte automatizado.

## Data de ejemplo (CSV)

**usuarios.csv**
usuario_id,edad,genero,ciudad,fecha_registro
1,22,M,Bogotá,2025-09-01
2,19,F,Medellín,2025-10-15
3,25,M,Cali,2025-11-20

**eventos.csv**
usuario_id,fecha_evento,tipo_evento,detalle
1,2026-03-01,login,web
1,2026-03-01,simulacion,inicio
1,2026-03-01,simulacion,fin
2,2026-03-02,login,mobile
2,2026-03-02,simulacion,inicio
3,2026-03-03,login,web

**productos.csv**
producto_id,nombre,categoria
101,Simulación Física,STEM
102,Simulación Química,STEM

**interacciones.csv**
usuario_id,producto_id,fecha,accion
1,101,2026-03-01,completado
2,102,2026-03-02,abandonado
3,101,2026-03-03,completado

## Palabras clave y consideraciones
- engagement, retención, conversión, cohortes, segmentación, churn, recomendación, personalización, insights, automatización, experiencia conversacional, limpieza de datos, reproducibilidad, trazabilidad, métricas de negocio, adaptabilidad.

## Qué tener en cuenta
- El formato y columnas pueden variar el día del reto, por lo que tu código debe ser flexible (usar pandas, validaciones dinámicas, manejo de columnas desconocidas).
- Prepara funciones para análisis exploratorio, generación de cohortes, cálculo de métricas clave y generación de recomendaciones.
- Documenta bien el código y permite cambiar rutas de archivos fácilmente.
- Prepara scripts/notebooks para depuración y pruebas rápidas.

---

Puedes usar estos archivos CSV de ejemplo para simular la carga y análisis de datos antes del evento real.