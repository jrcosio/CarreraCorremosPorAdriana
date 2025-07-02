import stripe
import webbrowser
import threading
import time
import logging
from typing import Callable, Optional

log = logging.getLogger(__name__)

class PagoStripe:
    """
    Clase de pago con Stripe que replica la interfaz de PagoTPVSantander
    Drop-in replacement para usar en aplicaciones Flet
    Compatible con modo web (Docker) y modo desktop
    """
    
    def __init__(
        self,
        concepto: str,
        importe: float,
        entorno_test: bool = True,
        callback_exito: Optional[Callable] = None,
        callback_error: Optional[Callable] = None,
        api_key_test: str = "sk_test_51xxxxx",  # Tu clave de test
        api_key_prod: str = "sk_live_51xxxxx",   # Tu clave de producción
        page = None  # 👈 AÑADIDO para Flet web mode
    ):
        """
        Inicializar el procesador de pagos Stripe
        
        Args:
            concepto: Descripción del pago
            importe: Cantidad en euros
            entorno_test: True para test, False para producción
            callback_exito: Función a llamar cuando el pago sea exitoso
            callback_error: Función a llamar cuando haya error
            api_key_test: Clave secreta de test de Stripe
            api_key_prod: Clave secreta de producción de Stripe
            page: Referencia a ft.Page para modo web (Docker/navegador)
        """
        self.concepto = concepto
        self.importe = importe
        self.entorno_test = entorno_test
        self.callback_exito = callback_exito
        self.callback_error = callback_error
        self.page = page  # 👈 GUARDAR referencia a page
        
        # Configurar Stripe
        if entorno_test:
            stripe.api_key = api_key_test
            log.info("Usando entorno de TEST de Stripe")
        else:
            stripe.api_key = api_key_prod
            log.info("Usando entorno de PRODUCCIÓN de Stripe")
        
        # Estado del pago
        self.pago_completado = False
        self.session_id = None
        self.numero_pedido = None
        self._verificando = False
        
        # Generar número de pedido
        import time
        timestamp = str(int(time.time()))
        self.numero_pedido = timestamp[-8:]  # Últimos 8 dígitos del timestamp
        
        log.info(f"PagoStripe inicializado: {concepto}, {importe}€, Test: {entorno_test}")
    
    def start(self, debug: bool = False, mantener_vivo: bool = False):
        """
        Iniciar el proceso de pago
        
        Args:
            debug: Mostrar información de debug
            mantener_vivo: Parámetro de compatibilidad (no usado en Stripe)
        """
        try:
            log.info(f"Iniciando pago Stripe: {self.concepto} - {self.importe}€")
            
            if debug:
                log.info(f"Número de pedido: {self.numero_pedido}")
            
            # Crear sesión de Stripe Checkout
            session = self._crear_checkout_session()
            
            if session:
                self.session_id = session['session_id']
                
                log.info(f"Sesión creada: {self.session_id}")
                
                # Abrir navegador - USAR EL MÉTODO CORRECTO según el modo
                if self.page is not None:
                    # Modo web de Flet - usar page.launch_url()
                    log.info("Abriendo navegador (modo web Flet)...")
                    self.page.launch_url(session['checkout_url'])
                else:
                    # Modo desktop - usar webbrowser como fallback
                    log.info("Abriendo navegador (modo desktop)...")
                    webbrowser.open(session['checkout_url'])
                
                # Iniciar verificación en background
                self._iniciar_verificacion()
                
            else:
                log.error("Error creando sesión de checkout")
                if self.callback_error:
                    self.callback_error("Error creando sesión de pago")
                    
        except Exception as e:
            log.error(f"Error en start(): {e}")
            if self.callback_error:
                self.callback_error(f"Error iniciando pago: {str(e)}")
    
    def _crear_checkout_session(self):
        """Crear sesión de Stripe Checkout"""
        try:
            # Convertir euros a centavos
            amount_cents = int(self.importe * 100)
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',  # Euros
                        'product_data': {
                            'name': self.concepto,
                            'description': f'Pedido #{self.numero_pedido}'
                        },
                        'unit_amount': amount_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                # URLs dummy (obligatorias pero no usadas)
                success_url='https://jrcosio.github.io/stripe-payment-pages/success.html?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='https://jrcosio.github.io/stripe-payment-pages/cancel.html',
                metadata={
                    'numero_pedido': self.numero_pedido,
                    'concepto': self.concepto
                }
            )
            
            return {
                'success': True,
                'checkout_url': session.url,
                'session_id': session.id
            }
            
        except stripe.error.StripeError as e:
            log.error(f"Error de Stripe: {e}")
            return None
        except Exception as e:
            log.error(f"Error creando checkout: {e}")
            return None
    
    def _iniciar_verificacion(self):
        """Iniciar verificación del pago en background"""
        
        def verificar_pago():
            self._verificando = True
            intentos = 0
            max_intentos = 120  # 10 minutos (120 * 5 segundos)
            
            log.info("Iniciando verificación de pago...")
            
            while self._verificando and intentos < max_intentos and not self.pago_completado:
                try:
                    # Verificar estado del pago
                    session = stripe.checkout.Session.retrieve(self.session_id)
                    
                    if session.payment_status == 'paid':
                        # ¡Pago exitoso!
                        log.info("¡Pago completado con éxito!")
                        self.pago_completado = True
                        self._verificando = False
                        
                        # Preparar datos para callback
                        datos_pago = {
                            'mensaje': 'Pago realizado correctamente',
                            'numero_pedido': self.numero_pedido,
                            'importe': self.importe,
                            'concepto': self.concepto,
                            'payment_intent': session.payment_intent,
                            'customer_email': session.customer_details.email if session.customer_details else None
                        }
                        
                        if self.callback_exito:
                            self.callback_exito(datos_pago)
                        
                        break
                        
                    elif session.payment_status == 'unpaid':
                        # Seguir esperando
                        intentos += 1
                        if intentos % 12 == 0:  # Log cada minuto
                            log.info(f"Esperando pago... ({intentos//12} min)")
                        time.sleep(5)
                        
                    else:
                        # Estado inesperado
                        log.warning(f"Estado inesperado: {session.payment_status}")
                        self._verificando = False
                        
                        if self.callback_error:
                            self.callback_error(f"Estado de pago inesperado: {session.payment_status}")
                        break
                        
                except stripe.error.StripeError as e:
                    log.error(f"Error verificando pago: {e}")
                    self._verificando = False
                    
                    if self.callback_error:
                        self.callback_error(f"Error verificando pago: {str(e)}")
                    break
                    
                except Exception as e:
                    log.error(f"Error inesperado verificando pago: {e}")
                    self._verificando = False
                    
                    if self.callback_error:
                        self.callback_error(f"Error inesperado: {str(e)}")
                    break
            
            # Timeout
            if intentos >= max_intentos:
                log.warning("Timeout verificando pago")
                self._verificando = False
                
                if self.callback_error:
                    self.callback_error("Tiempo agotado verificando el pago")
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=verificar_pago)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """Detener la verificación del pago"""
        self._verificando = False
        log.info("Verificación de pago detenida")
    
    def get_estado(self):
        """Obtener estado actual del pago"""
        return {
            'pago_completado': self.pago_completado,
            'verificando': self._verificando,
            'session_id': self.session_id,
            'numero_pedido': self.numero_pedido
        }

# ===== CONFIGURACIÓN RÁPIDA =====

class ConfigStripe:
    """Configuración centralizada de Stripe"""
    
    # 🔑 CAMBIA ESTAS CLAVES POR LAS TUYAS
    API_KEY_TEST = "sk_test_51xxxxx"  # Tu clave secreta de test
    API_KEY_PROD = "sk_live_51xxxxx"  # Tu clave secreta de producción
    
    @classmethod
    def configurar_claves(cls, test_key: str, prod_key: str):
        """Configurar claves globalmente"""
        cls.API_KEY_TEST = test_key
        cls.API_KEY_PROD = prod_key

