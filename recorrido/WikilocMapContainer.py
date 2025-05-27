import flet as ft
from flet_webview import WebView

class WikilocMapContainer(ft.Container):
    def __init__(
        self, 
        trail_id: str, 
        width: int = None,  
        height: int = None,  
        padding: int = 10, 
        border_color: str = ft.Colors.GREY_400,
        border_width: int = 1, 
        border_radius: int = 10,
        show_measures: bool = True,     # Mostrar medidas de la ruta
        show_title: bool = False,       # Mostrar título de la ruta
        show_near: bool = False,        # Mostrar rutas cercanas
        show_images: bool = False,      # Mostrar imágenes de la ruta
        map_type: str = "H",  # H, M, S (Híbrido, Mapa, Satélite)
        expand: bool = False,  # Añadido para permitir expandir al padre
        **kwargs
    ):
        # Construir la URL de Wikiloc
        wikiloc_url = f"https://es.wikiloc.com/wikiloc/spatialArtifacts.do?event=view&id={trail_id}"
        wikiloc_url += f"&measures={'on' if show_measures else 'off'}"
        wikiloc_url += f"&title={'on' if show_title else 'off'}"
        wikiloc_url += f"&near={'on' if show_near else 'off'}"
        wikiloc_url += f"&images={'on' if show_images else 'off'}"
        wikiloc_url += f"&maptype={map_type}"
        
        # Crear el WebView para el mapa con dimensiones que se adaptarán
        wikiloc_map = WebView(
            url=wikiloc_url,
            width=width,
            height=height,
            expand=expand,  # El WebView también se expandirá si es necesario
        )
        
        # Inicializar el Container con el WebView
        super().__init__(
            content=wikiloc_map,
            width=width,
            height=height,
            padding=padding,
            border=ft.border.all(border_width, border_color),
            border_radius=border_radius,
            expand=expand,  # Permite que el contenedor se expanda
            **kwargs  # Permite pasar otras propiedades del Container
        )



# def main(page: ft.Page):
#     page.title = "Mapa de Wikiloc en Flet"

    
#     wikiloc_container = WikilocMapContainer(
#         trail_id="176672547", # ID de la ruta de Wikiloc
#         # expand=True,  # Permitir que el contenedor se expanda
#         width=1000,
#         height=600
#     )
    
#     page.add(wikiloc_container)