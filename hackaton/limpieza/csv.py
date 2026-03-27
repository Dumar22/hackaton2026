# Procesamiento y limpieza de archivos CSV
import pandas as pd
from typing import List, Optional

class MissingValueCleaner:
	def clean(self, df: pd.DataFrame) -> pd.DataFrame:
		# Elimina filas con valores nulos (puede adaptarse a imputación)
		return df.dropna()

class IrrelevantColumnsCleaner:
	def __init__(self, columns_to_remove: Optional[List[str]] = None):
		self.columns_to_remove = columns_to_remove or []
	def clean(self, df: pd.DataFrame) -> pd.DataFrame:
		return df.drop(columns=self.columns_to_remove, errors='ignore')

class DuplicatesCleaner:
	def clean(self, df: pd.DataFrame) -> pd.DataFrame:
		return df.drop_duplicates()

class OutlierCleaner:
	def __init__(self, numeric_columns: Optional[List[str]] = None):
		self.numeric_columns = numeric_columns
	def clean(self, df: pd.DataFrame) -> pd.DataFrame:
		if not self.numeric_columns:
			return df
		for col in self.numeric_columns:
			if col in df.columns:
				q1 = df[col].quantile(0.25)
				q3 = df[col].quantile(0.75)
				iqr = q3 - q1
				lower = q1 - 1.5 * iqr
				upper = q3 + 1.5 * iqr
				df = df[(df[col] >= lower) & (df[col] <= upper)]
		return df

class TypoCleaner:
	def __init__(self, categorical_columns: Optional[List[str]] = None):
		self.categorical_columns = categorical_columns
	def clean(self, df: pd.DataFrame) -> pd.DataFrame:
		# Corrige errores tipográficos simples (espacios, mayúsculas)
		if not self.categorical_columns:
			return df
		for col in self.categorical_columns:
			if col in df.columns:
				df[col] = df[col].astype(str).str.strip().str.lower()
		return df

class LogicalIntegrityCleaner:
	def clean(self, df: pd.DataFrame) -> pd.DataFrame:
		# Ejemplo: fecha_entrega >= fecha_pedido
		if 'fecha_entrega' in df.columns and 'fecha_pedido' in df.columns:
			df = df[df['fecha_entrega'] >= df['fecha_pedido']]
		if 'edad' in df.columns:
			df = df[(df['edad'] > 0) & (df['edad'] < 120)]
		return df

class TextNormalizer:
	def __init__(self, text_columns: Optional[List[str]] = None):
		self.text_columns = text_columns
	def clean(self, df: pd.DataFrame) -> pd.DataFrame:
		if not self.text_columns:
			return df
		for col in self.text_columns:
			if col in df.columns:
				df[col] = df[col].astype(str).str.strip().str.lower()
		return df

class CsvCleaner:
	def __init__(self,
				 columns_to_remove: Optional[List[str]] = None,
				 numeric_columns: Optional[List[str]] = None,
				 categorical_columns: Optional[List[str]] = None,
				 text_columns: Optional[List[str]] = None):
		self.steps = [
			MissingValueCleaner(),
			IrrelevantColumnsCleaner(columns_to_remove),
			DuplicatesCleaner(),
			OutlierCleaner(numeric_columns),
			TypoCleaner(categorical_columns),
			LogicalIntegrityCleaner(),
			TextNormalizer(text_columns)
		]

	def clean(self, ruta_archivo: str) -> pd.DataFrame:
		df = pd.read_csv(ruta_archivo)
		for step in self.steps:
			df = step.clean(df)
		return df

# Función de alto nivel para usar desde fuera
def limpiar_csv(ruta_archivo,
				columns_to_remove: Optional[List[str]] = None,
				numeric_columns: Optional[List[str]] = None,
				categorical_columns: Optional[List[str]] = None,
				text_columns: Optional[List[str]] = None) -> pd.DataFrame:
	"""Limpia y estructura datos de un archivo CSV siguiendo buenas prácticas SOLID."""
	cleaner = CsvCleaner(columns_to_remove, numeric_columns, categorical_columns, text_columns)
	return cleaner.clean(ruta_archivo)
