# Análisis exploratorio de datos

import pandas as pd

class AnalisisExploratorio:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def resumen_estadistico(self):
        return self.df.describe(include='all')

    def correlaciones(self):
        return self.df.corr(numeric_only=True)

    def valores_unicos(self):
        return {col: self.df[col].unique() for col in self.df.columns}

    # Agrega más métodos según necesidades del reto
