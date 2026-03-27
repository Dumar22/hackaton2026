import pandas as pd
from .base_cleaner import BaseCleaner

class CSVCleaner(BaseCleaner):
    """
    Implementación concreta para la lectura y limpieza de archivos CSV.
    """
    def __init__(self, delimiter=',', encoding='utf-8'):
        self.delimiter = delimiter
        self.encoding = encoding

    def read_data(self, file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path, delimiter=self.delimiter, encoding=self.encoding)
        except Exception as e:
            print(f"Error cargando CSV en {file_path}: {e}")
            return pd.DataFrame()

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        try:
            df.to_csv(output_path, index=False, sep=self.delimiter, encoding=self.encoding)
            print(f"✅ Archivo CSV limpio guardado en: {output_path}")
        except Exception as e:
            print(f"Error guardando CSV: {e}")
