"""
CSV file cleaner – concrete implementation of BaseCleaner.
"""
import pandas as pd
from .base_cleaner import BaseCleaner


class CSVCleaner(BaseCleaner):
    """Reads and cleans CSV files using the standard cleaning pipeline."""

    def __init__(self, delimiter: str = ",", encoding: str = "utf-8"):
        self.delimiter = delimiter
        self.encoding = encoding

    def read_data(self, file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path, delimiter=self.delimiter, encoding=self.encoding)
        except Exception as e:
            print(f"Error loading CSV from {file_path}: {e}")
            return pd.DataFrame()

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        try:
            df.to_csv(output_path, index=False, sep=self.delimiter, encoding=self.encoding)
            print(f"✅ Cleaned CSV saved to: {output_path}")
        except Exception as e:
            print(f"Error saving CSV: {e}")
