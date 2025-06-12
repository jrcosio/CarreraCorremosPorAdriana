import flet as ft
import os
from dotenv import load_dotenv
import logging

load_dotenv()
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ...existing code...

class Inscritos(ft.Container):
    def __init__(self):
        super().__init__(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Inscritos",
                        size=40,
                        color=ft.Colors.GREEN_900,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    # Cabecera de la tabla
                    ft.Row(
                        [
                            ft.Container(ft.Text("Dorsal", weight=ft.FontWeight.BOLD,),padding=5,width=80, 
                                        border=ft.border.all(1, ft.Colors.GREY_400)),
                            ft.Container(ft.Text("Nombre", weight=ft.FontWeight.BOLD), padding=5,width=200,
                                        border=ft.border.all(1, ft.Colors.GREY_400)),
                            ft.Container(ft.Text("Apellidos", weight=ft.FontWeight.BOLD), padding=5,width=500,
                                        border=ft.border.all(1, ft.Colors.GREY_400)),
                            ft.Container(ft.Text("Sexo", weight=ft.FontWeight.BOLD), padding=5, 
                                         border=ft.border.all(1, ft.Colors.GREY_400)),
                            ft.Container(ft.Text("CCAA", weight=ft.FontWeight.BOLD), padding=5, width=150,
                                         border=ft.border.all(1, ft.Colors.GREY_400)),
                            ft.Container(ft.Text("Localidad", weight=ft.FontWeight.BOLD), padding=5,width=200,
                                         border=ft.border.all(1, ft.Colors.GREY_400)),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    # Lista de inscritos (ejemplo)
                    *[
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(
                                        ft.Text(str(inscrito["dorsal"])),
                                            padding=5,
                                            width=80,
                                            alignment=ft.alignment.center_left,
                                            ),
                                    ft.Container(
                                        ft.Text(inscrito["nombre"]),
                                            padding=5,
                                            width=200,
                                            alignment=ft.alignment.center_left,
                                            ),
                                    ft.Container(
                                        ft.Text(inscrito["apellidos"]),
                                            padding=5,
                                            width=500,
                                            alignment=ft.alignment.center_left,
                                            ),
                                    ft.Container(
                                        ft.Text(inscrito["sexo"]),
                                            padding=5,
                                            width=80,
                                            alignment=ft.alignment.center_left,
                                            ),
                                    ft.Container(
                                        ft.Text(inscrito["ccaa"]),
                                            padding=5,
                                            width=150,
                                            alignment=ft.alignment.center_left,
                                            ),
                                    ft.Container(
                                        ft.Text(inscrito["localidad"]),
                                            padding=5,
                                            width=200,
                                            alignment=ft.alignment.center_left,
                                            ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            border=ft.border.all(1, ft.Colors.GREY_400),
                            border_radius=8,
                            padding=0,
                            margin=5,
                        )
                        for inscrito in [
                            {
                                "dorsal": 101,
                                "nombre": "Juan",
                                "apellidos": "Pérez García",
                                "sexo": "M",
                                "ccaa": "Cantabria",
                                "localidad": "Santander"
                            },
                            {
                                "dorsal": 102,
                                "nombre": "Ana",
                                "apellidos": "López Ruiz",
                                "sexo": "F",
                                "ccaa": "Asturias",
                                "localidad": "Oviedo"
                            },
                        ]
                    ]
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
        )

def main(page: ft.Page):
    page.title = "Listado de Inscritos"
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.add(Inscritos())

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)