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

# Limpieza básica de datos

def limpieza_basica(df, nombre):
    print(f"\n--- Limpieza básica: {nombre} ---")
    print(df.info())
    print("Valores nulos por columna:")
    print(df.isnull().sum())
    # Ejemplo: eliminar duplicados
    df = df.drop_duplicates()
    # Ejemplo: rellenar NaN en columnas clave
    if 'edad' in df.columns:
        df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
        df['edad'] = df['edad'].fillna(df['edad'].median())
    if 'genero' in df.columns:
        df['genero'] = df['genero'].fillna('Sin dato')
    if 'ciudad' in df.columns:
        df['ciudad'] = df['ciudad'].fillna('Sin dato')
    return df

usuarios = limpieza_basica(usuarios, 'usuarios')
eventos = limpieza_basica(eventos, 'eventos')
productos = limpieza_basica(productos, 'productos')
interacciones = limpieza_basica(interacciones, 'interacciones')

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
