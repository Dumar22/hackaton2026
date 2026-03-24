"""
Generador de datos realistas para análisis y automatización de procesos
Genera 5000 registros con 10 columnas de datos con patrones identificables
"""
import random
import datetime
from typing import List, Dict
import json

class DataGenerator:
    """Genera datos realistas con patrones para análisis"""
    
    # Datos realistas
    PRODUCTO_CATEGORIAS = [
        'Electrónica', 'Ropa', 'Alimentos', 'Libros', 
        'Deportes', 'Casa', 'Belleza', 'Juguetes'
    ]
    
    REGIONES = [
        'Norte', 'Sur', 'Este', 'Oeste', 
        'Centro', 'Costera', 'Montaña', 'Metropolitana'
    ]
    
    ESTADOS_PEDIDO = [
        'Completado', 'Pendiente', 'En Proceso',
        'Cancelado', 'Reembolsado', 'En Espera'
    ]
    
    METODOS_PAGO = [
        'Tarjeta Crédito', 'Tarjeta Débito', 
        'PayPal', 'Transferencia', 'Efectivo'
    ]
    
    CLIENTE_TIPOS = [
        'Nuevo', 'Regular', 'Premium', 'VIP', 'Corporativo'
    ]
    
    def __init__(self, rows: int = 5000):
        """
        Args:
            rows: Número de registros a generar
        """
        self.rows = rows
        self.data = []
        self.generate()
    
    def generate(self) -> List[Dict]:
        """Genera datos con patrones realistas"""
        base_date = datetime.datetime(2024, 1, 1)
        
        for i in range(self.rows):
            # Crear variabilidad pero con patrones
            mes = (i // 200) % 12 + 1  # Patrón: cambio cada 200 registros
            
            record = {
                'id': str(i + 1).zfill(5),
                'fecha': (base_date + datetime.timedelta(days=i % 365)).strftime('%Y-%m-%d'),
                'categoria_producto': random.choice(self.PRODUCTO_CATEGORIAS),
                'region': random.choice(self.REGIONES),
                'cantidad': random.randint(1, 50),
                'precio_unitario': round(random.uniform(10, 1000), 2),
                'estado_pedido': self._get_estado_con_patron(i),
                'tipo_cliente': random.choice(self.CLIENTE_TIPOS),
                'metodo_pago': self._get_metodo_pago_con_patron(i),
                'monto_descuento': round(random.uniform(0, 50), 2)
            }
            
            # Calcular monto total
            record['monto_total'] = round(
                record['cantidad'] * record['precio_unitario'] - record['monto_descuento'],
                2
            )
            
            self.data.append(record)
        
        return self.data
    
    def _get_estado_con_patron(self, index: int) -> str:
        """Genera estado de pedido con patrón: más completados al inicio"""
        if index % 100 < 70:
            return 'Completado'
        elif index % 100 < 85:
            return 'Pendiente'
        elif index % 100 < 95:
            return 'En Proceso'
        else:
            return 'Cancelado'
    
    def _get_metodo_pago_con_patron(self, index: int) -> str:
        """Genera método de pago con patrón: más tarjetas de crédito"""
        random_val = random.random()
        if random_val < 0.5:
            return 'Tarjeta Crédito'
        elif random_val < 0.8:
            return 'Tarjeta Débito'
        elif random_val < 0.9:
            return 'PayPal'
        else:
            return random.choice(['Transferencia', 'Efectivo'])
    
    def get_data(self) -> List[Dict]:
        """Retorna los datos generados"""
        return self.data
    
    def get_headers(self) -> List[str]:
        """Retorna los nombres de las columnas"""
        return [
            'ID',
            'Fecha',
            'Categoría',
            'Región',
            'Cantidad',
            'Precio Unitario',
            'Estado',
            'Tipo Cliente',
            'Método Pago',
            'Descuento',
            'Monto Total'
        ]
    
    def get_sample(self, n: int = 10) -> List[Dict]:
        """Retorna una muestra de n registros"""
        return random.sample(self.data, min(n, len(self.data)))
    
    def get_stats(self) -> Dict:
        """Calcula estadísticas del dataset"""
        if not self.data:
            return {}
        
        totales = [d['monto_total'] for d in self.data]
        cantidades = [d['cantidad'] for d in self.data]
        descuentos = [d['monto_descuento'] for d in self.data]
        
        return {
            'total_registros': len(self.data),
            'monto_total_venta': round(sum(totales), 2),
            'monto_promedio': round(sum(totales) / len(totales), 2),
            'cantidad_promedio': round(sum(cantidades) / len(cantidades), 2),
            'descuento_total': round(sum(descuentos), 2),
            'cantidad_por_estado': self._contar_por_estado(),
            'cantidad_por_categoria': self._contar_por_categoria(),
            'cantidad_por_region': self._contar_por_region(),
            'cantidad_por_metodo_pago': self._contar_por_metodo_pago()
        }
    
    def _contar_por_estado(self) -> Dict[str, int]:
        """Cuenta registros por estado de pedido"""
        conteo = {}
        for record in self.data:
            estado = record['estado_pedido']
            conteo[estado] = conteo.get(estado, 0) + 1
        return conteo
    
    def _contar_por_categoria(self) -> Dict[str, int]:
        """Cuenta registros por categoría de producto"""
        conteo = {}
        for record in self.data:
            cat = record['categoria_producto']
            conteo[cat] = conteo.get(cat, 0) + 1
        return conteo
    
    def _contar_por_region(self) -> Dict[str, int]:
        """Cuenta registros por región"""
        conteo = {}
        for record in self.data:
            region = record['region']
            conteo[region] = conteo.get(region, 0) + 1
        return conteo
    
    def _contar_por_metodo_pago(self) -> Dict[str, int]:
        """Cuenta registros por método de pago"""
        conteo = {}
        for record in self.data:
            metodo = record['metodo_pago']
            conteo[metodo] = conteo.get(metodo, 0) + 1
        return conteo
