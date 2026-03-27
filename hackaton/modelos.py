# Modelos IA / Algoritmos

import pandas as pd

class ModeloBase:
    def entrenar(self, X: pd.DataFrame, y: pd.Series):
        pass
    def predecir(self, X: pd.DataFrame):
        pass

# Aquí puedes agregar modelos específicos (clasificación, clustering, etc.)
