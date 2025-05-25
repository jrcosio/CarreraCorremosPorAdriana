import flet as ft

class NavButton(ft.TextButton):
    def __init__(self, text, data, on_click):
        super().__init__(
            text=text,
            style=ft.ButtonStyle(
                color=ft.Colors.BLACK,
                padding=10,
            ),
            data=data,
            on_hover=self._on_hover_change,
            on_click=on_click
        )
    
    def _on_hover_change(self, e):
        if e.data == "true":
            e.control.style.color = ft.Colors.BLUE
        else:
            e.control.style.color = ft.Colors.BLACK
        e.control.update()

# Clase para la barra de navegación
class NavBar(ft.Container):
    def __init__(self, on_button_clicked):
        self.logo = ft.Image(
            src="images/logo.png",
            width=50,
            height=50,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(10),
        )
        
        # Botones de navegación
        self.buttons = [
            NavButton("HOME", "btn1", on_button_clicked),
            NavButton("INSCRIPCIÓN", "btn2", on_button_clicked),
            NavButton("GALERÍA", "btn3", on_button_clicked),
            NavButton("RECORRIDOS", "btn4", on_button_clicked)
        ]
        
        # Fila con logo y botones
        super().__init__(
            content=ft.Row(
                [self.logo, *self.buttons],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=15,
            bgcolor=ft.Colors.BLUE_GREY_100,
        )
        
        
if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")