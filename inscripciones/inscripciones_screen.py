import flet as ft
from .cont_campos import Campos
from barra_navegacion import NavBar

class InscripcionScreen(ft.Container):
    def __init__(self):
        super().__init__(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                controls=[
                    NavBar(),
                    Campos()
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
        )
            
if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")