"""
Mock data generator for the Hackathon 2026.
Produces realistic datasets for usuarios, eventos, productos, and interacciones.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_full_dataset(n_users=500, n_interactions=1000, n_events=2000):
    np.random.seed(42)
    random.seed(42)
    
    # --- 1. Usuarios ---
    ciudades = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Manizales", "Pereira", "Bucaramanga"]
    generos = ["M", "F", "Otro", None] # Incluimos nulos para probar la limpieza
    
    start_date = datetime(2025, 1, 1)
    
    users_data = {
        "usuario_id": range(1, n_users + 1),
        "edad": [random.randint(15, 60) if random.random() > 0.05 else np.nan for _ in range(n_users)],
        "genero": [random.choice(generos) for _ in range(n_users)],
        "ciudad": [random.choice(ciudades) if random.random() > 0.1 else "" for _ in range(n_users)],
        "fecha_registro": [(start_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(n_users)]
    }
    df_users = pd.DataFrame(users_data)
    
    # --- 2. Productos (Simulaciones) ---
    categorias = ["STEM", "Salud", "Ingeniería", "Gestión Ambiental", "Robótica"]
    productos_nombres = [
        "Física Mecánica I", "Química Orgánica", "Biología Celular", "Circuitos Eléctricos",
        "Termodinámica", "Anatomía Humana", "Microbiología", "Cálculo Integral",
        "Energías Renovables", "Gestión de Residuos", "Programación PLC", "Mecatrónica",
        "Hidráulica", "Suelos y Pavimentos", "Bioquímica", "Electromagnetismo",
        "Estadística Descriptiva", "Geología", "Botánica", "Física Nuclear"
    ]
    
    df_products = pd.DataFrame({
        "producto_id": range(101, 101 + len(productos_nombres)),
        "nombre": productos_nombres,
        "categoria": [random.choice(categorias) for _ in range(len(productos_nombres))]
    })
    
    # --- 3. Interacciones (Comportamiento) ---
    accione_types = ["completado", "abandonado", "en_progreso"]
    
    interactions = []
    for _ in range(n_interactions):
        u_id = random.randint(1, n_users)
        p_id = random.choice(df_products["producto_id"].values)
        
        # Generar sesgo: usuarios jóvenes tienden a completar más Robótica
        user_age = df_users.loc[u_id-1, "edad"]
        prod_cat = df_products.loc[p_id-101, "categoria"]
        
        if not np.isnan(user_age) and user_age < 25 and prod_cat == "Robótica":
            accion = "completado" if random.random() > 0.1 else "abandonado"
        else:
            accion = random.choices(accione_types, weights=[0.4, 0.4, 0.2])[0]
            
        date = (datetime(2026, 3, 1) + timedelta(days=random.randint(0, 25))).strftime('%Y-%m-%d')
        interactions.append([u_id, p_id, date, accion])
        
    df_interactions = pd.DataFrame(interactions, columns=["usuario_id", "producto_id", "fecha", "accion"])
    
    # --- 4. Eventos (Navegación) ---
    event_types = ["login", "simulacion", "descarga_guia", "ver_tutorial"]
    detalles = {
        "login": ["web", "mobile", "tablet"],
        "simulacion": ["inicio", "pausa", "fin"],
        "descarga_guia": ["pdf", "html"],
        "ver_tutorial": ["video", "texto"]
    }
    
    events = []
    for _ in range(n_events):
        u_id = random.randint(1, n_users)
        etype = random.choice(event_types)
        det = random.choice(detalles[etype])
        date = (datetime(2026, 3, 1) + timedelta(days=random.randint(0, 25))).strftime('%Y-%m-%d %H:%M:%S')
        events.append([u_id, date, etype, det])
        
    df_events = pd.DataFrame(events, columns=["usuario_id", "fecha_evento", "tipo_evento", "detalle"])
    
    return df_users, df_products, df_interactions, df_events

if __name__ == "__main__":
    print("🚀 Generando datos sintéticos para Hackathon 2026...")
    u, p, i, e = generate_full_dataset()
    
    base_path = os.path.dirname(__file__)
    u.to_csv(os.path.join(base_path, "usuarios.csv"), index=False)
    p.to_csv(os.path.join(base_path, "productos.csv"), index=False)
    i.to_csv(os.path.join(base_path, "interacciones.csv"), index=False)
    e.to_csv(os.path.join(base_path, "eventos.csv"), index=False)
    
    print(f"✅ datasets generados en {base_path}:")
    print(f"   - Usuarios: {len(u)}")
    print(f"   - Productos: {len(p)}")
    print(f"   - Interacciones: {len(i)}")
    print(f"   - Eventos: {len(e)}")
