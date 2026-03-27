"""
SQL data cleaner – reads from a database and applies the same cleaning pipeline
as CSVCleaner, since the data ends up as a pandas DataFrame either way.
"""
import pandas as pd
from sqlalchemy import create_engine
from typing import Optional, List

from .base_cleaner import BaseCleaner


class SQLCleaner(BaseCleaner):
    """
    Reads data from a SQL database via SQLAlchemy and cleans it
    using the standard BaseCleaner pipeline.
    """

    def __init__(self, database_url: str, query: str):
        self.database_url = database_url
        self.query = query
        self._engine = None

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(self.database_url)
        return self._engine

    def read_data(self, source: str = None) -> pd.DataFrame:
        """Executes stored SQL query and returns a DataFrame."""
        try:
            return pd.read_sql(self.query, self.engine)
        except Exception as e:
            print(f"Error reading SQL data: {e}")
            return pd.DataFrame()

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        try:
            df.to_csv(output_path, index=False)
            print(f"✅ Cleaned SQL data saved to CSV: {output_path}")
        except Exception as e:
            print(f"Error saving SQL data: {e}")

    def clean(self, output_path: str = "cleaned_output.csv", irrelevant_cols=None) -> pd.DataFrame:
        return super().clean(source=None, output_path=output_path, irrelevant_cols=irrelevant_cols)
