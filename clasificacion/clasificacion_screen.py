import flet as ft
import os
from dotenv import load_dotenv
import logging
from utils.TrailDataBase import TrailDataBase
from datetime import datetime, timedelta

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
    "p.": 40,
    "d.": 40,
    "nombre": 100,
    "apellidos": 200,
    "sexo": 45,
    "ca": 45,
    "cat.": 80,
    "tiempo_final": 100,
    "gap": 80,
    "ritmo": 80,
}

class ClasificacionScreen(ft.Container):
    """Componente para mostrar la clasificación de la carrera."""
    def __init__(self):
        self.bd = TrailDataBase()
        self.clasificacion = []
        self.edicion = 2025
        self.tiempo_ganador = None

        super().__init__(expand=True)
        self._cargar_datos_iniciales()
        self._construir_interfaz()

    def _cargar_datos_iniciales(self):
        try:
            self.clasificacion = self.bd.obtener_clasificaciones_por_edicion(self.edicion)
            # if self.clasificacion:
            #     # Obtener el tiempo del primer clasificado para calcular el gap
            #     self.tiempo_ganador = self.clasificacion[0].tiempo
            # log.info(f"Cargados {len(self.clasificacion)} clasificados")
        except Exception as e:
            log.error(f"Error cargando clasificación: {e}")
            self.clasificacion = []

    def _tiempo_a_segundos(self, tiempo_str):
        """Convierte un tiempo en formato HH:MM:SS a segundos totales."""
        try:
            # Asumiendo formato HH:MM:SS
            if isinstance(tiempo_str, str):
                partes = tiempo_str.split(":")
                if len(partes) == 3:
                    horas, minutos, segundos = map(int, partes)
                    return horas * 3600 + minutos * 60 + segundos
                elif len(partes) == 2:
                    minutos, segundos = map(int, partes)
                    return minutos * 60 + segundos
            return 0
        except (ValueError, AttributeError):
            return 0

    def _segundos_a_tiempo(self, segundos):
        """Convierte segundos totales a formato HH:MM:SS."""
        if segundos == 0:
            return "00:00:00"
        
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segs = segundos % 60
        
        if horas > 0:
            return f"{horas:02d}:{minutos:02d}:{segs:02d}"
        else:
            return f"{minutos:02d}:{segs:02d}"

    def _calcular_gap(self, tiempo_actual):
        """Calcula el gap respecto al tiempo del ganador."""
        if not self.tiempo_ganador or tiempo_actual == self.tiempo_ganador:
            return "00:00:00"
        
        segundos_ganador = self._tiempo_a_segundos(self.tiempo_ganador)
        segundos_actual = self._tiempo_a_segundos(tiempo_actual)
        
        diferencia = segundos_actual - segundos_ganador
        
        if diferencia <= 0:
            return "00:00:00"
        
        return self._segundos_a_tiempo(diferencia)

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
                    f"Clasificación Trail Sierra de Peñasagra",
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
            ("P.", MEDIDAS["p."], ft.alignment.center),
            ("D.", MEDIDAS["d."], ft.alignment.center),
            ("Nombre", MEDIDAS["nombre"], ft.alignment.center_left),
            ("Apellidos", MEDIDAS["apellidos"], ft.alignment.center_left),
            ("Sexo", MEDIDAS["sexo"], ft.alignment.center),
            ("CA", MEDIDAS["ca"], ft.alignment.center),
            ("Cat.", MEDIDAS["cat."], ft.alignment.center),
            ("Tiempo", MEDIDAS["tiempo_final"], ft.alignment.center),
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
            self._crear_fila_clasificado(clasificado, index)
            for  index, clasificado in enumerate(self.clasificacion)
        ]
    
           

    def _crear_fila_clasificado(self, clasificado, index):
        # Calcular el gap dinámicamente
       # gap_calculado = self._calcular_gap(clasificado.tiempo)
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    self._crear_celda_datos(str(index + 1), MEDIDAS["p."], ft.alignment.center),
                    self._crear_celda_datos(str(clasificado.inscrito.dorsal), MEDIDAS["d."], ft.alignment.center),
                    self._crear_celda_datos(clasificado.inscrito.nombre, MEDIDAS["nombre"], ft.alignment.center_left),
                    self._crear_celda_datos(clasificado.inscrito.apellidos, MEDIDAS["apellidos"], ft.alignment.center_left),
                    self._crear_celda_datos(clasificado.inscrito.sexo, MEDIDAS["sexo"], ft.alignment.center),
                    self._crear_celda_ccaa(clasificado.inscrito.ccaa),
                    self._crear_celda_datos(
                        self._calcular_categoria(clasificado.inscrito.fecha_nacimiento), 
                                 MEDIDAS["cat."], 
                        ft.alignment.center),
                    self._crear_celda_datos(clasificado.tiempo_final, MEDIDAS["tiempo_final"], ft.alignment.center),
                    self._crear_celda_datos("gap", MEDIDAS["gap"], ft.alignment.center),
                    self._crear_celda_datos("rit", MEDIDAS["ritmo"], ft.alignment.center),
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
            content=ft.Text(str(texto), color="#ffcb2e", size=20),
            padding=2,
            width=ancho,
            alignment=alineacion,
        )

    def _crear_celda_ccaa(self, ca):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Image(
                        src=BANDERAS_CCAA.get(ca),
                        fit=ft.ImageFit.CONTAIN,
                        width=30,
                        height=20,
                    ),
                    # ft.Text(ccaa, size=16, color="#ffcb2e"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=MEDIDAS["ca"],
            alignment=ft.alignment.center,
        )
        
    def _calcular_categoria(self, fecha_nacimiento):
        """Calcula la categoría basada en la fecha de nacimiento."""
        try:
            year = fecha_nacimiento.year
            
            categorias = [
                (1975, "VET C"),
                (1979, "VET B"),
                (1985, "VET A"),
                (2007, "SENIOR"),
                (float('inf'), "JUNIOR"),
            ]
            
            for limite_año, categoria in categorias:
                if year <= limite_año:
                    return categoria
                    
            return "N/A"
            
        except Exception as e:
            log.error(f"Error calculando categoría para fecha {fecha_nacimiento}: {e}")
            return "N/A"