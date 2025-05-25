import flet as ft
from recorrido.WikilocMapContainer import WikilocMapContainer

class RecorridoScreen(ft.Container):
    def __init__(self, recorrido_data):
        super().__init__(
            content = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls = [
                    ft.Text(
                        recorrido_data["titulo"],
                        weight=ft.FontWeight.BOLD,
                        size=24,
                        color=ft.Colors.BLACK,
                        font_family = "Roboto",
                    ),
                    ft.Text(
                        recorrido_data["descripcion"],
                        size=16,
                        color=ft.Colors.BLACK,
                        font_family= "Roboto",
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls = [
                            WikilocMapContainer(
                                trail_id=recorrido_data["wikilog"],
                                width=1000,
                                height=600,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Column(
                                            spacing=0,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[  # Cambiado para usar "controls" con una lista
                                                ft.Image(src="imagenes_recorrido/run.png", width=55, height=55),
                                                ft.Text(
                                                    f"{recorrido_data['distancia']} km",
                                                    size=20,
                                                    color=ft.Colors.BLACK
                                                ),
                                                ft.Text(
                                                    "DESNIVEL",
                                                    size=10,
                                                    color=ft.Colors.BLACK
                                                )
                                            ]
                                        ),
                                        bgcolor=ft.Colors.BLUE_GREY_400,
                                        border = ft.border.all(2, ft.Colors.BLACK),
                                        border_radius=ft.border_radius.all(100),
                                        width=120,
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            spacing=0,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[  # Cambiado para usar "controls" con una lista
                                                ft.Image(src="imagenes_recorrido/mont.png", width=64),
                                                ft.Text(
                                                    f"{recorrido_data['desnivel']} m",
                                                    size=20,
                                                    color=ft.Colors.BLACK
                                                ),
                                                ft.Text(
                                                    "DESNIVEL",
                                                    size=10,
                                                    color=ft.Colors.BLACK
                                                )
                                            ]
                                        ),
                                        bgcolor=ft.Colors.BLUE_GREY_400,
                                        border = ft.border.all(2, ft.Colors.BLACK),
                                        border_radius=ft.border_radius.all(100),
                                        width=120,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ]
                    ),
                ]
            )             
        )