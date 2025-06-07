import flet as ft
from home.home_screen import HomeScreen
from inscripciones.inscripciones_screen import InscripcionScreen
from galeria.galeria_screen import GaleriaScreen
from recorrido.recorrido_screen import RecorridoScreen
from barra_navegacion.barra_navegacion import NavBar
from contacto.contacto_screen import ContactoScreen
from configurar_web import trail, andarines

class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        page.title = "Trail Peñasagra - Corremos por Adriana"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        
        # Mapeo de botones a pantallas
        self.screens = {
            "btn_home": HomeScreen(),
            "btn_inscripcion": InscripcionScreen(),
            "btn_inscritos": HomeScreen(),
            "btn_galeria": GaleriaScreen(),
            "btn_trail": RecorridoScreen(recorrido_data=trail),
            "btn_andarines": RecorridoScreen(recorrido_data=andarines),
            "btn_contacto": ContactoScreen(),
            "btn_clasificacion": HomeScreen(),
        }
        
        # Contenedor para mostrar la pantalla activa
        self.body_container = ft.Container(
            content=self.screens["btn_home"],
            expand=True,
            bgcolor=ft.Colors.WHITE,
        )
        
        # Barra de navegación
        self.nav_bar = NavBar(self.on_button_clicked)
        
        # Estructura principal de la página
        self.page.add(
            ft.Column(
                [
                    self.nav_bar,
                    ft.Column(
                        [self.body_container],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    )
                ],
                spacing=0,
                expand=True
            )
        )

        # Configuración inicial del responsive
        self.page.on_resize = self.on_page_resize
        self.on_page_resize(None)

    def on_button_clicked(self, e):
        """Se ejecuta al hacer clic en una opción de navegación."""
        button_id = e.control.data
        if button_id in self.screens:
            self.body_container.content = self.screens[button_id]
            # Reaplicamos la lógica responsive para mantener la consistencia del UI
            self.on_page_resize(None)

    def on_page_resize(self, e):
        """
        Función central que gestiona la apariencia de la app según el tamaño.
        """
        breakpoint_mobile = 768
        width = self.page.width or 1024 # Usamos un valor por defecto si es None
        is_mobile = width < breakpoint_mobile

        # 1. Ordena a la NavBar que actualice la visibilidad de sus vistas
        self.nav_bar.update_visibility(is_mobile)

        # 2. Ajusta los paddings
        if is_mobile:
            self.nav_bar.padding = ft.padding.symmetric(horizontal=20, vertical=10)
            self.body_container.padding = ft.padding.symmetric(horizontal=20)
        else:
            self.nav_bar.padding = ft.padding.symmetric(horizontal=60, vertical=10)
            self.body_container.padding = ft.padding.symmetric(horizontal=60)
        
        # 3. Actualiza la página para aplicar todos los cambios
        self.page.update()

def main(page: ft.Page):
    # Envolvemos el contenido principal en una columna con scroll
    # para que la NavBar se quede fija arriba y el contenido sea el que se desplace.
    page.scroll = ft.ScrollMode.HIDDEN
    app = MainApp(page)

if __name__ == "__main__":
    ft.app(target=main, port=80, view=ft.WEB_BROWSER, host="0.0.0.0", assets_dir="assets")