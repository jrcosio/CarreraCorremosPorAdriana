import flet as ft


class InscripcionScreen(ft.Container):
    def __init__(self):
        super().__init__(
            alignment=ft.alignment.center,
            expand=True
        )
        
        self.content = ft.Column([
            ft.Text("Pantalla 2 de prueba", size=30,  color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        self.bgcolor = ft.Colors.GREEN_50
        
        
        
if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")