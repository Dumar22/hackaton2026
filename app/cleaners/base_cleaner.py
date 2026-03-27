from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class BaseCleaner(ABC):
    """
    Clase abstracta basada en el principio de Inversión de Dependencias y Abierto/Cerrado (SOLID).
    Define el proceso estándar de limpieza de datos garantizando que las 
    distintas implementaciones (CSV, Excel, PDF) no dependan entre sí, 
    sino de este contrato general.
    """

    @abstractmethod
    def read_data(self, file_path: str) -> pd.DataFrame:
        """Lee el archivo y retorna un DataFrame de pandas."""
        pass

    @abstractmethod
    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        """Guarda el DataFrame limpio en el formato correspondiente."""
        pass

    def clean(self, file_path: str, output_path: str, irrelevant_cols=None) -> pd.DataFrame:
        """
        Template Method: Orquesta los pasos de la limpieza de datos en orden.
        """
        df = self.read_data(file_path)
        if df.empty:
            print("El DataFrame devuelto está vacío. Revisa la fuente de datos.")
            return df

        if irrelevant_cols:
            df = self.remove_irrelevant_columns(df, irrelevant_cols)
            
        df = self.remove_duplicates(df)
        df = self.handle_missing_data(df)
        df = self.remove_outliers(df)
        df = self.correct_typos(df)
        df = self.check_logical_integrity(df)
        df = self.normalize_text(df)

        self.save_data(df, output_path)
        return df

    def handle_missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """1. Datos Faltantes: Imputar o eliminar"""
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                # Imputación por mediana para numéricos, si no está toda la columna en NaN
                value = df[col].median() if not df[col].isnull().all() else 0
                df[col] = df[col].fillna(value)
            else:
                # Imputación por 'Desconocido' para categóricos/texto
                df[col] = df[col].fillna('Desconocido')
        return df

    def remove_irrelevant_columns(self, df: pd.DataFrame, columns_to_drop: list) -> pd.DataFrame:
        """2. Columnas irrelevantes: Eliminar"""
        cols_to_drop = [c for c in columns_to_drop if c in df.columns]
        return df.drop(columns=cols_to_drop)

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """3. Registros repetidos: Eliminar"""
        return df.drop_duplicates()

    def remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        4. Valores extremos (outliers): Optimización Vectorizada.
        Calcula una máscara global para filtrar el DataFrame una sola vez.
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if numeric_cols.empty: return df

        # Construir máscara booleana global de 'filas válidas'
        global_mask = pd.Series(True, index=df.index)
        
        for col in numeric_cols:
            col_data = df[col]
            q1 = col_data.quantile(0.25)
            q3 = col_data.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            # Actualizar máscara (AND lógico)
            global_mask &= (col_data >= lower) & (col_data <= upper)

        return df[global_mask]

    def correct_typos(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        5. Errores tipográficos: Optimización de motor de strings.
        Consolida operaciones y utiliza PyArrow para velocidad extrema si está disponible.
        """
        text_cols = df.select_dtypes(include=['object', 'string']).columns
        if text_cols.empty: return df

        # Intentar usar motor PyArrow para máxima velocidad en regex
        try:
            for col in text_cols:
                # Combinamos limpieza en una sola asignación para evitar copias intermedias
                df[col] = df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True, engine='pyarrow')
        except (TypeError, ImportError):
            # Fallback al motor estándar si PyArrow no está instalado o compatible
            for col in text_cols:
                df[col] = df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
                
        return df

    def check_logical_integrity(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        6. Integridad Lógica: Validaciones vectorizadas.
        """
        # Restricción Lógica de la Edad
        age_cols = [col for col in df.columns if 'edad' in col.lower() or 'age' in col.lower()]
        for col in age_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                df = df[(df[col] >= 0) & (df[col] <= 120)]

        # Restricción Lógica de Fechas
        if 'fecha_pedido' in df.columns and 'fecha_entrega' in df.columns:
            try:
                pedido = pd.to_datetime(df['fecha_pedido'], errors='coerce')
                entrega = pd.to_datetime(df['fecha_entrega'], errors='coerce')
                df = df[(entrega >= pedido) | entrega.isna() | pedido.isna()]
            except: pass

        return df

    def normalize_text(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        7. Normalizar el texto: Consolidación a minúsculas.
        """
        text_cols = df.select_dtypes(include=['object', 'string']).columns
        # No usamos pyarrow aquí porque .lower() es muy eficiente nativamente
        for col in text_cols:
            df[col] = df[col].astype(str).str.lower()
        return df
