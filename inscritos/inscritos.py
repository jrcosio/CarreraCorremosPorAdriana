import flet as ft
import os
from dotenv import load_dotenv
import logging

load_dotenv()
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ...existing code...

inscritos = [
  {"dorsal":"001", "nombre":"Jose", "apellidos":"Gomez Perez", "Sexo":"H", "ccaa":"Cantabria", "Localidad":"Santander"},
  {"dorsal":"002", "nombre":"Lucía", "apellidos":"Martínez Ruiz", "Sexo":"M", "ccaa":"Andalucía", "Localidad":"Sevilla"},
  {"dorsal":"003", "nombre":"Carlos", "apellidos":"López Díaz", "Sexo":"H", "ccaa":"Madrid", "Localidad":"Madrid"},
  {"dorsal":"004", "nombre":"Marta", "apellidos":"García López", "Sexo":"M", "ccaa":"Cataluña", "Localidad":"Barcelona"},
  {"dorsal":"005", "nombre":"Álvaro", "apellidos":"Fernández Torres", "Sexo":"H", "ccaa":"Galicia", "Localidad":"A Coruña"},
  {"dorsal":"006", "nombre":"Elena", "apellidos":"Sánchez Vega", "Sexo":"M", "ccaa":"Castilla y León", "Localidad":"Valladolid"},
  {"dorsal":"007", "nombre":"David", "apellidos":"Ramírez Gómez", "Sexo":"H", "ccaa":"Comunidad Valenciana", "Localidad":"Valencia"},
  {"dorsal":"008", "nombre":"Patricia", "apellidos":"Moreno Sáez", "Sexo":"M", "ccaa":"Extremadura", "Localidad":"Badajoz"},
  {"dorsal":"009", "nombre":"Javier", "apellidos":"Hernández Cano", "Sexo":"H", "ccaa":"Aragón", "Localidad":"Zaragoza"},
  {"dorsal":"010", "nombre":"Sara", "apellidos":"Iglesias León", "Sexo":"M", "ccaa":"Asturias", "Localidad":"Oviedo"},
  {"dorsal":"011", "nombre":"Andrés", "apellidos":"Jiménez Molina", "Sexo":"H", "ccaa":"Murcia", "Localidad":"Murcia"},
  {"dorsal":"012", "nombre":"Cristina", "apellidos":"Ortiz Delgado", "Sexo":"M", "ccaa":"Navarra", "Localidad":"Pamplona"},
  {"dorsal":"013", "nombre":"Mario", "apellidos":"Ruiz Martín", "Sexo":"H", "ccaa":"Castilla-La Mancha", "Localidad":"Toledo"},
  {"dorsal":"014", "nombre":"Laura", "apellidos":"Núñez Herrera", "Sexo":"M", "ccaa":"La Rioja", "Localidad":"Logroño"},
  {"dorsal":"015", "nombre":"Sergio", "apellidos":"Vargas Jimeno", "Sexo":"H", "ccaa":"País Vasco", "Localidad":"Bilbao"},
  {"dorsal":"016", "nombre":"Carmen", "apellidos":"Domínguez Rivas", "Sexo":"M", "ccaa":"Baleares", "Localidad":"Palma"},
  {"dorsal":"017", "nombre":"Hugo", "apellidos":"Cortés Blanco", "Sexo":"H", "ccaa":"Canarias", "Localidad":"Las Palmas"},
  {"dorsal":"018", "nombre":"Beatriz", "apellidos":"Gutiérrez Lara", "Sexo":"M", "ccaa":"Aragón", "Localidad":"Huesca"},
  {"dorsal":"019", "nombre":"Pablo", "apellidos":"Rey Moreno", "Sexo":"H", "ccaa":"Madrid", "Localidad":"Alcalá de Henares"},
  {"dorsal":"020", "nombre":"Natalia", "apellidos":"Cano Paredes", "Sexo":"M", "ccaa":"Galicia", "Localidad":"Lugo"}
]


class Inscritos(ft.Container):
    def __init__(self):
        super().__init__(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Inscritos",
                        size=40,
                        color=ft.Colors.GREEN_900,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    # Cabecera de la tabla
                    ft.Row(
                        [
                            ft.Container(ft.Text("Dorsal", weight=ft.FontWeight.BOLD,),padding=5,width=80, 
                                        border=ft.border.all(1, ft.Colors.GREY_400)),
                            ft.Container(ft.Text("Nombre", weight=ft.FontWeight.BOLD), padding=5,width=200,
                                        border=ft.border.all(1, ft.Colors.GREY_400)),
                            ft.Container(ft.Text("Apellidos", weight=ft.FontWeight.BOLD), padding=5,width=350,
                                        border=ft.border.all(1, ft.Colors.GREY_400)),
                            ft.Container(ft.Text("Sexo", weight=ft.FontWeight.BOLD), padding=5,width=80,alignment=ft.alignment.center, 
                                         border=ft.border.all(1, ft.Colors.GREY_400)),
                            ft.Container(ft.Text("CCAA", weight=ft.FontWeight.BOLD), padding=5, width=200,
                                         border=ft.border.all(1, ft.Colors.GREY_400)),
                            ft.Container(ft.Text("Localidad", weight=ft.FontWeight.BOLD), padding=5,width=200,
                                         border=ft.border.all(1, ft.Colors.GREY_400)),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    # Lista de inscritos (ejemplo)
                   *[
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(
                                        ft.Text(str(inscrito["dorsal"])),
                                            padding=2,
                                            width=80,
                                            alignment=ft.alignment.center_left,
                                            ),
                                    ft.Container(
                                        ft.Text(inscrito["nombre"]),
                                            padding=2,
                                            width=200,
                                            alignment=ft.alignment.center_left,
                                            ),
                                    ft.Container(
                                        ft.Text(inscrito["apellidos"]),
                                            padding=2,
                                            width=350,
                                            alignment=ft.alignment.center_left,
                                            ),
                                    ft.Container(
                                        ft.Text(inscrito["sexo"]),
                                            padding=2,
                                            width=80,
                                            alignment=ft.alignment.center,
                                            ),
                                    ft.Container(
                                        ft.Text(inscrito["ccaa"]),
                                            padding=2,
                                            width=200,
                                            alignment=ft.alignment.center_left,
                                            ),
                                    ft.Container(
                                        ft.Text(inscrito["localidad"]),
                                            padding=2,
                                            width=200,
                                            alignment=ft.alignment.center_left,
                                            ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            # border=ft.border.all(2, ft.Colors.GREY_400),
                            border_radius=8,
                            padding=0,
                            margin=1,
                        )
                         for inscrito in [
                            {
                                "dorsal": i["dorsal"],
                                "nombre": i["nombre"],
                                "apellidos": i["apellidos"],
                                "sexo": i["Sexo"],
                                "ccaa": i["ccaa"],
                                "localidad": i["Localidad"]
                            }
                            for i in inscritos
                        ]
                    ]
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                scroll="auto",
            ),
        )

def main(page: ft.Page):
    page.title = "Listado de Inscritos"
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.add(Inscritos())

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)