# utils/pago_registry.py
# Sistema simple de registro de pagos para callbacks

import time
import logging

log = logging.getLogger(__name__)

# Registro global de pagos activos
_pagos_activos = {}

def registrar_pago_activo(numero_pedido: str, instancia_pago):
    """Registra una instancia de pago activa"""
    global _pagos_activos
    _pagos_activos[numero_pedido] = instancia_pago
    log.info(f"📝 Pago registrado: {numero_pedido}")
    
    # Limpiar pagos antiguos automáticamente
    limpiar_pagos_antiguos()

def obtener_pago_activo(numero_pedido: str):
    """Obtiene un pago activo por número de pedido"""
    global _pagos_activos
    return _pagos_activos.get(numero_pedido)

def obtener_todos_los_pagos():
    """Obtiene todos los pagos activos"""
    global _pagos_activos
    return _pagos_activos.copy()

def desregistrar_pago(numero_pedido: str):
    """Desregistra una instancia de pago"""
    global _pagos_activos
    if numero_pedido in _pagos_activos:
        del _pagos_activos[numero_pedido]
        log.info(f"🗑️ Pago desregistrado: {numero_pedido}")

def limpiar_pagos_antiguos():
    """Elimina pagos que llevan más de 30 minutos activos"""
    global _pagos_activos
    tiempo_actual = time.time()
    pagos_a_eliminar = []
    
    for numero_pedido in list(_pagos_activos.keys()):
        try:
            # Los números de pedido son timestamps de 8 dígitos
            if numero_pedido.isdigit() and len(numero_pedido) >= 8:
                # Reconstruir timestamp aproximado
                timestamp_pedido = int(numero_pedido)
                # Si han pasado más de 30 minutos (1800 segundos)
                if tiempo_actual - timestamp_pedido > 1800:
                    pagos_a_eliminar.append(numero_pedido)
        except:
            # Si hay error, mantener el pago
            pass
    
    # Eliminar pagos antiguos
    for numero_pedido in pagos_a_eliminar:
        del _pagos_activos[numero_pedido]
    
    if pagos_a_eliminar:
        log.info(f"🧹 Limpiados {len(pagos_a_eliminar)} pagos antiguos")

def estado_registro():
    """Devuelve el estado actual del registro"""
    global _pagos_activos
    return {
        "total_pagos": len(_pagos_activos),
        "numeros_pedido": list(_pagos_activos.keys())
    }