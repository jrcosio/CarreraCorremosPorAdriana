# utils/tpv_routes.py
import base64
import json
import logging
from urllib.parse import parse_qs
import flet as ft

log = logging.getLogger(__name__)

def manejar_rutas_tpv(page: ft.Page, route: str) -> bool:
    """
    Maneja las rutas específicas del TPV.
    
    Returns:
        bool: True si se manejó una ruta del TPV, False si no es una ruta del TPV
    """
    
    # Extraer parámetros de la URL si los hay
    parametros_url = {}
    ruta_base = route
    
    if '?' in route:
        ruta_base, query_string = route.split('?', 1)
        parametros_url = parse_qs(query_string)
        log.info(f"🔍 Parámetros URL detectados: {list(parametros_url.keys())}")
    
    # Verificar si es una ruta del TPV
    if not ruta_base.startswith('/tpv/'):
        return False  # No es una ruta del TPV
    
    log.info(f"🎯 Procesando ruta TPV: {ruta_base}")
    
    try:
        # Extraer número de pedido si está en los parámetros
        numero_pedido = None
        if 'Ds_MerchantParameters' in parametros_url:
            try:
                parametros_codificados = parametros_url['Ds_MerchantParameters'][0]
                parametros_json = base64.b64decode(parametros_codificados).decode('utf-8')
                parametros = json.loads(parametros_json)
                numero_pedido = parametros.get('Ds_Order', 'N/A')
                log.info(f"📋 Número de pedido extraído: {numero_pedido}")
            except Exception as e:
                log.warning(f"⚠️ Error extrayendo número de pedido: {e}")
        
        # Procesar según la ruta específica
        if ruta_base == '/tpv/exito':
            _manejar_callback_exito(page, parametros_url, numero_pedido)
            
        elif ruta_base == '/tpv/error':
            _manejar_callback_error(page, parametros_url, numero_pedido)
            
        elif ruta_base == '/tpv/notificacion':
            _manejar_callback_notificacion(page, parametros_url, numero_pedido)
            
        else:
            log.warning(f"⚠️ Ruta TPV no reconocida: {ruta_base}")
            _mostrar_pagina_generica(page, "Ruta TPV no reconocida", ruta_base)
        
        return True  # Se manejó como ruta del TPV
        
    except Exception as e:
        log.error(f"❌ Error procesando ruta TPV {ruta_base}: {e}")
        _mostrar_pagina_error(page, f"Error interno: {str(e)}")
        return True  # Aún es una ruta del TPV, aunque con error


def _manejar_callback_exito(page: ft.Page, parametros_url: dict, numero_pedido: str):
    """Maneja el callback de éxito del TPV"""
    log.info("🎉 Procesando callback de éxito")
    
    # Intentar procesar con el sistema de DorsalSolidarioScreen
    try:
        from dorsal_solidario.dorsalsolidario_screen import DorsalSolidarioScreen
        
        if DorsalSolidarioScreen.procesar_callback_tpv(numero_pedido or 'unknown', 'exito', parametros_url):
            log.info("✅ Callback procesado por DorsalSolidarioScreen")
        else:
            log.warning("⚠️ No se pudo procesar el callback")
            
    except ImportError as e:
        log.warning(f"⚠️ No se pudo importar DorsalSolidarioScreen: {e}")
    except Exception as e:
        log.error(f"❌ Error procesando callback de éxito: {e}")
    
    # Mostrar página de confirmación
    _mostrar_pagina_exito(page, numero_pedido)


def _manejar_callback_error(page: ft.Page, parametros_url: dict, numero_pedido: str):
    """Maneja el callback de error del TPV"""
    log.info("❌ Procesando callback de error")
    
    # Intentar procesar con el sistema de DorsalSolidarioScreen
    try:
        from dorsal_solidario.dorsalsolidario_screen import DorsalSolidarioScreen
        
        if DorsalSolidarioScreen.procesar_callback_tpv(numero_pedido or 'unknown', 'error', parametros_url):
            log.info("✅ Callback de error procesado por DorsalSolidarioScreen")
        else:
            log.warning("⚠️ No se pudo procesar el callback de error")
            
    except ImportError as e:
        log.warning(f"⚠️ No se pudo importar DorsalSolidarioScreen: {e}")
    except Exception as e:
        log.error(f"❌ Error procesando callback de error: {e}")
    
    # Mostrar página de error
    _mostrar_pagina_error(page, "Pago cancelado o error en el proceso")


