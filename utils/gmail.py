import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

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
    
    def crear_mensaje_html(self, nombre):
        """
        Crea el contenido HTML del email
        
        Args:
            nombre (str): Nombre del destinatario
            
        Returns:
            str: Contenido HTML del mensaje
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
                .logo {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo img {{
                    max-width: 200px;
                    height: auto;
                }}
                .saludo {{
                    font-size: 18px;
                    color: #2c5530;
                    margin-bottom: 20px;
                }}
                .contenido {{
                    background-color: #f9f9f9;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #2c5530;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="logo">
                <!-- Aquí puedes poner tu logo como imagen -->
                <h1 style="color: #2c5530; font-size: 28px;">🏔️ TRAIL PEÑASAGRA</h1>
            </div>
            
            <div class="saludo">
                ¡Hola {nombre}!
            </div>
            
            <div class="contenido">
                <p><strong>¡Enhorabuena!</strong> Estás preinscrito en el <strong>Trail Peñasagra</strong>.</p>
                
                <p>Tu preinscripción ha sido registrada correctamente. En cuanto sea verificado el pago de la carrera, 
                recibirás otro email de confirmación de inscripción con tu <strong>número de dorsal</strong> asignado.</p>
                
                <p>Mientras tanto, te recomendamos que:</p>
                <ul>
                    <li>Revises toda la información de la carrera en nuestra web</li>
                    <li>Comiences a preparar tu entrenamiento</li>
                    <li>Sigas nuestras redes sociales para estar al día de las novedades</li>
                </ul>
                
                <p>Si tienes alguna duda, no dudes en contactar con nosotros.</p>
                
                <p><strong>¡Nos vemos en la montaña!</strong></p>
            </div>
            
            <div class="footer">
                <p>Trail Peñasagra - Organización</p>
                <p>Este es un email automático, por favor no responder a este mensaje.</p>
            </div>
        </body>
        </html>
        """
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
            
            print(f"✅ Mensaje de contacto recibido de {nombre_usuario} ({email_usuario})")
            return True
            
        except Exception as e:
            print(f"❌ Error al enviar mensaje de contacto: {str(e)}")
            return False
    
    def enviar_email(self, email_destinatario, nombre):
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
            mensaje["To"] = email_destinatario
            mensaje["Subject"] = "Preinscrito en el Trail Peñasagra"
            
            # Crear contenido HTML
            html_content = self.crear_mensaje_html(nombre)
            part_html = MIMEText(html_content, "html")
            mensaje.attach(part_html)
            
            # Crear conexión segura y enviar
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.gmail_user, self.gmail_password)
                server.sendmail(self.gmail_user, email_destinatario, mensaje.as_string())
            
            print(f"✅ Email enviado correctamente a {email_destinatario}")
            return True
            
        except Exception as e:
            print(f"❌ Error al enviar email: {str(e)}")
            return False

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar credenciales
    GMAIL_USER = "asociacionpenasagra@gmail.com"
    GMAIL_PASSWORD = "cfri bxoq hsub uegt"
    
    
    # Crear instancia del Objeto Gmail --> Obligatorio hacerlo antes de enviar emails
    email_send = Gmail(GMAIL_USER, GMAIL_PASSWORD)
    
    # Enviar email de preinscripción
    email_send.enviar_email("jr.cosio1@gmail.com", "Jose Ramon Blanco")
    
    # Enviar mensaje de contacto (auto-envío)
    # email_send.enviar_contacto(
    #     nombre_usuario="María García",
    #     email_usuario="maria@example.com", 
    #     asunto_usuario="Consulta sobre la carrera",
    #     comentario="Hola, me gustaría saber más información sobre las categorías disponibles y los horarios de salida. ¿Hay algún límite de edad? Gracias."
    # )
