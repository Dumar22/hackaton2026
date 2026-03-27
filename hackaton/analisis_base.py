import pandas as pd
import os

# Rutas de los archivos (ajusta según sea necesario)
BASE_PATH = os.path.dirname(__file__)
USUARIOS = os.path.join(BASE_PATH, 'usuarios.csv')
EVENTOS = os.path.join(BASE_PATH, 'eventos.csv')
PRODUCTOS = os.path.join(BASE_PATH, 'productos.csv')
INTERACCIONES = os.path.join(BASE_PATH, 'interacciones.csv')

# Carga de datos con manejo de errores

def cargar_csv(path):
    try:
        df = pd.read_csv(path)
        print(f"Cargado: {os.path.basename(path)} ({df.shape[0]} filas, {df.shape[1]} columnas)")
        return df
    except Exception as e:
        print(f"Error cargando {path}: {e}")
        return pd.DataFrame()

usuarios = cargar_csv(USUARIOS)
eventos = cargar_csv(EVENTOS)
productos = cargar_csv(PRODUCTOS)
interacciones = cargar_csv(INTERACCIONES)

import limpieza

# Limpieza estructurada de datos por archivo
dfs_raw = {
    'usuarios': usuarios,
    'eventos': eventos,
    'productos': productos,
    'interacciones': interacciones
}

dfs_limpios = limpieza.limpieza_integral(dfs_raw)

usuarios = dfs_limpios['usuarios']
eventos = dfs_limpios['eventos']
productos = dfs_limpios['productos']
interacciones = dfs_limpios['interacciones']

print("\n--- Resultados después de la limpieza ---")
for nombre, df_l in dfs_limpios.items():
    print(f"{nombre}: {df_l.shape[0]} filas limpias")

# Exploración rápida
print("\n--- Exploración rápida de usuarios ---")
print(usuarios.head())
print(usuarios.describe(include='all'))

print("\n--- Exploración rápida de eventos ---")
print(eventos['tipo_evento'].value_counts())

print("\n--- Exploración rápida de interacciones ---")
print(interacciones['accion'].value_counts())

# Puedes agregar aquí funciones para cohortes, segmentación, métricas, etc.

def resumen_general():
    print(f"\nUsuarios únicos: {usuarios['usuario_id'].nunique()}")
    print(f"Productos distintos: {productos['producto_id'].nunique()}")
    print(f"Eventos totales: {len(eventos)}")
    print(f"Interacciones totales: {len(interacciones)}")

if __name__ == "__main__":
    resumen_general()
