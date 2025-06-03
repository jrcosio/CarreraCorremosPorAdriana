import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

class EmailSender:
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
        
    def enviar_info_contacto(self, email_destinatario, nombre, asunto, texto):
        """
        Envía un email de contacto con información adicional
        
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
            mensaje["To"] = self.gmail_user
            mensaje["Subject"] = f"Desde la WEB: [{asunto}]"
            
            # Crear contenido HTML
            html_content = f"""
            <p>Soy {nombre},</p>
            <p>{texto}</p>
            """
            part_html = MIMEText(html_content, "html")
            mensaje.attach(part_html)
            
            # Crear conexión segura y enviar
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.gmail_user, self.gmail_password)
                server.sendmail(self.gmail_user, self.gmail_user, mensaje.as_string())
            
            print(f"✅ Información de contacto enviada a {email_destinatario}")
            return True
            
        except Exception as e:
            print(f"❌ Error al enviar información de contacto: {str(e)}")
            return False

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar credenciales
    GMAIL_USER = "asociacionpenasagra@gmail.com"
    GMAIL_PASSWORD = "cfri bxoq hsub uegt"
    
    # Crear instancia del sender
    email_sender = EmailSender(GMAIL_USER, GMAIL_PASSWORD)
    
    # Enviar email
    email_sender.enviar_email("jr.cosio1@gmail.com", "José Ramón")
