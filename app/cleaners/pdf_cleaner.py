"""
PDF file cleaner – concrete implementation of BaseCleaner.

Note: requires `tabula-py` or `pdfplumber` installed.
Install with:  pip install tabula-py  OR  pip install pdfplumber
"""
import pandas as pd
from .base_cleaner import BaseCleaner


class PDFCleaner(BaseCleaner):
    """
    Extracts and cleans tabular data embedded in PDF files.
    Falls back to an empty DataFrame if the required library is not installed.
    """

    def read_data(self, file_path: str) -> pd.DataFrame:
        try:
            import tabula  # type: ignore
            dfs = tabula.read_pdf(file_path, pages="all", multiple_tables=True)
            return pd.concat(dfs, ignore_index=True)
        except ImportError:
            print("tabula-py is not installed. Run: pip install tabula-py")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error extracting table from PDF {file_path}: {e}")
            return pd.DataFrame()

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        try:
            # PDF output is uncommon – save as CSV instead
            csv_path = output_path.replace(".pdf", ".csv") if output_path.endswith(".pdf") else output_path
            df.to_csv(csv_path, index=False)
            print(f"✅ PDF-extracted data saved as CSV: {csv_path}")
        except Exception as e:
            print(f"Error saving PDF-extracted data: {e}")

    def correct_typos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Override to also strip carriage returns typical in PDF-to-text conversions."""
        df = super().correct_typos(df)
        text_cols = df.select_dtypes(include=["object", "string"]).columns
        for col in text_cols:
            df[col] = df[col].replace(r"[\r\n]+", " ", regex=True)
        return df
