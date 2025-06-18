import flet as ft
import os
from dotenv import load_dotenv
import logging


load_dotenv()
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ...existing code...

inscritos = [
  
  {"dorsal":"001", "nombre":"Jose", "apellidos":"Gomez Perez", "sexo":"H", "ccaa":"Cantabria", "localidad":"Santander","Año":"2005", "categoria":"SENIOR"},
  {"dorsal":"002", "nombre":"Lucia", "apellidos":"Martinez Ruiz", "sexo":"M", "ccaa":"Andalucía", "localidad":"Sevilla","Año":"2000", "categoria":"SENIOR"},
  {"dorsal":"003", "nombre":"Carlos", "apellidos":"Lopez Garcia", "sexo":"H", "ccaa":"Madrid", "localidad":"Madrid","Año":"1972", "categoria":"VET A"},
  {"dorsal":"004", "nombre":"Ana", "apellidos":"Sanchez Torres", "sexo":"M", "ccaa":"Catalunya", "localidad":"Barcelona","Año":"1985", "categoria":"VET B"},
  {"dorsal":"005", "nombre":"Miguel", "apellidos":"Fernandez Cano", "sexo":"H", "ccaa":"Comunidad Valenciana", "localidad":"Valencia","Año":"2010", "categoria":"JUNIOR"},
  {"dorsal":"006", "nombre":"Elena", "apellidos":"Moreno Diaz", "sexo":"M", "ccaa":"Galicia", "localidad":"A Coruña","Año":"2001", "categoria":"SENIOR"},
  {"dorsal":"007", "nombre":"Pablo", "apellidos":"Ramirez Ortega", "sexo":"H", "ccaa":"Castilla_y_León", "localidad":"Valladolid","Año":"1996", "categoria":"VET C"},
  {"dorsal":"008", "nombre":"Sara", "apellidos":"Hernandez Vega", "sexo":"M", "ccaa":"País Vasco", "localidad":"Bilbao","Año":"1987", "categoria":"VET B"},
  {"dorsal":"009", "nombre":"David", "apellidos":"Iglesias Martin", "sexo":"H", "ccaa":"Aragón", "localidad":"Zaragoza","Año":"2012", "categoria":"JUNIOR"},
  {"dorsal":"010", "nombre":"Laura", "apellidos":"Navarro Blanco", "sexo":"M", "ccaa":"Castilla_La_Mancha", "localidad":"Toledo","Año":"1974", "categoria":"VET A"},
  {"dorsal":"011", "nombre":"Javier", "apellidos":"Ortega Perez", "sexo":"H", "ccaa":"Extremadura", "localidad":"Cáceres","Año":"1991", "categoria":"VET C"},
  {"dorsal":"012", "nombre":"Claudia", "apellidos":"Ruiz Molina", "sexo":"M", "ccaa":"Asturias", "localidad":"Oviedo","Año":"2000", "categoria":"SENIOR"},
  {"dorsal":"013", "nombre":"Alvaro", "apellidos":"Gonzalez Suarez", "sexo":"H", "ccaa":"Navarra", "localidad":"Pamplona","Año":"1970", "categoria":"VET C"},
  {"dorsal":"014", "nombre":"Natalia", "apellidos":"Cruz Delgado", "sexo":"M", "ccaa":"La Rioja", "localidad":"Logroño","Año":"1986", "categoria":"VET B"},
  {"dorsal":"015", "nombre":"Diego", "apellidos":"Vega Romero", "sexo":"H", "ccaa":"Canarias", "localidad":"Las Palmas","Año":"2001", "categoria":"SENIOR"},
  {"dorsal":"016", "nombre":"Irene", "apellidos":"Campos Pardo", "sexo":"M", "ccaa":"Murcia", "localidad":"Murcia","Año":"2007", "categoria":"JUNIOR"},
  {"dorsal":"017", "nombre":"Sergio", "apellidos":"Rey Morales", "sexo":"H", "ccaa":"Baleares", "localidad":"Palma","Año":"1973", "categoria":"VET A"},
  {"dorsal":"018", "nombre":"Marta", "apellidos":"Dominguez Leon", "sexo":"M", "ccaa":"Cantabria", "localidad":"Torrelavega","Año":"1986", "categoria":"VET B"},
  {"dorsal":"019", "nombre":"Adrian", "apellidos":"Castro Herrera", "sexo":"H", "ccaa":"Madrid", "localidad":"Alcalá de Henares","Año":"2005", "categoria":"SENIOR"},
  {"dorsal":"020", "nombre":"Patricia", "apellidos":"Nieto Bravo", "sexo":"M", "ccaa":"Comunidad Valenciana", "localidad":"Alicante","Año":"2011", "categoria":"JUNIOR"},
  {"dorsal":"021", "nombre":"Fernando", "apellidos":"Soto Jimenez", "sexo":"H", "ccaa":"Galicia", "localidad":"Santiago de Compostela","Año":"1994", "categoria":"VET C"},
]


