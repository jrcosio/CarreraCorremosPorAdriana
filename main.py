import flet as ft
from home.home_screen import HomeScreen
from inscripciones.inscripciones_screen import InscripcionScreen
from galeria.galeria_screen import GaleriaScreen
from recorrido.recorrido_screen import RecorridoScreen
from barra_navegacion import NavBar


class MainApp:
    trail ={
        "titulo": "Trail Peñasagra",
        "descripcion": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "wikilog": "214816740",
        "distancia": 20,
        "desnivel": 1029,
        "fecha": "2024-06-15",
        "hora": "09:00",
        "lugar": "Cosío"
    }
    andarines ={
        "titulo": "Andarines",
        "descripcion": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "wikilog": "214817578",
        "distancia": 15,
        "desnivel": 780,
        "fecha": "2024-06-15",
        "hora": "09:00",
        "lugar": "Cosío"
    }
    def __init__(self, page: ft.Page):
        self.page = page
        page.title = "Trail Peñasagra - Corremos por Adriana"
        page.scroll = None
        page.auto_scroll = False
        
       # Crear instancias de cada pantalla
        self.home_screen = HomeScreen()
        self.inscripcion_screen = InscripcionScreen()
        self.galeria_screen = GaleriaScreen()
        self.recorrido_screen = RecorridoScreen(recorrido_data=self.trail)
        
        
        
        # Mapeo de botones a pantallas
        # Si hubiera mas pantallas se añaden aquí para que los botones la encuentren
        self.screens = {
            "btn1": self.home_screen,
            "btn2": self.inscripcion_screen,
            "btn3": self.galeria_screen,
            "btn4": self.recorrido_screen
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