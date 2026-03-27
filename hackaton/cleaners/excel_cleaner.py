import pandas as pd
from .base_cleaner import BaseCleaner

class ExcelCleaner(BaseCleaner):
    """
    Implementación concreta para la lectura y limpieza de archivos Excel (.xlsx/.xls).
    """
    def __init__(self, sheet_name=0):
        self.sheet_name = sheet_name

    def read_data(self, file_path: str) -> pd.DataFrame:
        try:
            # Requiere openpyxl para .xlsx
            return pd.read_excel(file_path, sheet_name=self.sheet_name)
        except Exception as e:
            print(f"Error cargando Excel en {file_path}: {e}")
            return pd.DataFrame()

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        try:
            df.to_excel(output_path, index=False, sheet_name='DatosLimpios')
            print(f"✅ Archivo Excel limpio guardado en: {output_path}")
        except Exception as e:
            print(f"Error guardando Excel: {e}")
