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
        page.scroll = None
        page.theme_mode = ft.ThemeMode.LIGHT
        page.auto_scroll = False
        page.padding = 0
                
        
        # Mapeo de botones a pantallas
        # Si hubiera mas pantallas se añaden aquí para que los botones la encuentren
        self.screens = {
            "btn_home": HomeScreen(),
            "btn_inscripcion": InscripcionScreen(),
            "btn_inscritos": HomeScreen(),  # Reutilizando la pantalla de inscripción pero sera otra pantalla
            "btn_galeria": GaleriaScreen(),
            "btn_trail": RecorridoScreen(recorrido_data = trail),
            "btn_andarines": RecorridoScreen(recorrido_data = andarines),
            "btn_contacto": ContactoScreen(),  # Reutilizando la pantalla de inicio para contacto
            "btn_clasificacion": HomeScreen(),  # Reutilizando la pantalla de inicio para contacto
        }
        
        # Contenedor para mostrar la pantalla activa
        self.body_container = ft.Container(
            content=ft.Column(
                [self.screens["btn_home"]],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            expand=True,
            bgcolor= ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal = 60) # Añadido padding horizontal para que no se vea tan pegado a los bordes
        )
        
        # Barra de navegación, acordaros de que es unafuncion Callback
        # que se ejecuta cuando se hace click en un botón
        self.nav_bar = NavBar(self.on_button_clicked)
        
        # Añadir todo a la página
        self.page.add(
            ft.Column([
                self.nav_bar,
                ft.Divider(color=ft.Colors.GREEN_300),
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
    ft.app(target=main, port=80, view=ft.WEB_BROWSER, host="0.0.0.0", assets_dir="assets")