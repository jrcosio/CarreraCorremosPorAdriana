import flet as ft

class ContactoScreen(ft.Container):
    def __init__(self):
        self.txtnombre = ft.TextField(
            label="Nombre y Apellidos",
            value="",
            color=ft.Colors.BLACK,
            width=500,
        )

        self.txtemail = ft.TextField(
            label="Email",  
            value="",
            color=ft.Colors.BLACK,
            width=500,
        )

        self.txtasunto = ft.TextField(
            label="Asunto",
            value="",
            color=ft.Colors.BLACK,
            width=500,
        )

        self.txtcomentario = ft.TextField(
            label="Comentario",
            value="",
            color=ft.Colors.BLACK,
            width=500,
            min_lines=10,
            max_length=500,
            multiline=True,
            text_align=ft.TextAlign.LEFT,
        )

        self.txtnemail = ft.Text("email: asociacionpeñasagra@gmail.com", 
                            size=20,
                            font_family="Britanic Bold",
                            color=ft.Colors.BLACK,)
        

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
                        color=ft.Colors.GREEN_900,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    self.txtnombre,
                    self.txtemail,
                    self.txtasunto,
                    self.txtcomentario,
                    self.txtnemail,
                    self.btn_enviar
 
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
            # Si los campos son válidos, enviar el comentario
           
            self.limpiar_campos()
            print("Enviar comentario")
        
