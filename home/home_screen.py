import flet as ft


class HomeScreen(ft.Container):
    def __init__(self):
        super().__init__(
            alignment=ft.alignment.center,
            expand=True
        )
        
        self.content = ft.Column([
            ft.Text("Pantalla 1", color=ft.Colors.BLACK, size=30, weight=ft.FontWeight.BOLD),
            ft.Image(
                src="images/foto2.jpg",
                width=300,
                height=200,
                fit=ft.ImageFit.CONTAIN,
                border_radius=ft.border_radius.all(10),
            ),
            ft.Image(
                src="images/foto1.jpg",
                width=300,
                height=200,
                fit=ft.ImageFit.CONTAIN,
                border_radius=ft.border_radius.all(10),
            ),
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        self.bgcolor = ft.Colors.BLUE_50
        
        
if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")