def _manejar_callback_notificacion(page: ft.Page, parametros_url: dict, numero_pedido: str):
    """Maneja las notificaciones POST del TPV"""
    log.info("📨 Procesando notificación del TPV")
    
    respuesta = "ERROR"
    
    try:
        from dorsal_solidario.dorsalsolidario_screen import DorsalSolidarioScreen
        
        if DorsalSolidarioScreen.procesar_callback_tpv(numero_pedido or 'unknown', 'notificacion', parametros_url):
            respuesta = "OK"
            log.info("✅ Notificación procesada correctamente")
        else:
            log.warning("⚠️ Error procesando notificación")
            
    except ImportError as e:
        log.warning(f"⚠️ No se pudo importar DorsalSolidarioScreen: {e}")
    except Exception as e:
        log.error(f"❌ Error procesando notificación: {e}")
    
    # Responder al TPV (Redsys necesita una respuesta)
    page.clean()
    page.add(ft.Text(respuesta))
    page.update()


def _mostrar_pagina_exito(page: ft.Page, numero_pedido: str):
    """Muestra página de confirmación de éxito"""
    page.clean()
    page.title = "Pago Completado"
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=80),
                ft.Text(
                    "✅ ¡Pago Completado!",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.GREEN
                ),
                ft.Text(
                    "Tu dorsal solidario ha sido procesado correctamente.",
                    size=18,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    f"Número de pedido: {numero_pedido or 'N/A'}",
                    size=16,
                    color=ft.colors.GREY_600
                ),
                ft.Text(
                    "Gracias por tu colaboración. ¡Nos vemos en la carrera!",
                    size=16,
                    color=ft.colors.BLUE_600,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=30),
                ft.Row([
                    ft.ElevatedButton(
                        "Cerrar ventana",
                        on_click=lambda e: _cerrar_ventana(page),
                        icon=ft.icons.CLOSE,
                        bgcolor=ft.colors.GREEN_100
                    ),
                    ft.ElevatedButton(
                        "Volver a la aplicación",
                        on_click=lambda e: page.go("/"),
                        icon=ft.icons.HOME,
                        bgcolor=ft.colors.BLUE_100
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
            ),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.colors.WHITE,
            padding=40
        )
    )
    page.update()


def _mostrar_pagina_error(page: ft.Page, mensaje: str):
    """Muestra página de error"""
    page.clean()
    page.title = "Error en el Pago"
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.ERROR, color=ft.colors.RED, size=80),
                ft.Text(
                    "❌ Error en el Pago",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.RED
                ),
                ft.Text(
                    mensaje,
                    size=18,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Puedes intentarlo de nuevo o usar transferencia bancaria.",
                    size=16,
                    color=ft.colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=30),
                ft.Row([
                    ft.ElevatedButton(
                        "Cerrar ventana",
                        on_click=lambda e: _cerrar_ventana(page),
                        icon=ft.icons.CLOSE,
                        bgcolor=ft.colors.RED_100
                    ),
                    ft.ElevatedButton(
                        "Volver a la aplicación", 
                        on_click=lambda e: page.go("/"),
                        icon=ft.icons.HOME,
                        bgcolor=ft.colors.BLUE_100
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
            ),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.colors.WHITE,
            padding=40
        )
    )
    page.update()


def _mostrar_pagina_generica(page: ft.Page, titulo: str, mensaje: str):
    """Muestra una página genérica"""
    page.clean()
    page.title = titulo
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.INFO, color=ft.colors.BLUE, size=64),
                ft.Text(titulo, size=24, weight=ft.FontWeight.BOLD),
                ft.Text(mensaje, size=16),
                ft.ElevatedButton(
                    "Volver al inicio",
                    on_click=lambda e: page.go("/"),
                    icon=ft.icons.HOME
                )
            ]),
            alignment=ft.alignment.center,
            expand=True
        )
    )
    page.update()


def _cerrar_ventana(page: ft.Page):
    """Intenta cerrar la ventana/pestaña"""
    try:
        page.window_close()
    except:
        # Si no se puede cerrar, ir al inicio
        page.go("/")