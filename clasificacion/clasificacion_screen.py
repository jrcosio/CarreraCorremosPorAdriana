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
    "nombre": 115,
    "apellidos": 245,
    "sexo": 45,
    "ca": 50,
    "cat.": 80,
    "tiempo_final": 100,
    "gap": 90,
    "ritmo": 80,
}

class ClasificacionScreen(ft.Container):
    """Componente para mostrar la clasificación de la carrera."""
    def __init__(self):
        self.bd = TrailDataBase()
        self.clasificacion = []
        self.clasificacion_completa = []
        self.filtro_activo = "Todos"
        self.edicion = 2025
        self.tiempo_ganador = None

        super().__init__(expand=True)
        self._cargar_datos_iniciales()
        self._construir_interfaz()

    def _aplicar_filtro(self):
        """Aplica el filtro seleccionado y actualiza la interfaz."""
        try:
            if self.filtro_activo == "Todos":
                self.clasificacion = self.clasificacion_completa.copy()
            elif self.filtro_activo == "Trail":
                self.clasificacion = [c for c in self.clasificacion_completa if c.inscrito.tipo_carrera == "trail"]
            elif self.filtro_activo == "Andarines":
                self.clasificacion = [c for c in self.clasificacion_completa if c.inscrito.tipo_carrera == "andarines"]

            # Actualizar tiempo ganador para el filtro aplicado
            self.tiempo_ganador = self.clasificacion[0].tiempo_final if self.clasificacion else None
            
            # Actualizar solo los datos en la interfaz
            self._actualizar_datos_tabla()
            
        except Exception as e:
            print(f"Error aplicando filtro: {e}")

    def _actualizar_datos_tabla(self):
        """Actualiza solo la tabla de datos manteniendo el resto de la interfaz."""
        try:
            # Crear nuevas filas de datos
            nuevas_filas = self._crear_filas_datos()
            
            # Actualizar el contenido del contenedor de datos
            self.datos_container.controls = nuevas_filas
            
            # Actualizar botones para reflejar el filtro activo
            self._actualizar_botones_filtro()
            
            # Forzar actualización
            self.update()
            
        except Exception as e:
            print(f"Error actualizando tabla: {e}")

    def _actualizar_botones_filtro(self):
        """Actualiza el estado visual de los botones de filtro."""
        try:
            # Recrear los botones con el estado actual
            nuevos_botones = [
                self._crear_boton_filtro("Todos", self._filtrar_todos),
                self._crear_boton_filtro("Trail", self._filtrar_trail),
                self._crear_boton_filtro("Andarines", self._filtrar_andarines),
            ]
            
            self.botones_container.controls = nuevos_botones
            
        except Exception as e:
            print(f"Error actualizando botones: {e}")

    def _cargar_datos_iniciales(self):
        try:
            self.clasificacion_completa = self.bd.obtener_clasificaciones_por_edicion(self.edicion)
            self.clasificacion = self.clasificacion_completa.copy()
            self.tiempo_ganador = self.clasificacion[0].tiempo_final if self.clasificacion else None
            print(f"---------------------Tiempo del ganador: {self.tiempo_ganador}")
            print(type(self.tiempo_ganador))
        except Exception as e:
            print(f"Error cargando clasificación: {e}")
            self.clasificacion = []
            self.clasificacion_completa = []

    def _tiempo_a_segundos(self, tiempo_str):
        """Convierte un tiempo en formato HH:MM:SS a segundos totales."""
        try:
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

    def _formatear_duracion(self, duracion):
        """Formatea un objeto timedelta a formato HH:MM:SS."""
        if not duracion:
            return "00:00:00"
        
        total_segundos = int(duracion.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    def _calcular_gap(self, tiempo_actual: datetime):
        """Calcula el gap respecto al tiempo del ganador."""
        if not self.tiempo_ganador or not tiempo_actual:
            return ""

        if tiempo_actual == self.tiempo_ganador:
            return ""
        
        gap = tiempo_actual - self.tiempo_ganador
        return self._formatear_duracion(gap)
        
    def _calcular_ritmo(self, tiempo_final: datetime, tiempo_inicio: datetime, tipo_carrera: str):
        """Calcula el ritmo (min/km) según el tipo de carrera y el tiempo."""
        if not tiempo_final or not tiempo_inicio or not tipo_carrera:
            return ""
            
        if tipo_carrera == "trail":
            distancia = 20
        elif tipo_carrera == "andarines":
            distancia = 15
        else:
            return ""

        duracion = tiempo_final - tiempo_inicio
        segundos_totales = duracion.total_seconds()
        
        if segundos_totales <= 0:
            return ""
        
        minutos_totales = segundos_totales / 60
        ritmo_min_por_km = minutos_totales / distancia
        
        minutos = int(ritmo_min_por_km)
        segundos = int((ritmo_min_por_km - minutos) * 60)
        
        return f"{minutos:02d}:{segundos:02d}"

    def _construir_interfaz(self):
        """Construye la interfaz inicial."""
        self.titulo_container = self._crear_titulo()
        self.botones_container = self._crear_botones_filtro()
        self.encabezados_container = self._crear_encabezados_tabla()
        self.datos_container = ft.Column(
            controls=self._crear_filas_datos(),
            spacing=1,
        )

        self.content = ft.Column(
            controls=[
                self.titulo_container,
                self.botones_container,
                self.encabezados_container,
                self.datos_container,
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
            ]
        )

    def _crear_botones_filtro(self):
        """Crea la fila de botones de filtro."""
        return ft.Row(
            controls=[
                self._crear_boton_filtro("Todos", self._filtrar_todos),
                self._crear_boton_filtro("Trail", self._filtrar_trail),
                self._crear_boton_filtro("Andarines", self._filtrar_andarines),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
    
    def _crear_boton_filtro(self, texto, callback):
        """Crea un botón de filtro individual."""
        es_activo = self.filtro_activo == texto
        
        return ft.Container(
            content=ft.ElevatedButton(
                text=texto,
                width=200,
                on_click=callback,
                bgcolor=ft.Colors.BLUE_100 if es_activo else ft.Colors.GREY_300,
                color=ft.Colors.BLUE_900 if es_activo else ft.Colors.BLACK,
            ),
            padding=5,
            alignment=ft.alignment.center_left,
        )

    def _crear_encabezados_tabla(self):
        encabezados = [
            ("P.", MEDIDAS["p."], ft.alignment.center),
            ("D.", MEDIDAS["d."], ft.alignment.center),
            ("Nombre", MEDIDAS["nombre"], ft.alignment.center_left),
            ("Apellidos", MEDIDAS["apellidos"], ft.alignment.center_left),
            ("Sexo", MEDIDAS["sexo"], ft.alignment.center),
            ("CCAA", MEDIDAS["ca"], ft.alignment.center),
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
        return [self._crear_fila_clasificado(clasificado, index) 
                for index, clasificado in enumerate(self.clasificacion)]

    def _crear_fila_clasificado(self, clasificado, index):
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
                        ft.alignment.center
                    ),
                    self._crear_celda_datos(self._formatear_tiempo_final(clasificado.tiempo_final, clasificado.tiempo_p1), MEDIDAS["tiempo_final"], ft.alignment.center),
                    self._crear_celda_datos(self._calcular_gap(clasificado.tiempo_final), MEDIDAS["gap"], ft.alignment.center),
                    self._crear_celda_datos(self._calcular_ritmo(clasificado.tiempo_final, clasificado.tiempo_p1, clasificado.inscrito.tipo_carrera), MEDIDAS["ritmo"], ft.alignment.center),
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
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=MEDIDAS["ca"],
            alignment=ft.alignment.center,
        )
    
    def _filtrar_todos(self, e):
        """Maneja el filtro para mostrar todos los inscritos."""
        self.filtro_activo = "Todos"
        self._aplicar_filtro()
    
    def _filtrar_trail(self, e):
        """Maneja el filtro para mostrar solo inscritos de trail."""
        self.filtro_activo = "Trail"
        self._aplicar_filtro()
    
    def _filtrar_andarines(self, e):
        """Maneja el filtro para mostrar solo inscritos de andarines."""
        self.filtro_activo = "Andarines"
        self._aplicar_filtro()
    
    def _actualizar_tiempo_ganador(self):
        """Actualiza el tiempo del ganador (posición 1 del listado)."""
        # El ganador es simplemente el primer elemento de la lista
        self.tiempo_ganador = self.clasificacion[0].tiempo_final if self.clasificacion else None
    
    def calcular_gap(tiempo_ganador, tiempo_final):
        """Calcula el gap entre dos tiempos"""
        if not tiempo_ganador or not tiempo_final:
            return " "
        return abs((tiempo_final - tiempo_ganador).total_seconds())
            
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
            return "N/A"
    
    def _formatear_tiempo_final(self, tiempo_final, tiempo_inicio):
        """Formatea el tiempo final de la carrera manejando valores None."""
        if not tiempo_final or not tiempo_inicio:
            return "N/A"
        
        try:
            duracion = tiempo_final - tiempo_inicio
            return self._formatear_duracion(duracion)
        except (TypeError, AttributeError):
            return "N/A"