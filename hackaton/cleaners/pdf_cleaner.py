import pandas as pd
from .base_cleaner import BaseCleaner

class PDFCleaner(BaseCleaner):
    """
    Implementación concreta para extraer y limpiar tablas incrustadas en PDF.
    """
    
    def read_data(self, file_path: str) -> pd.DataFrame:
        """
        Lee datos tabulares de un PDF. 
        Generalmente requiere tabula-py o pdfplumber instanciado en el entorno.
        """
        try:
            # Ejemplo con tabula-py:
            # import tabula
            # dfs = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
            # return pd.concat(dfs, ignore_index=True)
            
            print(f"Información: Para extraer los datos reales del PDF {file_path} necesitas 'tabula-py'.")
            print("Devolviendo DataFrame vacío como placeholder estructural.")
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error extrayendo tabla del PDF {file_path}: {e}")
            return pd.DataFrame()

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        try:
            # Es poco común guardar en PDF, su lugar seguro suele ser escribir un CSV derivado
            csv_path = output_path.replace('.pdf', '.csv') if output_path.endswith('.pdf') else output_path
            df.to_csv(csv_path, index=False)
            print(f"✅ Datos de PDF limpios guardados como CSV en: {csv_path}")
        except Exception as e:
            print(f"Error guardando tabla extraída en {output_path}: {e}")

    def correct_typos(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sobrescribe paso para PDF, es clásico tener retornos de carro '\r' 
        por parseos fallidos.
        """
        df = super().correct_typos(df)
        text_cols = df.select_dtypes(include=['object', 'string']).columns
        for col in text_cols:
            # Ajuste de ruido clásico en conversiones PDF -> Texto
            df[col] = df[col].replace(r'[\r\n]+', ' ', regex=True)
        return df
