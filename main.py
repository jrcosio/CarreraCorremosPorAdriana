import flet as ft
from home.home_screen import HomeScreen
from inscripciones.inscripciones_screen import InscripcionScreen
from galeria.galeria_screen import GaleriaScreen
from barra_navegacion import NavBar


class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.LIGHT
        page.title = "Trail Peñasagra - Corremos por Adriana"
        page.scroll = None
        page.auto_scroll = False
        page.spacing = 0
        page.padding = 0
        
       # Crear instancias de cada pantalla
        self.home_screen = HomeScreen()
        self.inscripcion_screen = InscripcionScreen()
        self.galeria_screen = GaleriaScreen()
        
        
        
        # Mapeo de botones a pantallas
        # Si hubiera mas pantallas se añaden aquí para que los botones la encuentren
        self.screens = {
            "btn1": self.home_screen,
            "btn2": self.inscripcion_screen,
            "btn3": self.galeria_screen
        }
        
        # Contenedor para mostrar la pantalla activa
        self.body_container = ft.Container(
            content=ft.Column(
                [self.screens["btn1"]],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            expand=True,
        )
        
        # Barra de navegación, acordaros de que es unafuncion Callback
        # que se ejecuta cuando se hace click en un botón
        self.nav_bar = NavBar(self.on_button_clicked)
        
        # Añadir todo a la página
        self.page.add(
            ft.Column([
                self.nav_bar,
                self.body_container,
            ], spacing=0, expand=True)
        )
    
    def on_button_clicked(self, e):
        button_id = e.control.data
        if button_id in self.screens:
            self.body_container.content = ft.Column(
                [self.screens[button_id]],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
            self.page.update()

def main(page: ft.Page):
    app = MainApp(page)

if __name__ == "__main__":
    ft.app(target=main, port=80, view=ft.WEB_BROWSER)#, host="0.0.0.0")