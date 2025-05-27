import flet as ft
from .cont_campos import Campos
from barra_navegacion import NavBar

class InscripcionScreen(ft.Container):
    def __init__(self):
        super().__init__(
            content=Campos()
        )

if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")