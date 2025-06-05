import flet as ft

class NavButton(ft.TextButton):
    def __init__(self, text, data, on_click, color=ft.Colors.BLACK, negrita=ft.FontWeight.NORMAL):
        super().__init__(
            text=text,
            style=ft.ButtonStyle(
                color=color,
                padding=10,
                text_style=ft.TextStyle(
                    size=16,
                    weight=negrita,
                ),
            ),
            data=data,
            on_hover=lambda e: self._on_hover_change(e, color),
            on_click=on_click
        )
    
    def _on_hover_change(self, e, color):
        if e.data == "true":
            e.control.style.color = ft.Colors.BLUE
        else:
            e.control.style.color = color
        e.control.update()

# Clase para la barra de navegación
class NavBar(ft.Container):
    def __init__(self, on_button_clicked):
        self.logo = ft.Image(
            src="images/logomenu.png",
            fit=ft.ImageFit.CONTAIN,
        )
        
        # Botones de navegación
        self.buttons = [
            NavButton("PRINCIPAL", "btn_home", on_button_clicked),
            NavButton("INSCRIPCIÓN", "btn_inscripcion", on_button_clicked, color=ft.Colors.RED_300, negrita=ft.FontWeight.BOLD),
            # NavButton("INSCRITOS", "btn_inscritos", on_button_clicked),
            NavButton("TRAIL", "btn_trail", on_button_clicked),
            NavButton("ANDARINES", "btn_andarines", on_button_clicked),
            # NavButton("CLASIFICACIÓN", "btn_clasificacion", on_button_clicked),
            NavButton("GALERÍA", "btn_galeria", on_button_clicked),
            NavButton("CONTACTO", "btn_contacto", on_button_clicked),
        ]
        
        # Fila con logo y botones
        super().__init__(
            content=ft.Row(
                [self.logo, ft.Container(expand=True),*self.buttons],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            padding=10,
            bgcolor=ft.Colors.WHITE,
        )
        
        
if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")