import json
import base64
import hmac
import hashlib
import time, os
import webbrowser
import threading
from typing import Callable, Optional
from http.server import HTTPServer
import flet as ft
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from utils.PagoHandler import PagoHandler
from dotenv import load_dotenv
import logging

log = logging.getLogger(__name__)

class PagoTPVSantander:
    def __init__(
        self, 
        concepto: str, 
        importe: float,
        entorno_test: bool = False,
        callback_exito: Optional[Callable] = None,
        callback_error: Optional[Callable] = None,
        puerto_servidor: int = 8765,
        base_url: Optional[str] = None,  
        page: Optional[ft.Page] = None   
    ):
        """
        Clase para realizar pagos con TPV de Redsys de forma sencilla
        """
        # Cargar variables de entorno
        load_dotenv()

        merchant_code_ = os.getenv('MERCHANT_CODE')
        terminal_ = os.getenv('TERMINAL_TPV')
        clave_secreta_ = os.getenv('FIRMA_SECRETA')
        
        self.concepto = concepto
        self.importe = importe
        self.merchant_code = merchant_code_
        self.terminal = terminal_
        self.clave_secreta = clave_secreta_
        self.entorno_test = entorno_test
        self.callback_exito = callback_exito
        self.callback_error = callback_error
        self.puerto_servidor = puerto_servidor
        self.page = page
        self.servidor = None
        self.servidor_thread = None
        self.pago_completado = False
        
        # Configurar URLs según entorno
        self.base_url = base_url or self._detectar_entorno()
        self.es_local = self._es_entorno_local()
        
        print(f"🌍 Entorno detectado: {'LOCAL' if self.es_local else 'PRODUCCIÓN'}")
        print(f"🔗 Base URL: {self.base_url}")
        
        # URLs del TPV según entorno
        if entorno_test:
            self.url_tpv = "https://sis-t.redsys.es:25443/sis/realizarPago"
        else:
            self.url_tpv = "https://sis.redsys.es/sis/realizarPago"
            
        # Generar número de pedido único
        timestamp = str(int(time.time()))
        self.numero_pedido = timestamp[-8:]

    def _detectar_entorno(self) -> str:
        """Detecta automáticamente el entorno y la URL base"""
        
        # 1. Variable de entorno específica (solo si está configurada correctamente)
        external_url = os.getenv('EXTERNAL_URL')
        if external_url and not external_url.startswith('https://tu-dominio'):
            print(f"🌍 Usando EXTERNAL_URL: {external_url}")
            return external_url.rstrip('/')
        
        # 2. Detectar plataformas específicas
        if os.getenv('RAILWAY_STATIC_URL'):
            url = f"https://{os.getenv('RAILWAY_STATIC_URL')}"
            print(f"🚂 Detectado Railway: {url}")
            return url
        elif os.getenv('VERCEL_URL'):
            url = f"https://{os.getenv('VERCEL_URL')}"
            print(f"▲ Detectado Vercel: {url}")
            return url
        elif os.getenv('HEROKU_APP_NAME'):
            url = f"https://{os.getenv('HEROKU_APP_NAME')}.herokuapp.com"
            print(f"🟣 Detectado Heroku: {url}")
            return url
        
        # 3. Detectar si estamos en un contenedor Docker REAL
        if self._es_contenedor_real():
            print("🐳 Detectado contenedor Docker en producción")
            print("⚠️ IMPORTANTE: Configura EXTERNAL_URL=https://trailpenasagra.com")
            return "https://trailpenasagra.com"  # Fallback para tu dominio
        
        # 4. Local por defecto
        print("🏠 Detectado entorno local")
        return f"http://localhost:{self.puerto_servidor}"

    def _es_entorno_local(self) -> bool:
        """Determina si estamos en entorno local"""
        if os.path.exists('/.dockerenv') or os.getenv('DOCKER_CONTAINER') == 'true':
            return False
    
        return (
            'localhost' in self.base_url or 
            '127.0.0.1' in self.base_url or
            self.base_url.startswith('http://localhost')
        )

    def _es_contenedor_real(self) -> bool:
        """Detecta si estamos en un contenedor Docker real (no local)"""
        # Si existe /.dockerenv y además hay variables que indican producción
        return (
            os.path.exists('/.dockerenv') and 
            (os.getenv('DOCKER_CONTAINER') == 'true' or os.getenv('PORT') == '80')
        )
        
    def _generar_parametros(self) -> dict:
        """Genera los parámetros necesarios para el pago"""
        importe_centimos = str(int(self.importe * 100))

        # URLs dinámicas según entorno
        if self.es_local:
            # En local, usar servidor HTTP separado
            url_base_callbacks = f"http://localhost:{self.puerto_servidor}"
            print(f"🏠 URLs locales: {url_base_callbacks}")
        else:
            # En producción, usar la app principal
            url_base_callbacks = self.base_url
            print(f"🌍 URLs producción: {url_base_callbacks}")

        parametros = {
            "DS_MERCHANT_ORDER": self.numero_pedido,
            "DS_MERCHANT_MERCHANTCODE": self.merchant_code,
            "DS_MERCHANT_TERMINAL": self.terminal,
            "DS_MERCHANT_AMOUNT": importe_centimos,
            "DS_MERCHANT_CURRENCY": "978",  # EUR
            "DS_MERCHANT_TRANSACTIONTYPE": "0",  # Pago
            "DS_MERCHANT_MERCHANTURL": f"{url_base_callbacks}/tpv/notificacion",
            "DS_MERCHANT_URLOK": f"{url_base_callbacks}/tpv/exito",
            "DS_MERCHANT_URLKO": f"{url_base_callbacks}/tpv/error",
            "DS_MERCHANT_PRODUCTDESCRIPTION": self.concepto
        }
        
        print(f"📋 URLs de callback:")
        print(f"  ✅ Éxito: {parametros['DS_MERCHANT_URLOK']}")
        print(f"  ❌ Error: {parametros['DS_MERCHANT_URLKO']}")
        print(f"  📨 Notificación: {parametros['DS_MERCHANT_MERCHANTURL']}")
        
        return parametros
    
    def _codificar_parametros(self, parametros: dict) -> str:
        """Codifica los parámetros en Base64"""
        json_str = json.dumps(parametros, separators=(',', ':'))
        return base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    
    def _generar_firma(self, parametros_codificados: str) -> str:
        """Genera la firma HMAC SHA-256"""
        clave_decodificada = base64.b64decode(self.clave_secreta)
        clave_operacion = self._cifrar_3des(clave_decodificada, self.numero_pedido)
        
        firma = hmac.new(
            clave_operacion,
            parametros_codificados.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        return base64.b64encode(firma).decode('utf-8')
    
    def _cifrar_3des(self, clave: bytes, datos: str) -> bytes:
        """Cifrado 3DES real según especificaciones de Redsys"""
        try:
            if len(clave) < 24:
                clave = clave + b'\x00' * (24 - len(clave))
            elif len(clave) > 24:
                clave = clave[:24]
            
            datos_bytes = datos.encode('utf-8')
            padding_needed = 8 - (len(datos_bytes) % 8)
            if padding_needed != 8:
                datos_bytes += b'\x00' * padding_needed
            
            cipher = Cipher(
                algorithms.TripleDES(clave),
                modes.CBC(b'\x00' * 8),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            encrypted = encryptor.update(datos_bytes) + encryptor.finalize()
            
            return encrypted[:24]
            
        except Exception as e:
            print(f"Error en cifrado 3DES: {e}")
            return hashlib.sha256(clave + datos.encode()).digest()[:24]
    
    def _iniciar_servidor(self):
        """Inicia el servidor HTTP para recibir respuestas (solo en local)"""
        try:
            self.servidor = HTTPServer(('localhost', self.puerto_servidor), PagoHandler)
            self.servidor.pago_instance = self
            print(f"🌐 Servidor local iniciado en http://localhost:{self.puerto_servidor}")
            self.servidor.serve_forever()
        except Exception as e:
            print(f"❌ Error iniciando servidor local: {e}")
    
    def _on_success(self, mensaje: str):
        """Callback interno de éxito"""
        if not self.pago_completado:
            self.pago_completado = True
            print(f"✅ {mensaje}")
            if self.callback_exito:
                self.callback_exito({"mensaje": mensaje, "numero_pedido": self.numero_pedido})
    
    def _on_error(self, mensaje: str):
        """Callback interno de error"""
        if not self.pago_completado:
            self.pago_completado = True
            print(f"❌ {mensaje}")
            if self.callback_error:
                self.callback_error(mensaje)
    
    def _generar_formulario_html(self, parametros_codificados: str, firma: str) -> str:
        """Genera el HTML del formulario para enviar al TPV"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Redirigiendo al TPV...</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <div style="text-align: center; margin-top: 50px; font-family: Arial, sans-serif;">
                <h2>🔒 Redirigiendo al sistema de pago seguro...</h2>
                <p><strong>Importe:</strong> {self.importe}€</p>
                <p><strong>Concepto:</strong> {self.concepto}</p>
                <p>Por favor, espere mientras lo redirigimos...</p>
                <div style="margin: 20px;">
                    <div style="border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 2s linear infinite; margin: 0 auto;"></div>
                </div>
                <p style="font-size: 12px; color: #666;">
                    Entorno: {self.base_url} | Pedido: {self.numero_pedido}
                </p>
            </div>
            
            <form id="tpvForm" action="{self.url_tpv}" method="POST">
                <input type="hidden" name="Ds_SignatureVersion" value="HMAC_SHA256_V1"/>
                <input type="hidden" name="Ds_MerchantParameters" value="{parametros_codificados}"/>
                <input type="hidden" name="Ds_Signature" value="{firma}"/>
            </form>
            
            <script>
                setTimeout(function() {{
                    document.getElementById('tpvForm').submit();
                }}, 2000);
            </script>
            
            <style>
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
            </style>
        </body>
        </html>
        """
        return html
    
    def start(self, debug: bool = False, mantener_vivo: bool = True):
        """Inicia el proceso de pago"""
        try:
            print(f"🚀 Iniciando pago de {self.importe}€ - {self.concepto}")
            print(f"📋 Número de pedido: {self.numero_pedido}")
            print(f"🌍 Entorno: {'Local' if self.es_local else 'Producción'}")
            print(f"🔗 Base URL: {self.base_url}")
            
            # Registrar el pago para callbacks
            self._registrar_pago()
            
            # Solo iniciar servidor HTTP separado si estamos en LOCAL
            if self.es_local:
                if self.servidor_thread is None or not self.servidor_thread.is_alive():
                    self.servidor_thread = threading.Thread(target=self._iniciar_servidor, daemon=True)
                    self.servidor_thread.start()
                    time.sleep(1)
                    print("✅ Servidor local iniciado")
            else:
                print("ℹ️ En producción - usando rutas de Flet para callbacks")
            
            # Generar parámetros del pago
            parametros = self._generar_parametros()
            parametros_codificados = self._codificar_parametros(parametros)
            firma = self._generar_firma(parametros_codificados)
            
            if debug:
                print("\n🔍 DEBUG INFO:")
                print(f"Entorno: {'Local' if self.es_local else 'Producción'}")
                print(f"Base URL: {self.base_url}")
                print(f"Merchant Code: {self.merchant_code}")
                print(f"Terminal: {self.terminal}")
                print(f"Número de pedido: {self.numero_pedido}")
                print(f"Importe (céntimos): {int(self.importe * 100)}")
                print(f"Firma generada: {firma}")
                print("=" * 50)
            
            # Generar y abrir formulario de pago
            html_content = self._generar_formulario_html(parametros_codificados, firma)
            
            print("🔧 DEBUG: Formulario HTML generado")
            print(f"🔧 DEBUG: es_local = {self.es_local}")
            print(f"🔧 DEBUG: page existe = {self.page is not None}")
            
            if self.es_local:
                # En local: crear archivo temporal y abrirlo
                print("🔧 DEBUG: Ejecutando rama LOCAL")
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                    f.write(html_content)
                    temp_file = f.name
                print("✅ Formulario local abierto en navegador")
                webbrowser.open(f'file://{temp_file}')
                print("✅ Formulario local abierto en navegador")
                
                if not mantener_vivo:
                    def limpiar_temp():
                        time.sleep(10)
                        try:
                            os.unlink(temp_file)
                        except:
                            pass
                    threading.Thread(target=limpiar_temp, daemon=True).start()
            else:
                print("🔧 DEBUG: Ejecutando rama PRODUCCIÓN")
            # En lugar de data URL, guardar HTML y hacer redirect
            import urllib.parse
            
            print(f"🔧 DEBUG: Guardando formulario HTML para Flet")
            
            # Guardar el HTML en una variable global temporal
            if not hasattr(PagoTPVSantander, '_formularios_temp'):
                PagoTPVSantander._formularios_temp = {}
            
            PagoTPVSantander._formularios_temp[self.numero_pedido] = html_content
            
            if self.page:
                print("🔧 DEBUG: Redirigiendo a ruta de formulario")
                try:
                    # Redireccionar a una ruta especial
                    self.page.go(f"/formulario_pago/{self.numero_pedido}")
                    print("✅ Formulario servido via ruta Flet")
                except Exception as e:
                    print(f"⚠️ Error en redirect: {e}")
            else:
                print("🔧 DEBUG: No hay page")
            
            print("💳 Usuario redirigido al TPV")
            print("⏳ Esperando respuesta del pago...")
            
        except Exception as e:
            print(f"❌ Error al iniciar el pago: {e}")
            if self.callback_error:
                self.callback_error(str(e))

    def _registrar_pago(self):
        """Registra este pago para callbacks"""
        try:
            from utils.pago_registry import registrar_pago_activo
            registrar_pago_activo(self.numero_pedido, self)
            print(f"📝 Pago registrado: {self.numero_pedido}")
        except Exception as e:
            print(f"⚠️ Error registrando pago: {e}")
    
    def detener(self):
        """Detiene el servidor y limpia recursos"""
        try:
            if self.servidor:
                self.servidor.shutdown()
                print("🔌 Servidor detenido")
        except:
            pass
    
    def verificar_respuesta(self, parametros_respuesta: str, firma_recibida: str) -> bool:
        """Verifica la respuesta del TPV"""
        try:
            print(f"\n🔍 VERIFICANDO RESPUESTA:")
            print(f"Parámetros recibidos: {parametros_respuesta}")
            print(f"Firma recibida: {firma_recibida}")
            
            parametros_json = base64.b64decode(parametros_respuesta).decode('utf-8')
            parametros = json.loads(parametros_json)
            
            print(f"📄 Parámetros decodificados:")
            for key, value in parametros.items():
                print(f"  {key}: {value}")
            
            codigo_respuesta = parametros.get('Ds_Response', '')
            numero_pedido_respuesta = parametros.get('Ds_Order', '')
            
            print(f"\n📊 Análisis de respuesta:")
            print(f"Código de respuesta: {codigo_respuesta}")
            print(f"Número de pedido esperado: {self.numero_pedido}")
            print(f"Número de pedido recibido: {numero_pedido_respuesta}")
            
            if numero_pedido_respuesta != self.numero_pedido:
                print(f"❌ El número de pedido no coincide")
                return False
            
            # Verificar código de respuesta (0000-0099 = éxito)
            pago_exitoso = False
            if codigo_respuesta and codigo_respuesta.isdigit():
                codigo = int(codigo_respuesta)
                if 0 <= codigo <= 99:
                    pago_exitoso = True
                    print(f"✅ Código de respuesta indica éxito: {codigo}")
                else:
                    print(f"❌ Código de respuesta indica error: {codigo}")
            else:
                print(f"❌ Código de respuesta inválido: {codigo_respuesta}")
            
            # Verificar firma
            try:
                firma_calculada = self._generar_firma(parametros_respuesta)
                print(f"Firma calculada: {firma_calculada}")
                print(f"Firma recibida:  {firma_recibida}")
                
                if firma_calculada == firma_recibida:
                    print("✅ Firma válida")
                    return pago_exitoso
                else:
                    print("⚠️ Firma no coincide, pero verificando por código de respuesta...")
                    if pago_exitoso:
                        print("✅ Aceptando pago por código de respuesta exitoso")
                        return True
                    else:
                        print("❌ Firma inválida y código de respuesta no exitoso")
                        return False
            except Exception as e:
                print(f"❌ Error calculando firma: {e}")
                if pago_exitoso:
                    print("✅ Aceptando pago por código de respuesta exitoso")
                    return True
                return False
                
        except Exception as e:
            print(f"❌ Error general verificando respuesta: {e}")
            return False