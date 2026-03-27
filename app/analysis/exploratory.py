"""
Exploratory data analysis utilities.
"""
import pandas as pd


class ExploratoryAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def statistical_summary(self) -> pd.DataFrame:
        """Returns descriptive statistics for all columns."""
        return self.df.describe(include="all")

    def correlations(self) -> pd.DataFrame:
        """Returns the correlation matrix for numeric columns."""
        return self.df.corr(numeric_only=True)

    def unique_values(self) -> dict:
        """Returns unique values per column."""
        return {col: self.df[col].unique().tolist() for col in self.df.columns}

    def missing_report(self) -> pd.DataFrame:
        """Returns a report of missing values per column."""
        report = pd.DataFrame({
            "missing_count": self.df.isnull().sum(),
            "missing_pct": (self.df.isnull().sum() / len(self.df) * 100).round(2),
        })
        return report[report["missing_count"] > 0].sort_values("missing_pct", ascending=False)
