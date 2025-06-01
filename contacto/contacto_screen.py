import flet as ft

class ContactoScreen(ft.Container):
    def __init__(self):
        txtnombre = ft.TextField(
            label="Nombre y Apellidos",
            value="",
            color=ft.Colors.BLACK,
            width=400,
        )

        txtemail = ft.TextField(
            label="Email",  
            value="",
            color=ft.Colors.BLACK,
            width=400,
        )

        txtasunto = ft.TextField(
            label="Asunto",
            value="",
            color=ft.Colors.BLACK,
            width=400,
        )

        txtcomentario = ft.TextField(
            label="Comentario",
            value="",
            color=ft.Colors.BLACK,
            width=400,
            min_lines=5,
            max_length=500,
            multiline=True,
            text_align=ft.TextAlign.LEFT,
        )

        txtnemail = ft.Text("email: asociacionpeñasagra@gmail.com", 
                            size=20,
                            font_family="Britanic Bold",
                            color=ft.Colors.BLACK,)
        
        enviar= ft.ElevatedButton("Enviar", icon=ft.Icons.SEND,
                                  color=ft.Colors.BLACK,
                                  icon_color=ft.Colors.BLACK, 
                                  bgcolor=ft.Colors.GREEN_300
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
                    txtnombre,
                    txtemail,
                    txtasunto,
                    txtcomentario,
                    txtnemail,
                    enviar
 
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),  
        )
        
