#!/usr/bin/env python
"""
Script de ejemplo: Generar datos, clasificarlos y analizarlos
Demuestra el flujo completo de la solución
"""
import asyncio
import json
from app.data_processing import (
    DataGenerator,
    DataExporter,
    PatternAnalyzer,
    ProcessClassifier
)

async def main():
    """Ejecuta el flujo completo"""
    
    print("=" * 80)
    print("SOLUCIÓN DE ANÁLISIS DE PATRONES Y AUTOMATIZACIÓN DE PROCESOS")
    print("=" * 80)
    
    # 1. GENERAR DATOS
    print("\n1. GENERANDO DATOS (5000 registros, 10 columnas)...")
    print("-" * 80)
    
    generator = DataGenerator(rows=5000)
    data = generator.get_data()
    headers = generator.get_headers()
    stats = generator.get_stats()
    
    print(f"✓ Datos generados: {len(data)} registros")
    print(f"✓ Columnas: {', '.join(headers)}")
    print(f"\nEstadísticas:")
    print(f"  - Monto total de ventas: ${stats['monto_total_venta']:,.2f}")
    print(f"  - Monto promedio por pedido: ${stats['monto_promedio']:.2f}")
    print(f"  - Cantidad promedio por pedido: {stats['cantidad_promedio']:.1f} unidades")
    print(f"  - Descuento total aplicado: ${stats['descuento_total']:.2f}")
    
    print(f"\nDistribución por estado:")
    for estado, cantidad in stats['cantidad_por_estado'].items():
        pct = (cantidad / len(data)) * 100
        print(f"  - {estado}: {cantidad} ({pct:.1f}%)")
    
    # 2. CLASIFICAR PROCESOS
    print("\n2. CLASIFICANDO PROCESOS POR PRIORIDAD...")
    print("-" * 80)
    
    classifier = ProcessClassifier()
    classified = classifier.classify_all(data)
    metrics = classifier.get_metrics()
    workflow = classifier.generate_workflow(classified)
    
    print(f"✓ Registros clasificados:\n")
    print(f"  - Urgentes: {len(classified['urgentes'])} registros ({metrics['distribucion']['urgentes_pct']:.1f}%)")
    print(f"  - Alta Prioridad: {len(classified['alta_prioridad'])} registros ({metrics['distribucion']['alta_prioridad_pct']:.1f}%)")
    print(f"  - Media Prioridad: {len(classified['media_prioridad'])} registros ({metrics['distribucion']['media_prioridad_pct']:.1f}%)")
    print(f"  - Baja Prioridad: {len(classified['baja_prioridad'])} registros ({metrics['distribucion']['baja_prioridad_pct']:.1f}%)")
    
    print(f"\n✓ Análisis de Automatización:")
    print(f"  - Procesos Automatizables: {metrics['automatizacion']['automatizable_total']} ({metrics['automatizacion']['automatizable_pct']:.1f}%)")
    print(f"  - Ahorro de tiempo: {metrics['automatizacion']['ahorro_tiempo_horas']:.1f} horas")
    
    print(f"\n✓ Anomalías Detectadas: {metrics['anomalias']['detectadas']} ({metrics['anomalias']['porcentaje']:.1f}%)")
    
    # 3. MOSTRAR FLUJO DE TRABAJO
    print("\n3. FLUJO DE TRABAJO RECOMENDADO:")
    print("-" * 80)
    
    for fase, info in workflow.items():
        print(f"\n{info['nombre']}")
        print(f"  Registros: {info['cantidad']}")
        print(f"  Tiempo estimado: {info['tiempo_estimado']}")
        print(f"  Acciones:")
        for accion in info['acciones']:
            print(f"    • {accion}")
    
    # 4. EXPORTAR DATOS
    print("\n4. EXPORTANDO DATOS A MÚLTIPLES FORMATOS...")
    print("-" * 80)
    
    exporter = DataExporter(data, headers)
    results = exporter.export_all(output_dir="./exports")
    
    for fmt, result in results.items():
        if 'error' in fmt:
            print(f"  ✗ {fmt}: {result}")
        elif 'warning' in fmt:
            print(f"  ⚠ {fmt}: {result}")
        else:
            print(f"  ✓ {fmt.upper()}: {result}")
    
    # 5. MOSTRAR EJEMPLOS
    print("\n5. EJEMPLOS DE REGISTROS POR CATEGORÍA:")
    print("-" * 80)
    
    print("\n📍 EJEMPLO - Registro URGENTE (requiere atención inmediata):")
    if classified['urgentes']:
        urgent = classified['urgentes'][0]
        print(f"  ID: {urgent['id']}")
        print(f"  Cliente: {urgent['tipo_cliente']}")
        print(f"  Monto: ${urgent['monto_total']}")
        print(f"  Estado: {urgent['estado_pedido']}")
        print(f"  Razón: Monto elevado O Cliente VIP/Premium")
    
    print("\n🤖 EJEMPLO - Registro AUTOMATIZABLE (procesamiento automático):")
    if classified['automatizable']:
        auto = classified['automatizable'][0]
        print(f"  ID: {auto['id']}")
        print(f"  Cliente: {auto['tipo_cliente']}")
        print(f"  Método Pago: {auto['metodo_pago']}")
        print(f"  Estado: {auto['estado_pedido']}")
        print(f"  Acción Automática: Generar factura + Actualizar inventario + Enviar confirmación")
    
    print("\n⚠️  EJEMPLO - Registro con ANOMALÍA (requiere revisión):")
    if classified['anomalias']:
        anomaly = classified['anomalias'][0]
        print(f"  ID: {anomaly['id']}")
        print(f"  Cantidad: {anomaly['cantidad']} unidades")
        print(f"  Descuento: ${anomaly['monto_descuento']}")
        print(f"  Monto: ${anomaly['monto_total']}")
        print(f"  Razón: Cantidad inusualmente alta O descuento elevado")
    
    print("\n" + "=" * 80)
    print("EJEMPLO COMPLETADO EXITOSAMENTE")
    print("=" * 80)
    
    # 6. Mostrar instrucciones de API
    print("\n6. CÓMO USAR A TRAVÉS DE LA API REST:")
    print("-" * 80)
    print("""
# 1. Generar datos
curl -X POST "http://localhost:8000/api/v1/data/generate" \\
  -d "rows=5000&export_formats=csv&export_formats=json"

# 2. Clasificar procesos (sustituir CACHE_KEY)
curl -X POST "http://localhost:8000/api/v1/data/classify" \\
  -d "cache_key=CACHE_KEY"

# 3. Analizar patrones con IA (sustituir CACHE_KEY)
curl -X POST "http://localhost:8000/api/v1/data/analyze" \\
  -d "cache_key=CACHE_KEY&model=gpt"

# 4. Subir archivo CSV y analizarlo
curl -X POST "http://localhost:8000/api/v1/data/analyze-file" \\
  -F "file=@tu_archivo.csv" \\
  -d "model=gpt"
    """)
    
    print("\n✨ Los datos se han guardado en la carpeta ./exports/")
    print("📊 Puedes revisar los archivos generados: CSV, JSON, SQL, Excel, PDF")

if __name__ == "__main__":
    asyncio.run(main())
