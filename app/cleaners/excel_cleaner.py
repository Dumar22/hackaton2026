"""
Excel file cleaner – concrete implementation of BaseCleaner.
"""
import pandas as pd
from .base_cleaner import BaseCleaner


class ExcelCleaner(BaseCleaner):
    """Reads and cleans Excel (.xlsx / .xls) files using the standard cleaning pipeline."""

    def __init__(self, sheet_name: int = 0):
        self.sheet_name = sheet_name

    def read_data(self, file_path: str) -> pd.DataFrame:
        try:
            # Requires openpyxl for .xlsx
            return pd.read_excel(file_path, sheet_name=self.sheet_name)
        except Exception as e:
            print(f"Error loading Excel from {file_path}: {e}")
            return pd.DataFrame()

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        try:
            df.to_excel(output_path, index=False, sheet_name="CleanData")
            print(f"✅ Cleaned Excel saved to: {output_path}")
        except Exception as e:
            print(f"Error saving Excel: {e}")
