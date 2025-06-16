import flet as ft
from utils.gmail import Gmail
import os
from dotenv import load_dotenv
import logging

log = logging.getLogger(__name__)
# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ContactoScreen(ft.Container):
    def __init__(self):
        
        estilo = {
            "color" : "#ffcb2e",
            "border_color" : "#ffcb2e",
            "bgcolor" : "#3c90be",
            "label_style" : ft.TextStyle(color="#ffcb2e"),
            "error_style" : ft.TextStyle(color=ft.Colors.RED_300),
        }
        
        self.txtnombre = ft.TextField(
            label="Nombre y Apellidos",
            value="",
            **estilo,
            width=500,
        )

        self.txtemail = ft.TextField(
            label="Email",  
            value="",
            **estilo,
            width=500,
        )

        self.txtasunto = ft.TextField(
            label="Asunto",
            value="",
            **estilo,
            width=500,
        )

        self.txtcomentario = ft.TextField(
            label="Comentario",
            value="",
            **estilo,
            width=500,
            min_lines=10,
            max_length=500,
            multiline=True,
            text_align=ft.TextAlign.LEFT,
        )

        self.txtnemail = ft.Container(
            content= ft.Column(
                [
                    ft.Text("Estas enviando un correo a la Asociación Peñasagra", 
                                size=20,
                                font_family="Britanic Bold",
                                color=ft.Colors.BLUE_ACCENT,),
                    ft.Text("asociacionpenasagra@gmail.com",
                                size=20,
                                font_family="Britanic Bold",
                                color=ft.Colors.BLUE_ACCENT)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.Alignment(0,0),
        )
        

        self.btn_enviar= ft.ElevatedButton("Enviar", 
                                  icon=ft.Icons.SEND,
                                  width=200,
                                  height=50,
                                  bgcolor=ft.Colors.GREEN_300,
                                  color=ft.Colors.WHITE,
                                  on_click=self.on_click_enviar,
                                  )
        
        super().__init__(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Contacto",
                        size=40,
                        color="#ffcb2e",
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    self.txtnombre,
                    self.txtemail,
                    self.txtasunto,
                    self.txtcomentario,
                    self.txtnemail,
                    self.btn_enviar,
                    ft.Container(height=200),  # Espacio flexible para centrar el contenido
 
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),  
        )
    
    def validar_campos(self):
        # Aquí puedes implementar la lógica para validar los campos del formulario
        if not self.txtnombre.value or self.txtnombre.value.strip() == "":
            self.txtnombre.error_text = "El nombre es obligatorio"
            self.txtnombre.update()
            return False
        else:
            self.txtnombre.error_text = None
            self.txtnombre.update()
            
        if not self.txtemail.value or self.txtemail.value.strip() == "":
            self.txtemail.error_text = "El email es obligatorio"
            self.txtemail.update()
            return False
        else:
            self.txtemail.error_text = None
            self.txtemail.update()
        
        if not self.txtasunto.value or self.txtasunto.value.strip() == "":
            self.txtasunto.error_text = "El asunto es obligatorio"
            self.txtasunto.update() 
            return False
        else:
            self.txtasunto.error_text = None
            self.txtasunto.update()
        
        if not self.txtcomentario.value or self.txtcomentario.value.strip() == "":
            self.txtcomentario.error_text = "El comentario es obligatorio"
            self.txtcomentario.update()
            return False
        else:
            self.txtcomentario.error_text = None
            self.txtcomentario.update()
        
        # Si todos los campos son válidos, limpiar los errores
        
        return True
    
    def limpiar_campos(self):
        # Aquí puedes implementar la lógica para limpiar los campos del formulario
        self.txtnombre.value = ""
        self.txtemail.value = ""
        self.txtasunto.value = ""
        self.txtcomentario.value = ""
        
        # Limpiar los mensajes de error
        self.txtnombre.error_text = None
        self.txtemail.error_text = None
        self.txtasunto.error_text = None
        self.txtcomentario.error_text = None
        
        self.update()
    
    def on_click_enviar(self, e):
        # Aquí puedes manejar el evento de clic en el botón de enviar
        if self.validar_campos():
            # Cargar variables de entorno
            load_dotenv()

            # Obtener credenciales de Gmail desde .env
            gmail_user = os.getenv('GMAIL_USER')
            gmail_pass = os.getenv('GMAIL_PASSWORD')

            # Crear instancia de Gmail y enviar contacto
            gmail = Gmail(gmail_user, gmail_pass)
            
            gmail.enviar_contacto(
                nombre_usuario=self.txtnombre.value,
                email_usuario=self.txtemail.value,
                asunto_usuario=self.txtasunto.value,
                comentario=self.txtcomentario.value
            )
                   
            
            log.info(f"Comentario enviado correctamente de {self.txtnombre.value}")
            self.page.open(
                ft.SnackBar(
                    content=ft.Text(f"{self.txtnombre.value} has enviado el comentario correctamente.",
                                    size=20,
                                    font_family="Britanic Bold",
                                    color=ft.Colors.WHITE),
                    open=True,
                    bgcolor=ft.Colors.GREEN_300,
                    duration=ft.Duration(seconds=5),
                )
            )
            self.limpiar_campos() 
