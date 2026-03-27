# Inicializador del módulo limpieza por tipo de archivo

from .csv import limpiar_csv
from .pdf import limpiar_pdf
from .image import limpiar_imagen
from .sql import limpiar_sql, SqlCleaner
from .depurador import ejecutar_flujo
