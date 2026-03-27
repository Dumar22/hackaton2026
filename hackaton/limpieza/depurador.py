# Orquestador del flujo ETL completo para limpieza y análisis

from .csv import limpiar_csv
from .pdf import limpiar_pdf
from .image import limpiar_imagen

# TODO: Integrar Unstract, embeddings y análisis

def ejecutar_flujo(tipo_archivo, ruta_archivo):
    if tipo_archivo == 'csv':
        return limpiar_csv(ruta_archivo)
    elif tipo_archivo == 'pdf':
        return limpiar_pdf(ruta_archivo)
    elif tipo_archivo == 'imagen':
        return limpiar_imagen(ruta_archivo)
    else:
        raise ValueError('Tipo de archivo no soportado')
