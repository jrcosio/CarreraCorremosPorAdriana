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
        
        self.enviar= ft.ElevatedButton("Enviar", icon=ft.Icons.SEND,
                                  color=ft.Colors.BLACK,
                                  icon_color=ft.Colors.BLACK, 
                                  bgcolor=ft.Colors.GREEN_300)

        self.btn_enviar= ft.ElevatedButton("Enviar", 
                                  icon=ft.Icons.SEND,
                                  width=200,
                                  height=50,
                                  bgcolor=ft.Colors.GREEN_300,
                                  color=ft.Colors.WHITE,
                                  #on_click=self.on_click_enviar,
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
                    self.enviar
 
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
        
