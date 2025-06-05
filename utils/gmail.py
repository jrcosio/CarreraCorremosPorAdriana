import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import logging
import textwrap

log = logging.getLogger(__name__)
# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Gmail:
    """
    Clase para enviar emails de preinscripción al Trail Peñasagra usando Gmail
    """
    
    def __init__(self, gmail_user, gmail_password):
        """
        Inicializa la clase con las credenciales de Gmail
        
        Args:
            gmail_user (str): Tu dirección de Gmail
            gmail_password (str): Tu contraseña de aplicación de Gmail
        """
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def crear_mensaje_html(self, inscrito) -> str:  # type: ignore[override]
        """Devuelve el HTML listo para enviar.

        Args:
            inscrito: Objeto con los datos del corredor.
        """

        # Usamos textwrap.dedent para eliminar la indentación extra y evitar que aparezcan
        # espacios no deseados en el código resultante.
        html: str = textwrap.dedent(f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8" />
                <title>Preinscripción Trail Peñasagra</title>
            </head>
            <body style="margin:0;padding:0;background:#f0f4f8;">
                <!-- Contenedor principal -->
                <div style="max-width:600px;margin:0 auto;font-family:Helvetica,Arial,sans-serif;color:#333;">

                <!-- Cabecera -->
                <div style="background:linear-gradient(90deg,#16a34a 0%, #4ade80 100%);padding:24px 0;text-align:center;border-radius:0 0 12px 12px;">
                    <h1 style="margin:0;font-size:28px;color:#fff;">¡Enhorabuena, {inscrito.nombre}!</h1>
                    <p style="margin:8px 0 0;font-size:18px;color:#e0fbe2;">Tu preinscripción está confirmada</p>
                </div>

                <!-- Tarjeta principal -->
                <div style="background:#ffffff;padding:32px;border-radius:12px;box-shadow:0 4px 14px rgba(0,0,0,0.08);margin-top:-12px;">
                    <p style="font-size:16px;line-height:1.5;">
                    Tu preinscripción en el <strong>Trail Peñasagra - Corremos por Adriana</strong> se ha registrado correctamente.
                    </p>
                    <p style="font-size:16px;line-height:1.5;">
                    Estamos trabajando para, en breve, disponer de un sistema automático de pago con tarjeta o <em>Bizum</em>. En los próximos días recibirás un correo para que finalices el proceso de inscripción realizando el pago.
                    </p>

                    <!-- Datos de la inscripción -->
                    <h2 style="font-size:20px;margin:24px 0 12px;border-bottom:2px solid #16a34a;display:inline-block;padding-bottom:4px;">Datos de tu inscripción</h2>

                    <table role="presentation" cellpadding="8" cellspacing="0" width="100%" style="border-collapse:collapse;font-size:14px;">
                    <tbody>
                        <tr style="background:#f8fafc;"><td><strong>Nombre</strong></td><td>{inscrito.nombre} {inscrito.apellidos}</td></tr>
                        <tr><td><strong>Sexo</strong></td><td>{inscrito.sexo}</td></tr>
                        <tr style="background:#f8fafc;"><td><strong>Fecha de nacimiento</strong></td><td>{inscrito.fecha_nacimiento.strftime('%d/%m/%Y')}</td></tr>
                        <tr><td><strong>Teléfono</strong></td><td>{inscrito.telefono}</td></tr>
                        <tr style="background:#f8fafc;"><td><strong>Email</strong></td><td>{inscrito.email}</td></tr>
                        <tr><td><strong>Tipo de documento</strong></td><td>{inscrito.tipo_documento}</td></tr>
                        <tr style="background:#f8fafc;"><td><strong>N.º de documento</strong></td><td>{inscrito.numero_documento}</td></tr>
                        <tr><td><strong>Dirección</strong></td><td>{inscrito.direccion}</td></tr>
                        <tr style="background:#f8fafc;"><td><strong>CC. AA.</strong></td><td>{inscrito.ccaa}</td></tr>
                        <tr><td><strong>Municipio</strong></td><td>{inscrito.municipio}</td></tr>
                        <tr style="background:#f8fafc;"><td><strong>Tipo de carrera</strong></td><td>{inscrito.tipo_carrera}</td></tr>
                        <tr><td><strong>Talla camiseta</strong></td><td>{inscrito.talla}</td></tr>
                        <tr style="background:#f8fafc;"><td><strong>Contacto emergencia</strong></td><td>{inscrito.contacto_emergencia}</td></tr>
                        <tr><td><strong>Tel. emergencia</strong></td><td>{inscrito.telefono_emergencia}</td></tr>
                        <tr style="background:#f8fafc;"><td><strong>Edición</strong></td><td>{inscrito.edicion}</td></tr>
                        <tr><td><strong>Dorsal</strong></td><td>{inscrito.dorsal or '<em>Se asignará al confirmar el pago</em>'}</td></tr>
                    </tbody>
                    </table>

                    <!-- Recomendaciones -->
                    <div style="margin-top:24px;">
                    <p style="font-size:16px;"><strong>Mientras tanto, te recomendamos que:</strong></p>
                    <ul style="font-size:15px;line-height:1.5;margin-left:20px;">
                        <li>Revises toda la información de la carrera en nuestra web.</li>
                        <li>Comiences a preparar tu entrenamiento.</li>
                        <li>Sigas nuestras redes sociales para estar al día de las novedades.</li>
                    </ul>
                    </div>

                    <p style="font-size:16px;line-height:1.5;">Si tienes cualquier duda, no dudes en contactar con nosotros.</p>
                    <p style="font-size:18px;font-weight:bold;text-align:center;margin-top:32px;">¡Nos vemos en la montaña!</p>
                </div>
                </div>
            </body>
            </html>
        """)
        return html

    
    def crear_mensaje_contacto_html(self, nombre_usuario, email_usuario, asunto_usuario, comentario):
        """
        Crea el contenido HTML del email de contacto
        
        Args:
            nombre_usuario (str): Nombre del usuario que contacta
            email_usuario (str): Email del usuario que contacta
            asunto_usuario (str): Asunto del mensaje
            comentario (str): Comentario del usuario
            
        Returns:
            str: Contenido HTML del mensaje de contacto
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #2c5530;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px 8px 0 0;
                }}
                .contenido {{
                    background-color: #f9f9f9;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 0 0 8px 8px;
                }}
                .campo {{
                    margin-bottom: 15px;
                    padding: 10px;
                    background-color: white;
                    border-radius: 4px;
                    border-left: 4px solid #2c5530;
                }}
                .label {{
                    font-weight: bold;
                    color: #2c5530;
                    display: block;
                    margin-bottom: 5px;
                }}
                .comentario {{
                    background-color: #fff;
                    padding: 15px;
                    border-radius: 4px;
                    border: 1px solid #ddd;
                    white-space: pre-wrap;
                }}
                .responder {{
                    background-color: #e8f5e8;
                    padding: 15px;
                    border-radius: 4px;
                    margin-top: 20px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>📧 Nuevo mensaje de contacto - Trail Peñasagra</h2>
            </div>
            
            <div class="contenido">
                <div class="campo">
                    <span class="label">👤 Nombre:</span>
                    {nombre_usuario}
                </div>
                
                <div class="campo">
                    <span class="label">📧 Email:</span>
                    <a href="mailto:{email_usuario}">{email_usuario}</a>
                </div>
                
                <div class="campo">
                    <span class="label">📝 Asunto:</span>
                    {asunto_usuario}
                </div>
                
                <div class="campo">
                    <span class="label">💬 Comentario:</span>
                    <div class="comentario">{comentario}</div>
                </div>
                
                <div class="responder">
                    <p><strong>💡 Para responder:</strong> Simplemente haz clic en el email del usuario para abrir tu cliente de correo</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def enviar_contacto(self, nombre_usuario, email_usuario, asunto_usuario, comentario):
        """
        Envía un email de contacto al administrador (auto-envío)
        
        Args:
            nombre_usuario (str): Nombre del usuario que contacta
            email_usuario (str): Email del usuario que contacta
            asunto_usuario (str): Asunto del mensaje
            comentario (str): Comentario del usuario
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            # Crear el mensaje - se envía al mismo email configurado
            mensaje = MIMEMultipart("alternative")
            mensaje["From"] = self.gmail_user
            mensaje["To"] = self.gmail_user  # Auto-envío
            mensaje["Reply-To"] = email_usuario  # Para poder responder fácilmente
            mensaje["Subject"] = f"Contacto Web: {asunto_usuario} - {nombre_usuario}"
            
            # Crear contenido HTML
            html_content = self.crear_mensaje_contacto_html(
                nombre_usuario, email_usuario, asunto_usuario, comentario
            )
            part_html = MIMEText(html_content, "html")
            mensaje.attach(part_html)
            
            # Crear conexión segura y enviar
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.gmail_user, self.gmail_password)
                server.sendmail(self.gmail_user, self.gmail_user, mensaje.as_string())
            
            log.info(f"Mensaje de contacto enviado correctamente: {asunto_usuario} - {nombre_usuario}")
            return True
            
        except Exception as e:
            log.error(f"Error al enviar mensaje de contacto: {str(e)}")
            return False
    
    
    def enviar_email_inscrito(self, inscrito) -> str:
        """
        Envía el email de preinscripción
        
        Args:
            email_destinatario (str): Email del destinatario
            nombre (str): Nombre del destinatario
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            # Crear el mensaje
            mensaje = MIMEMultipart("alternative")
            mensaje["From"] = self.gmail_user
            mensaje["To"] = inscrito.email
            mensaje["Subject"] = "Preinscrito en el Trail Peñasagra"
            
            # Crear contenido HTML
            html_content = self.crear_mensaje_html(inscrito)
            part_html = MIMEText(html_content, "html")
            mensaje.attach(part_html)
            
            # Crear conexión segura y enviar
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.gmail_user, self.gmail_password)
                server.sendmail(self.gmail_user, inscrito.email, mensaje.as_string())
            
            log.info(f"Email enviado correctamente a {inscrito.email} para {inscrito.nombre}")
            return True
            
        except Exception as e:
            log.error(f"Error al enviar email: {str(e)}")
            return False
    
    # def enviar_email(self, email_destinatario, nombre):
    #     """
    #     Envía el email de preinscripción
        
    #     Args:
    #         email_destinatario (str): Email del destinatario
    #         nombre (str): Nombre del destinatario
            
    #     Returns:
    #         bool: True si se envió correctamente, False en caso contrario
    #     """
    #     try:
    #         # Crear el mensaje
    #         mensaje = MIMEMultipart("alternative")
    #         mensaje["From"] = self.gmail_user
    #         mensaje["To"] = email_destinatario
    #         mensaje["Subject"] = "Preinscrito en el Trail Peñasagra"
            
    #         # Crear contenido HTML
    #         html_content = self.crear_mensaje_html(nombre)
    #         part_html = MIMEText(html_content, "html")
    #         mensaje.attach(part_html)
            
    #         # Crear conexión segura y enviar
    #         context = ssl.create_default_context()
    #         with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
    #             server.starttls(context=context)
    #             server.login(self.gmail_user, self.gmail_password)
    #             server.sendmail(self.gmail_user, email_destinatario, mensaje.as_string())
            
    #         log.info(f"Email enviado correctamente a {email_destinatario} para {nombre}")
    #         return True
            
    #     except Exception as e:
    #         log.error(f"Error al enviar email: {str(e)}")
    #         return False

# Ejemplo de uso
# if __name__ == "__main__":
    # Configurar credenciales
    # GMAIL_USER = "asociacionpenasagra@gmail.com"
    # GMAIL_PASSWORD = "cfri bxoq hsub uegt"
    
    
    # # Crear instancia del Objeto Gmail --> Obligatorio hacerlo antes de enviar emails
    # email_send = Gmail(GMAIL_USER, GMAIL_PASSWORD)
    
    # # Enviar email de preinscripción
    # email_send.enviar_email("jr.cosio1@gmail.com", "Jose Ramon Blanco")
    
    # Enviar mensaje de contacto (auto-envío)
    # email_send.enviar_contacto(
    #     nombre_usuario="María García",
    #     email_usuario="maria@example.com", 
    #     asunto_usuario="Consulta sobre la carrera",
    #     comentario="Hola, me gustaría saber más información sobre las categorías disponibles y los horarios de salida. ¿Hay algún límite de edad? Gracias."
    # )
