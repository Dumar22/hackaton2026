# Procesamiento y limpieza de datos provenientes de SQL

import pandas as pd
from sqlalchemy import create_engine
from typing import Optional, List
from .csv import CsvCleaner
from app.core.config import settings

class SqlCleaner:
    def __init__(self,
                 columns_to_remove: Optional[List[str]] = None,
                 numeric_columns: Optional[List[str]] = None,
                 categorical_columns: Optional[List[str]] = None,
                 text_columns: Optional[List[str]] = None):
        self.csv_cleaner = CsvCleaner(columns_to_remove, numeric_columns, categorical_columns, text_columns)
        self.engine = create_engine(settings.DATABASE_URL)

    def clean(self, query: str) -> pd.DataFrame:
        df = pd.read_sql(query, self.engine)
        return self.csv_cleaner.clean(df)

# Función de alto nivel

def limpiar_sql(query: str,
                columns_to_remove: Optional[List[str]] = None,
                numeric_columns: Optional[List[str]] = None,
                categorical_columns: Optional[List[str]] = None,
                text_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Limpia y estructura datos de una consulta SQL siguiendo buenas prácticas SOLID."""
    cleaner = SqlCleaner(columns_to_remove, numeric_columns, categorical_columns, text_columns)
    return cleaner.clean(query)
