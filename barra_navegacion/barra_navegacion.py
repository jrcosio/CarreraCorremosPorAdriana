# barra_navegacion/barra_navegacion.py

import flet as ft

# La clase NavButton no necesita cambios.
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


class NavBar(ft.Container):
    def __init__(self, on_button_clicked):
        super().__init__()
        self.bgcolor = ft.Colors.WHITE
        self.padding = ft.padding.symmetric(horizontal=60, vertical=10)
        self.on_button_clicked = on_button_clicked

        # --- CONSTRUIMOS AMBAS VISTAS ---
        # Guardamos las vistas como atributos para poder acceder a ellas después
        self.desktop_view = self._build_desktop_view()
        self.mobile_view = self._build_mobile_view()
        
        # Ocultamos la vista móvil inicialmente
        self.mobile_view.visible = False

        # --- EL CONTENIDO ES UN STACK CON AMBAS VISTAS ---
        # Stack permite superponer controles. Solo uno será visible a la vez.
        self.content = ft.Stack(
            [
                self.desktop_view,
                self.mobile_view,
            ]
        )

    def _build_desktop_view(self):
        """Construye y devuelve la Row para la vista de escritorio."""
        return ft.Row(
            [
                ft.Image(src="images/logomenu.png", fit=ft.ImageFit.CONTAIN, height=35),
                ft.Container(expand=True),
                NavButton("PRINCIPAL", "btn_home", self.on_button_clicked),
                NavButton("INSCRIPCIÓN", "btn_inscripcion", self.on_button_clicked, color=ft.Colors.RED_300, negrita=ft.FontWeight.BOLD),
                NavButton("TRAIL", "btn_trail", self.on_button_clicked),
                NavButton("ANDARINES", "btn_andarines", self.on_button_clicked),
                NavButton("GALERÍA", "btn_galeria", self.on_button_clicked),
                NavButton("CONTACTO", "btn_contacto", self.on_button_clicked),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

    def _build_mobile_view(self):
        """Construye y devuelve la Row para la vista móvil."""
        menu_items_map = {
            "PRINCIPAL": "btn_home", "INSCRIPCIÓN": "btn_inscripcion", "TRAIL": "btn_trail",
            "ANDARINES": "btn_andarines", "GALERÍA": "btn_galeria", "CONTACTO": "btn_contacto"
        }
        return ft.Row(
            [
                ft.Image(src="images/logomenu.png", fit=ft.ImageFit.CONTAIN, height=35),
                ft.Container(expand=True),
                ft.PopupMenuButton(
                    icon=ft.Icons.MENU,
                    items=[
                        ft.PopupMenuItem(text=item, on_click=self.on_button_clicked, data=data)
                        for item, data in menu_items_map.items()
                    ],
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

    def update_visibility(self, is_mobile: bool):
        """
        Método clave: Cambia la visibilidad de las vistas.
        """
        self.desktop_view.visible = not is_mobile
        self.mobile_view.visible = is_mobile
        self.update()