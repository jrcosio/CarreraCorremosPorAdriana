import flet as ft

txtnombre = ft.TextField(
    label="Nombre y Apellidos",
    value="",
    color=ft.Colors.WHITE,
    width=400,
)

txtemail = ft.TextField(
    label="Email",  
    value="",
    color=ft.Colors.WHITE,
    width=400,
)

txtasunto = ft.TextField(
    label="Asunto",
    value="",
    color=ft.Colors.WHITE,
    width=400,
)

txtcomentario = ft.TextField(
    label="Comentario",
    value="",
    color=ft.Colors.WHITE,
    width=400,
    height=400,
    max_length=500,
    multiline=True,
    text_align=ft.TextAlign.LEFT,
)

enviar= ft.ElevatedButton("Enviar", icon=ft.Icons.SEND)

def main(page: ft.Page):
    page.bgcolor = ft.Colors.WHITE,
    page.title = "Contacto"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    datos = ft.Column(
        [
            txtnombre,
            txtemail,
            txtasunto,
            txtcomentario,
            enviar,
        ],
        # expand=True,
        scroll=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        
    )

    container_vacio= ft.Container(
        bgcolor=ft.Colors.WHITE,    
        width=400,
        height=400,     
        alignment=ft.alignment.top_left,
    )
    container= ft.Row([container_vacio, datos])
    page.add(container)

ft.app(target=main)
