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
        """4. Valores extremos (outliers): Eliminar usando rango intercuartílico (IQR) en numéricas"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            # Filtrar DataFrame eliminando valores fuera de los bounds
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        return df

    def correct_typos(self, df: pd.DataFrame) -> pd.DataFrame:
        """5. Errores tipográficos: Corregir en variables categóricas"""
        text_cols = df.select_dtypes(include=['object', 'string']).columns
        for col in text_cols:
            # Limpieza básica: quitar espacios sobrantes (ej. dobles espacios a uno)
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
            # Reemplazos puntuales específicos del dominio (se pueden configurar dicts a futuro)
        return df

    def check_logical_integrity(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        6. Integridad Lógica: Validaciones estándar de sentido común entre variables.
        """
        # Restricción Lógica de la Edad: Si existe 'edad' o 'age', debe estar en un rango [0, 120]
        age_cols = [col for col in df.columns if 'edad' in col.lower() or 'age' in col.lower()]
        for col in age_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                df = df[(df[col] >= 0) & (df[col] <= 120)]

        # Restricción Lógica de Fechas: Ej. Fecha_Entrega NO menor a Fecha_Pedido
        if 'fecha_pedido' in df.columns and 'fecha_entrega' in df.columns:
            try:
                pedido = pd.to_datetime(df['fecha_pedido'], errors='coerce')
                entrega = pd.to_datetime(df['fecha_entrega'], errors='coerce')
                valid_dates = (entrega >= pedido) | entrega.isna() | pedido.isna()
                df = df[valid_dates]
            except Exception:
                pass

        return df

    def normalize_text(self, df: pd.DataFrame) -> pd.DataFrame:
        """7. Normalizar el texto (Minúsculas)"""
        text_cols = df.select_dtypes(include=['object', 'string']).columns
        for col in text_cols:
            # Todas las variables de texto a minúsculas
            df[col] = df[col].astype(str).str.lower()
        return df
