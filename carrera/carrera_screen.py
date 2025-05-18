import flet as ft
from flet_webview import WebView  # Importar desde el nuevo paquete

def main(page: ft.Page):
    page.title = "Mapa de Wikiloc en Flet"
    
    # ID de la ruta de Wikiloc que quieres mostrar
    wikiloc_trail_id = "176672547"  
    
    # URL del iframe de Wikiloc
    wikiloc_url = f"https://es.wikiloc.com/wikiloc/spatialArtifacts.do?event=view&id={wikiloc_trail_id}&measures=on&title=off&near=off&images=off&maptype=H"
                   
    
    # Crear un WebView para mostrar el mapa
    wikiloc_map = WebView(
        url=wikiloc_url,
        width=1000,
        height=600,
    )
    titulo = ft.Text(
        "Mapa de la ruta de Wikiloc Corremos por Adriana",
        size=20,
        color=ft.Colors.RED,
        font_family="Arial",
        weight=ft.FontWeight.BOLD,
    )
    # Añadir el WebView a un contenedor
    container = ft.Container(
        content=wikiloc_map,
        padding=10,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10,
    )
    
    page.add(titulo, container)

ft.app(target=main, view=ft.WEB_BROWSER, port=80)