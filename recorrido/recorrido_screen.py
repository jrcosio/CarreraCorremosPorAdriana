import flet as ft
from recorrido.WikilocMapContainer import WikilocMapContainer



class RecorridoScreen(ft.Container):
    def __init__(self, recorrido_data):
        super().__init__(
            content = ft.Column(
                controls = [
                    ft.Text(
                        recorrido_data["titulo"],
                        weight=ft.FontWeight.BOLD,
                        size=24,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        recorrido_data["descripcion"],
                        size=16,
                        color=ft.Colors.WHITE70
                    ),
                    ft.Row(
                        controls = [
                            WikilocMapContainer(
                                trail_id=recorrido_data["wikilog"],
                                width=1000,
                                height=600,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Text(
                                            f"Distancia: {recorrido_data['distancia']} km",
                                            size=25,
                                            color=ft.Colors.RED
                                        ),
                                        bgcolor=ft.Colors.BLUE_GREY_400,
                                        border_radius=ft.border_radius.all(20)
                                        
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            f"Desnivel: {recorrido_data['desnivel']} m",
                                            size=25,
                                            color=ft.Colors.RED
                                        ),
                                        bgcolor=ft.Colors.BLUE_GREY_400,
                                        border_radius=ft.border_radius.all(20)
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )             
        )