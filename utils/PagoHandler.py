
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


class PagoHandler(BaseHTTPRequestHandler):
    """Manejador HTTP para recibir respuestas del TPV"""
    
    def do_GET(self):
        """Maneja las respuestas GET (URLs de retorno)"""
        if hasattr(self.server, 'pago_instance'):
            pago = self.server.pago_instance
            
            if '/exito' in self.path:
                # Extraer parámetros de la URL si los hay
                if '?' in self.path:
                    query_string = self.path.split('?')[1]
                    params = parse_qs(query_string)
                    
                    # Si hay parámetros, procesarlos
                    if 'Ds_MerchantParameters' in params and 'Ds_Signature' in params:
                        parametros_codificados = params['Ds_MerchantParameters'][0]
                        firma_recibida = params['Ds_Signature'][0]
                        
                        if pago.verificar_respuesta(parametros_codificados, firma_recibida):
                            pago._on_success("Pago completado con éxito")
                        else:
                            pago._on_error("Error en la verificación del pago")
                    else:
                        pago._on_success("Pago completado (sin parámetros de verificación)")
                else:
                    pago._on_success("Pago completado")
                    
                self._send_response("✅ Pago completado con éxito", "success")
                
            elif '/error' in self.path:
                pago._on_error("Pago cancelado por el usuario")
                self._send_response("❌ Pago cancelado", "error")
                
            else:
                self._send_response("🔄 Página de estado del pago", "info")
        else:
            self._send_response("❓ Servidor de pagos activo", "info")
    
    def do_POST(self):
        """Maneja las notificaciones POST del TPV"""
        try:
            # Leer datos del POST
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            
            if hasattr(self.server, 'pago_instance'):
                pago = self.server.pago_instance
                
                if 'Ds_MerchantParameters' in params and 'Ds_Signature' in params:
                    parametros_codificados = params['Ds_MerchantParameters'][0]
                    firma_recibida = params['Ds_Signature'][0]
                    
                    print(f"\n📨 Notificación recibida del TPV:")
                    print(f"Parámetros: {parametros_codificados}")
                    print(f"Firma: {firma_recibida}")
                    
                    if pago.verificar_respuesta(parametros_codificados, firma_recibida):
                        pago._on_success("Pago verificado correctamente")
                        self._send_response("OK", "text")
                    else:
                        pago._on_error("Error en la verificación del pago")
                        self._send_response("ERROR", "text")
                else:
                    self._send_response("ERROR - Parámetros faltantes", "text")
            else:
                self._send_response("ERROR - No hay instancia de pago", "text")
                
        except Exception as e:
            print(f"❌ Error procesando notificación: {e}")
            self._send_response("ERROR", "text")
    
    def _send_response(self, message: str, type_: str = "info"):
        """Envía una respuesta HTTP"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        Colors = {
            "success": "#4CAF50",
            "error": "#f44336", 
            "info": "#2196F3",
            "text": "#333"
        }
        
        if type_ == "text":
            self.wfile.write(message.encode('utf-8'))
        else:
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Estado del Pago</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                    .message {{ color: {Colors[type_]}; font-size: 24px; margin: 20px; }}
                    .button {{ background: #2196F3; color: white; padding: 10px 20px; 
                             text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
                </style>
                
            </head>
            <body>
                <div class="message">{message}</div>
                <a>Cierra esta pestaña ventana</a>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Silenciar logs del servidor HTTP"""
        pass