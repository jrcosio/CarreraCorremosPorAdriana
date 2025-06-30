import flet as ft
import os
from dotenv import load_dotenv
import logging
from utils.TrailDataBase import TrailDataBase

load_dotenv()
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

BANDERAS_CCAA = {
    "Andalucía": "banderas/Andalucía.png",
    "Aragón": "banderas/Aragón.png",
    "Asturias": "banderas/Asturias.png",
    "Baleares": "banderas/Baleares.png",
    "Canarias": "banderas/Canarias.png",
    "Cantabria": "banderas/Cantabria.png",
    "Castilla y León": "banderas/Castilla_y_León.png",
    "Castilla La Mancha": "banderas/Castilla_La_Mancha.png",
    "Cataluña": "banderas/Catalunya.png",
    "Comunidad Valenciana": "banderas/Comunidad Valenciana.png",
    "Extremadura": "banderas/Extremadura.png",
    "Galicia": "banderas/Galicia.png",
    "La Rioja": "banderas/La Rioja.png",
    "Madrid": "banderas/Madrid.png",
    "Murcia": "banderas/Murcia.png",
    "Navarra": "banderas/Navarra.png",
    "País Vasco": "banderas/País Vasco.png",
}

COLORES = {
    "titulo": "#ffcb2e",
    "encabezado": ft.Colors.GREY_100,
    "borde": ft.Colors.WHITE,
}

MEDIDAS = {
    "puesto": 70,
    "dorsal": 80,
    "nombre": 160,
    "apellidos": 250,
    "sexo": 60,
    "ccaa": 120,
    "localidad": 120,
    "categoria": 100,
    "tiempo_p1": 100,
    "tiempo_meta": 100,
    "gap": 80,
    "ritmo": 80,
}

class ClasificacionScreen(ft.Container):
    """Componente para mostrar la clasificación de la carrera."""
    def __init__(self):
        self.bd = TrailDataBase()
        self.clasificacion = []
        self.edicion = 2025

        super().__init__(expand=True)
        self._cargar_datos_iniciales()
        self._construir_interfaz()

    def _cargar_datos_iniciales(self):
        try:
            self.clasificacion = self.bd.obtener_clasificacion_por_edicion(self.edicion)
            log.info(f"Cargados {len(self.clasificacion)} clasificados")
        except Exception as e:
            log.error(f"Error cargando clasificación: {e}")
            self.clasificacion = []

    def _construir_interfaz(self):
        self.content = ft.Column(
            controls=[
                self._crear_titulo(),
                self._crear_encabezados_tabla(),
                *self._crear_filas_datos(),
                ft.Container(height=30),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll="auto",
        )

    def _crear_titulo(self):
        return ft.Column(
            alignment=ft.alignment.center,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(height=10),
                ft.Text(
                    f"Clasificación Trail Peñasagra",
                    size=40,
                    color=COLORES["titulo"],
                    font_family="Britanic Bold",
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"{len(self.clasificacion)} clasificados",
                    size=24,
                    color=COLORES["titulo"],
                    font_family="Britanic Bold",
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            ]
        )

    def _crear_encabezados_tabla(self):
        encabezados = [
            ("Puesto", MEDIDAS["puesto"], ft.alignment.center),
            ("Dorsal", MEDIDAS["dorsal"], ft.alignment.center),
            ("Nombre", MEDIDAS["nombre"], ft.alignment.center_left),
            ("Apellidos", MEDIDAS["apellidos"], ft.alignment.center_left),
            ("Sexo", MEDIDAS["sexo"], ft.alignment.center),
            ("CCAA", MEDIDAS["ccaa"], ft.alignment.center_left),
            ("Localidad", MEDIDAS["localidad"], ft.alignment.center_left),
            ("Categoria", MEDIDAS["categoria"], ft.alignment.center),
            ("Tiempo P1", MEDIDAS["tiempo_p1"], ft.alignment.center),
            ("Tiempo Meta", MEDIDAS["tiempo_meta"], ft.alignment.center),
            ("Gap", MEDIDAS["gap"], ft.alignment.center),
            ("Ritmo", MEDIDAS["ritmo"], ft.alignment.center),
        ]
        return ft.Row(
            controls=[
                self._crear_celda_encabezado(texto, ancho, alineacion)
                for texto, ancho, alineacion in encabezados
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

    def _crear_celda_encabezado(self, texto, ancho, alineacion):
        return ft.Container(
            content=ft.Text(texto, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            padding=5,
            width=ancho,
            border=ft.border.all(1, COLORES["borde"]),
            alignment=alineacion,
        )

    def _crear_filas_datos(self):
        return [
            self._crear_fila_clasificado(clasificado)
            for clasificado in self.clasificacion
        ]

    def _crear_fila_clasificado(self, clasificado):
        return ft.Container(
            content=ft.Row(
                controls=[
                    self._crear_celda_datos(str(clasificado.puesto), MEDIDAS["puesto"], ft.alignment.center),
                    self._crear_celda_datos(str(clasificado.dorsal), MEDIDAS["dorsal"], ft.alignment.center),
                    self._crear_celda_datos(clasificado.nombre, MEDIDAS["nombre"], ft.alignment.center_left),
                    self._crear_celda_datos(clasificado.apellidos, MEDIDAS["apellidos"], ft.alignment.center_left),
                    self._crear_celda_datos(clasificado.sexo, MEDIDAS["sexo"], ft.alignment.center),
                    self._crear_celda_ccaa(clasificado.ccaa),
                    self._crear_celda_datos(clasificado.municipio, MEDIDAS["localidad"], ft.alignment.center_left),
                    self._crear_celda_datos(clasificado.categoria, MEDIDAS["categoria"], ft.alignment.center),
                    self._crear_celda_datos(clasificado.tiempo_p1, MEDIDAS["tiempo_p1"], ft.alignment.center),
                    self._crear_celda_datos(clasificado.tiempo_meta, MEDIDAS["tiempo_meta"], ft.alignment.center),
                    self._crear_celda_datos(clasificado.gap, MEDIDAS["gap"], ft.alignment.center),
                    self._crear_celda_datos(clasificado.ritmo, MEDIDAS["ritmo"], ft.alignment.center),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            border_radius=4,
            padding=0,
            margin=1,
        )

    def _crear_celda_datos(self, texto, ancho, alineacion):
        return ft.Container(
            content=ft.Text(str(texto), color="#ffcb2e", size=16),
            padding=2,
            width=ancho,
            alignment=alineacion,
        )

    def _crear_celda_ccaa(self, ccaa):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Image(
                        src=BANDERAS_CCAA.get(ccaa),
                        fit=ft.ImageFit.CONTAIN,
                        width=30,
                        height=20,
                    ),
                    ft.Text(ccaa, size=16, color="#ffcb2e"),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            width=MEDIDAS["ccaa"],
            alignment=ft.alignment.center_left,
        )