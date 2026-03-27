import pandas as pd
import os
import json
from typing import Optional

# Importamos las clases de nuestra arquitectura SOLID
from cleaners import CSVCleaner, ExcelCleaner, PDFCleaner

def get_cleaner(path: str):
    """
    Patrón Factory simple: Retorna la instancia de limpiador correcta 
    según la extensión del archivo (Sigue el principio Abierto/Cerrado).
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.csv', '.txt']:
        return CSVCleaner()
    elif ext in ['.xlsx', '.xls']:
        return ExcelCleaner()
    elif ext == '.pdf':
        return PDFCleaner()
    else:
        print(f"Formato no implementado específicamente: {ext}. Usando CSVCleaner por defecto.")
        return CSVCleaner()

def exportar_a_json(df: pd.DataFrame, path: str):
    try:
        df.to_json(path, orient='records', force_ascii=False, indent=2)
        print(f"Exportado a JSON: {path}")
    except Exception as e:
        print(f"Error exportando a JSON: {e}")

def resumen_campos(df: pd.DataFrame, nombre: str):
    print(f"\n--- {nombre} ---")
    print(f"Columnas: {list(df.columns)}")
    print(f"Nulos por columna:\n{df.isnull().sum()}")
    print(f"Tipos de datos:\n{df.dtypes}")
    print(f"Primeras filas:\n{df.head(3)}")

def cargar_y_procesar(path: str, nombre: Optional[str] = None, exportar_json: bool = True):
    # Fase 1: Obtener la abstracción correcta
    cleaner = get_cleaner(path)
    
    # Fase 2: Lectura (cada cleaner sabe cómo leer su propio formato)
    df = cleaner.read_data(path)
    if df.empty:
        print(f"No se pudo cargar {nombre or path}")
        return df
        
    resumen_campos(df, f"ORIGINAL: {nombre or os.path.basename(path)}")
    
    # Fase 3: Canalización de limpieza (Pipeline) paso a paso
    # Esto sigue el contrato definido en BaseCleaner
    df = cleaner.remove_duplicates(df)
    df = cleaner.handle_missing_data(df)
    df = cleaner.remove_outliers(df)
    df = cleaner.correct_typos(df)
    df = cleaner.check_logical_integrity(df)
    df = cleaner.normalize_text(df)

    resumen_campos(df, f"LIMPIO: {nombre or os.path.basename(path)}")
    
    # Fase 4: Guardado / Exportado
    base_name = os.path.basename(path)
    output_full_path = os.path.join(os.path.dirname(path), f"limpio_{base_name}")
    
    # El cleaner guarda el archivo eficientemente en su formato
    cleaner.save_data(df, output_full_path)

    # Exportación estándar a JSON si se solicitó
    if exportar_json:
        json_path = os.path.splitext(path)[0] + '.json'
        exportar_a_json(df, json_path)
        
    return df

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    archivos = ['usuarios.csv', 'eventos.csv', 'productos.csv', 'interacciones.csv']
    for archivo in archivos:
        ruta = os.path.join(base_dir, archivo)
        # Solo procesar los archivos si existen para evitar un bloque de errores en consola
        if os.path.exists(ruta):
            cargar_y_procesar(ruta, nombre=archivo)
        else:
            print(f"Omitiendo {archivo}: Archivo no encontrado en ruta local.")
