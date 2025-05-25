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
                    WikilocMapContainer(
                        trail_id=recorrido_data["wikilog"],
                        width=1000,
                        height=600,  
                    )
                ]
            )             
        )