banderas_ccaa = {
    "Andalucía": "banderas/Andalucía.png",
    "Aragón": "banderas/Aragón.png",
    "Asturias": "banderas/Asturias.png",
    "Baleares": "banderas/Baleares.png",
    "Canarias": "banderas/Canarias.png",
    "Cantabria": "banderas/Cantabria.png",
    "Castilla_y_León": "banderas/Castilla_y_León.png",
    "Castilla_La_Mancha": "banderas/Castilla_La_Mancha.png",
    "Catalunya": "banderas/Catalunya.png",
    "Comunidad Valenciana": "banderas/Comunidad Valenciana.png",
    "Extremadura": "banderas/Extremadura.png",
    "Galicia": "banderas/Galicia.png",
    "La Rioja": "banderas/La Rioja.png",
    "Madrid": "banderas/Madrid.png",
    "Murcia": "banderas/Murcia.png",
    "Navarra": "banderas/Navarra.png",
    "País Vasco": "banderas/País Vasco.png",
}



class Inscritos(ft.Container):
    def __init__(self):
        super().__init__(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Inscritos Trail Peñasagra 2025",
                        size=40,
                        color=ft.Colors.GREEN_900,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),   
                    ft.Row(
                        [
                            ft.Container(width=100, height=50, alignment=ft.alignment.center_left,),
                            ft.Container(ft.ElevatedButton(text="Todos", on_click=lambda e: log.info("Mostrar todos los inscritos")), padding=5, alignment=ft.alignment.center_left,
                                         ),
                            ft.Container(ft.ElevatedButton(text="Trail", on_click=lambda e: log.info("Mostrar inscritos trail")), padding=5, alignment=ft.alignment.center_left,
                                         ),
                            ft.Container(ft.ElevatedButton(text="Andarines", on_click=lambda e: log.info("Mostrar inscritos femeninos")), padding=5, alignment=ft.alignment.center_left,
                                        ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                        
                    ),
                    ft.Row(
                        [
                            ft.Container(ft.Text("Dorsal", weight=ft.FontWeight.BOLD), padding=5, width=80, border=ft.border.all(1, ft.Colors.GREY_400), alignment=ft.alignment.center),
                            ft.Container(ft.Text("Nombre", weight=ft.FontWeight.BOLD), padding=5, width=200, border=ft.border.all(1, ft.Colors.GREY_400), alignment=ft.alignment.center_left),
                            ft.Container(ft.Text("Apellidos", weight=ft.FontWeight.BOLD), padding=5, width=350, border=ft.border.all(1, ft.Colors.GREY_400), alignment=ft.alignment.center_left),
                            ft.Container(ft.Text("Sexo", weight=ft.FontWeight.BOLD), padding=5, width=80, border=ft.border.all(1, ft.Colors.GREY_400), alignment=ft.alignment.center),
                            ft.Container(ft.Text("CCAA", weight=ft.FontWeight.BOLD), padding=5, width=200, border=ft.border.all(1, ft.Colors.GREY_400), alignment=ft.alignment.center_left),
                            ft.Container(ft.Text("Localidad", weight=ft.FontWeight.BOLD), padding=5, width=200, border=ft.border.all(1, ft.Colors.GREY_400), alignment=ft.alignment.center_left),
                            ft.Container(ft.Text("Categoria", weight=ft.FontWeight.BOLD), padding=5, width=100, border=ft.border.all(1, ft.Colors.GREY_400), alignment=ft.alignment.center),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    *[
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(ft.Text(str(inscrito["dorsal"])), padding=2, width=80, alignment=ft.alignment.center),
                                    ft.Container(ft.Text(inscrito["nombre"]), padding=2, width=200, alignment=ft.alignment.center_left),
                                    ft.Container(ft.Text(inscrito["apellidos"].upper()), padding=2, width=350, alignment=ft.alignment.center_left),
                                    ft.Container(ft.Text(inscrito["sexo"]), padding=2, width=80, alignment=ft.alignment.center),
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.Image(
                                                    src=banderas_ccaa.get(inscrito["ccaa"], None),
                                                    fit=ft.ImageFit.CONTAIN,
                                                    width=30,
                                                    height=20,
                                                ),
                                                ft.Text(inscrito["ccaa"], size=12),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        width=200,
                                        alignment=ft.alignment.center_left,
                                    ),
                                    ft.Container(ft.Text(inscrito["localidad"]), padding=2, width=200, alignment=ft.alignment.center_left),
                                    ft.Container(ft.Text(inscrito["categoria"]), padding=2, width=100, alignment=ft.alignment.center),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            border_radius=4,
                            padding=0,
                            margin=1,
                        )
                        for inscrito in inscritos
                    ]
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll="auto",
            )
        )

def main(page: ft.Page):
    page.title = "Listado de Inscritos"
    
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.add(Inscritos())

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)