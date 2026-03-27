"""
Adaptive data loader – supports CSV, Excel, JSON, Parquet and plain text.
"""
import os
import pandas as pd
from typing import Optional, Dict
import re


def load_file(path: str) -> pd.DataFrame:
    """Loads a file into a DataFrame based on its extension."""
    ext = os.path.splitext(path)[1].lower()
    loaders = {
        ".csv": pd.read_csv,
        ".txt": pd.read_csv,
        ".xlsx": pd.read_excel,
        ".xls": pd.read_excel,
        ".json": pd.read_json,
        ".parquet": pd.read_parquet,
    }
    loader = loaders.get(ext, pd.read_table)
    try:
        df = loader(path)
        print(f"Loaded: {os.path.basename(path)} → {df.shape[0]} rows, {df.shape[1]} cols")
        return df
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return pd.DataFrame()


def export_to_json(df: pd.DataFrame, path: str) -> None:
    """Exports a DataFrame to a JSON file."""
    try:
        df.to_json(path, orient="records", force_ascii=False, indent=2)
        print(f"Exported to JSON: {path}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}")


def load_and_process(path: str, name: Optional[str] = None, export_json: bool = False) -> pd.DataFrame:
    """Loads a file, prints a field summary, and optionally exports to JSON."""
    df = load_file(path)
    if df.empty:
        print(f"Could not load {name or path}")
        return df

    label = name or os.path.basename(path)
    print(f"\n--- {label} ---")
    print(f"Columns: {list(df.columns)}")
    print(f"Nulls:\n{df.isnull().sum()}")
    print(f"Dtypes:\n{df.dtypes}")
    print(df.head(3))

    if export_json:
        json_path = os.path.splitext(path)[0] + ".json"
        export_to_json(df, json_path)

    return df

def dynamic_column_mapping(df: pd.DataFrame, expected_types: Dict[str, str]) -> pd.DataFrame:
    """
    Attempts to map the current dataframe columns to expected names 
    by searching for keywords in column headers.
    
    Example: 'user_id', 'usuario', 'Cod_Estudiante' -> 'usuario_id'
    """
    if df.empty: return df
    
    mappings = {
        "usuario_id": ["user", "usuario", "id", "cod", "estudiante", "persona"],
        "edad": ["edad", "age", "years"],
        "genero": ["genero", "gender", "sex"],
        "ciudad": ["ciudad", "city", "location", "ubica"],
        "fecha": ["fecha", "date", "time", "created"],
        "tipo_evento": ["evento", "event", "type", "accion", "tipo"]
    }
    
    new_cols = {}
    current_cols = [c.lower() for c in df.columns]
    
    for expected, keywords in mappings.items():
        for i, col in enumerate(current_cols):
            if any(key in col for key in keywords):
                new_cols[df.columns[i]] = expected
                break # Found the first match
                
    if new_cols:
        print(f"🔄 Mapeo dinámico aplicado: {new_cols}")
        return df.rename(columns=new_cols)
        
    return df
