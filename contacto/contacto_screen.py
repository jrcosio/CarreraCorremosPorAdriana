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

        enviar= ft.ElevatedButton("Enviar", icon=ft.Icons.SEND)
        super().__init__(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Contacto",
                        size=40,
                        color=ft.Colors.BLACK,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    txtnombre,
                    txtemail,
                    txtasunto,
                    txtcomentario,
                    enviar
 
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),  
        )
        
        
        # Contenido de la pantalla de contacto
       




# def main(page: ft.Page):
#     page.bgcolor = ft.Colors.WHITE,
#     page.title = "Contacto"
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER

#     datos = ft.Column(
#         [
#             txtnombre,
#             txtemail,
#             txtasunto,
#             txtcomentario,
#             enviar,
#         ],
#         # expand=True,
#         scroll=True,
#         alignment=ft.MainAxisAlignment.CENTER,
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        
#     )

   
    
    
   