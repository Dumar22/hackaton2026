import pandas as pd
import os
import json
from typing import Optional

def cargar_archivo(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in ['.csv', '.txt']:
            return pd.read_csv(path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(path)
        elif ext == '.json':
            return pd.read_json(path)
        elif ext == '.parquet':
            return pd.read_parquet(path)
        else:
            print(f"Formato no soportado directamente: {ext}. Intentando leer como tabla...")
            return pd.read_table(path)
    except Exception as e:
        print(f"Error cargando {path}: {e}")
        return pd.DataFrame()

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

def limpiar_df(df: pd.DataFrame) -> pd.DataFrame:
    # Elimina duplicados y rellena nulos genéricamente
    df = df.drop_duplicates()
    for col in df.columns:
        if df[col].dtype == 'O':
            df[col] = df[col].fillna('Sin dato')
        else:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median() if df[col].notnull().any() else 0)
    return df

def cargar_y_procesar(path: str, nombre: Optional[str] = None, exportar_json: bool = True):
    df = cargar_archivo(path)
    if df.empty:
        print(f"No se pudo cargar {nombre or path}")
        return df
    resumen_campos(df, nombre or os.path.basename(path))
    df = limpiar_df(df)
    if exportar_json:
        json_path = os.path.splitext(path)[0] + '.json'
        exportar_a_json(df, json_path)
    return df

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    archivos = ['usuarios.csv', 'eventos.csv', 'productos.csv', 'interacciones.csv']
    for archivo in archivos:
        ruta = os.path.join(base_dir, archivo)
        cargar_y_procesar(ruta, nombre=archivo)
    # Puedes agregar aquí lógica para cargar otros formatos o rutas dinámicas
