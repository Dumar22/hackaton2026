"""
Clasificador y automatizador de procesos basado en patrones
"""
from typing import List, Dict, Tuple
from enum import Enum

class PriorityLevel(Enum):
    """Niveles de prioridad"""
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"

class ProcessClassifier:
    """Clasifica y automatiza procesos basado en reglas y patrones"""
    
    # Reglas de clasificación
    RULES = {
        "prioridad_cliente": {
            "VIP": PriorityLevel.URGENTE,
            "Premium": PriorityLevel.ALTA,
            "Regular": PriorityLevel.MEDIA,
            "Nuevo": PriorityLevel.MEDIA,
            "Corporativo": PriorityLevel.URGENTE
        },
        "prioridad_estado": {
            "Cancelado": PriorityLevel.BAJA,
            "Reembolsado": PriorityLevel.BAJA,
            "En Espera": PriorityLevel.MEDIA,
            "Pendiente": PriorityLevel.ALTA,
            "En Proceso": PriorityLevel.ALTA,
            "Completado": PriorityLevel.BAJA
        },
        "monto_critico": 500.0  # Montos mayores a 500 son prioritarios
    }
    
    def __init__(self):
        """Inicializa el clasificador"""
        self.classified_data = {}
        self.automation_rules = self._initialize_automation_rules()
    
    def classify_all(self, data: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Clasifica todos los registros
        
        Args:
            data: Lista de registros
        
        Returns:
            Registros clasificados por categoría
        """
        classified = {
            "urgentes": [],
            "alta_prioridad": [],
            "media_prioridad": [],
            "baja_prioridad": [],
            "anomalias": [],
            "automatizable": []
        }
        
        for record in data:
            classification = self.classify_record(record)
            priority = classification["priority"]
            
            if priority == PriorityLevel.URGENTE:
                classified["urgentes"].append(record)
            elif priority == PriorityLevel.ALTA:
                classified["alta_prioridad"].append(record)
            elif priority == PriorityLevel.MEDIA:
                classified["media_prioridad"].append(record)
            else:
                classified["baja_prioridad"].append(record)
            
            if classification.get("anomaly"):
                classified["anomalias"].append(record)
            
            if classification.get("can_automate"):
                classified["automatizable"].append(record)
        
        self.classified_data = classified
        return classified
    
    def classify_record(self, record: Dict) -> Dict:
        """
        Clasifica un registro individual
        
        Args:
            record: Registro a clasificar
        
        Returns:
            Clasificación del registro
        """
        classification = {
            "priority": PriorityLevel.MEDIA,
            "reason": [],
            "anomaly": False,
            "can_automate": False,
            "suggested_action": "",
            "metadata": {}
        }
        
        # Aplicar reglas de prioridad
        type_cliente = record.get("tipo_cliente", "")
        if type_cliente in self.RULES["prioridad_cliente"]:
            priority = self.RULES["prioridad_cliente"][type_cliente]
            classification["priority"] = priority
            classification["reason"].append(f"Cliente tipo: {type_cliente}")
        
        # Considerar estado del pedido
        estado = record.get("estado_pedido", "")
        if estado in self.RULES["prioridad_estado"]:
            state_priority = self.RULES["prioridad_estado"][estado]
            if state_priority.value > classification["priority"].value:
                classification["priority"] = state_priority
                classification["reason"].append(f"Estado: {estado}")
        
        # Montos elevados
        monto = float(record.get("monto_total", 0))
        if monto > self.RULES["monto_critico"]:
            classification["priority"] = PriorityLevel.URGENTE
            classification["reason"].append(f"Monto elevado: ${monto:.2f}")
            classification["metadata"]["monto_elevado"] = True
        
        # Detectar anomalías
        classification["anomaly"] = self._detect_anomalies(record)
        if classification["anomaly"]:
            classification["reason"].append("Anomalía detectada")
        
        # Determinar si puede ser automatizado
        classification["can_automate"] = self._can_automate(record)
        if classification["can_automate"]:
            classification["reason"].append("Proceso automatizable")
            classification["suggested_action"] = self._get_automation_action(record)
        
        return classification
    
    def _detect_anomalies(self, record: Dict) -> bool:
        """Detecta anomalías en el registro"""
        # Cantidad inusualmente alta
        cantidad = int(record.get("cantidad", 0))
        if cantidad > 40:
            return True
        
        # Descuento muy alto
        descuento = float(record.get("monto_descuento", 0))
        if descuento > 40:
            return True
        
        # Precio muy bajo
        precio = float(record.get("precio_unitario", 1))
        if precio < 15 and cantidad > 20:
            return True
        
        # Estado pendiente/en espera con fecha antigua
        # (simplificado para este ejemplo)
        
        return False
    
    def _can_automate(self, record: Dict) -> bool:
        """Determina si el proceso puede ser automatizado"""
        estado = record.get("estado_pedido", "")
        metodo_pago = record.get("metodo_pago", "")
        tipo_cliente = record.get("tipo_cliente", "")
        
        # Automatizable si:
        # - Pedido completado
        # - Pago con tarjeta (automático)
        # - Cliente regular o corporativo
        return (
            estado == "Completado" and
            metodo_pago in ["Tarjeta Crédito", "Tarjeta Débito"] and
            tipo_cliente in ["Regular", "Premium", "Corporativo"]
        )
    
    def _get_automation_action(self, record: Dict) -> str:
        """Define la acción de automatización"""
        metodo = record.get("metodo_pago", "")
        
        if metodo == "Tarjeta Crédito":
            return "Generar factura automática + Actualizar inventario + Enviar confirmación"
        elif metodo == "Tarjeta Débito":
            return "Generar factura automática + Actualizar inventario + Enviar confirmación"
        elif metodo == "PayPal":
            return "Integración PayPal + Enviar confirmación"
        else:
            return "Revisar manualmente antes de procesar"
    
    def generate_workflow(self, classified_data: Dict = None) -> Dict:
        """
        Genera flujo de trabajo recomendado
        
        Args:
            classified_data: Datos clasificados (usa los guardados si no se proporciona)
        
        Returns:
            Flujo de trabajo recomendado
        """
        if not classified_data:
            classified_data = self.classified_data
        
        workflow = {
            "fase_1": {
                "nombre": "Procesar Urgentes",
                "cantidad": len(classified_data.get("urgentes", [])),
                "tiempo_estimado": f"{len(classified_data.get('urgentes', [])) * 2} minutos",
                "acciones": [
                    "Revisar registros urgentes",
                    "Asignar a equipo premium",
                    "Procesar inmediatamente"
                ]
            },
            "fase_2": {
                "nombre": "Automatizar Procesos",
                "cantidad": len(classified_data.get("automatizable", [])),
                "tiempo_estimado": f"Automático - {len(classified_data.get('automatizable', [])) * 0.5:.0f} segundos",
                "acciones": [
                    "Ejecutar procesos automáticos",
                    "Generar facturas",
                    "Actualizar inventario",
                    "Enviar confirmaciones"
                ]
            },
            "fase_3": {
                "nombre": "Revisar Alta Prioridad",
                "cantidad": len(classified_data.get("alta_prioridad", [])),
                "tiempo_estimado": f"{len(classified_data.get('alta_prioridad', [])) * 1} minutos",
                "acciones": [
                    "Revisar registros de alta prioridad",
                    "Asignar a equipo estándar"
                ]
            },
            "fase_4": {
                "nombre": "Investigar Anomalías",
                "cantidad": len(classified_data.get("anomalias", [])),
                "tiempo_estimado": f"{len(classified_data.get('anomalias', [])) * 3} minutos",
                "acciones": [
                    "Análisis de anomalías",
                    "Verificar integridad de datos",
                    "Contactar cliente si es necesario"
                ]
            },
            "fase_5": {
                "nombre": "Procesar Resto",
                "cantidad": len(classified_data.get("media_prioridad", [])) + len(classified_data.get("baja_prioridad", [])),
                "tiempo_estimado": "Según disponibilidad",
                "acciones": [
                    "Realizar en horarios de baja actividad"
                ]
            }
        }
        
        return workflow
    
    def get_metrics(self, data: List[Dict] = None) -> Dict:
        """
        Genera métricas de clasificación
        
        Args:
            data: Datos a analizar (usa los clasificados si no se proporciona)
        
        Returns:
            Métricas de clasificación
        """
        if data:
            classified = self.classify_all(data)
        else:
            classified = self.classified_data
        
        total = sum(len(v) for v in classified.values() if isinstance(v, list))
        
        metrics = {
            "total_registros": total,
            "distribucion": {
                "urgentes_pct": (len(classified.get("urgentes", [])) / total * 100) if total else 0,
                "alta_prioridad_pct": (len(classified.get("alta_prioridad", [])) / total * 100) if total else 0,
                "media_prioridad_pct": (len(classified.get("media_prioridad", [])) / total * 100) if total else 0,
                "baja_prioridad_pct": (len(classified.get("baja_prioridad", [])) / total * 100) if total else 0,
            },
            "automatizacion": {
                "automatizable_total": len(classified.get("automatizable", [])),
                "automatizable_pct": (len(classified.get("automatizable", [])) / total * 100) if total else 0,
                "ahorro_tiempo_horas": len(classified.get("automatizable", [])) * 0.016,  # 1 minuto por registro
            },
            "anomalias": {
                "detectadas": len(classified.get("anomalias", [])),
                "porcentaje": (len(classified.get("anomalias", [])) / total * 100) if total else 0,
            }
        }
        
        return metrics
    
    def _initialize_automation_rules(self) -> Dict:
        """Inicializa reglas de automatización"""
        return {
            "tarjeta_credito": {"factura": True, "inventario": True, "confirmacion": True},
            "paypal": {"factura": True, "confirmacion": True},
            "transferencia": {"factura": True, "esperar_confirmacion": True},
            "efectivo": {"esperar_confirmacion": True}
        }
