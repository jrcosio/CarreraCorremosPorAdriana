import flet as ft
import os
from dotenv import load_dotenv
import logging
from utils.TrailDataBase import TrailDataBase

load_dotenv()
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Constantes
BANDERAS_CCAA = {
    "Andalucía": "banderas/Andalucía.png",
    "Aragón": "banderas/Aragón.png",
    "Asturias": "banderas/Asturias.png",
    "Baleares": "banderas/Baleares.png",
    "Canarias": "banderas/Canarias.png",
    "Cantabria": "banderas/Cantabria.png",
    "Castilla_y_León": "banderas/Castilla_y_León.png",
    "Castilla_La_Mancha": "banderas/Castilla_La_Mancha.png",
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

# Configuración de estilos
COLORES = {
    "titulo": ft.Colors.RED_300,
    "encabezado": ft.Colors.GREY_100,
    "borde": ft.Colors.GREY_400,
}

MEDIDAS = {
    "dorsal": 80,
    "nombre": 200,
    "apellidos": 350,
    "sexo": 80,
    "ccaa": 200,
    "localidad": 200,
    "categoria": 100,
}


class Inscritos(ft.Container):
    """Componente para mostrar la lista de inscritos con filtros por tipo de carrera."""
    
    def __init__(self):
        """Inicializa el componente con datos por defecto (trail)."""
        self.bd = TrailDataBase()
        self.inscritos = []
        self.filtro_activo = "Todos"
        self.edicion = 2025
        
        super().__init__(expand=True)
        
        # Cargar datos iniciales y construir interfaz
        self._cargar_datos_iniciales()
        self._construir_interfaz()
    
    def _cargar_datos_iniciales(self):
        """Carga los datos iniciales (trail por defecto)."""
        try:
            self.inscritos = self.bd.obtener_inscritos_por_edicion(2025)
            log.info(f"Cargados {len(self.inscritos)} inscritos de trail")
        except Exception as e:
            log.error(f"Error cargando datos iniciales: {e}")
            self.inscritos = []
    
    def _construir_interfaz(self):
        """Construye la interfaz completa del componente."""
        self.content = ft.Column(
            controls=[
                self._crear_titulo(),
                self._crear_botones_filtro(),
                self._crear_encabezados_tabla(),
                *self._crear_filas_datos()
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll="auto",
        )
    
    def _crear_titulo(self):
        """Crea el título con contador de participantes."""
        return ft.Column(
            alignment=ft.alignment.center,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    f"Inscritos Trail Peñasagra",
                    size=40,
                    color=COLORES["titulo"],
                    font_family="Britanic Bold",
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"{len(self.inscritos)} participantes",
                    size=26,
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
                on_click=callback,
                bgcolor=ft.Colors.BLUE_100 if es_activo else None,
                color=ft.Colors.BLUE_900 if es_activo else None,
            ),
            padding=5,
            alignment=ft.alignment.center_left,
        )
    
    def _crear_encabezados_tabla(self):
        """Crea la fila de encabezados de la tabla."""
        encabezados = [
            ("Dorsal", MEDIDAS["dorsal"], ft.alignment.center),
            ("Nombre", MEDIDAS["nombre"], ft.alignment.center_left),
            ("Apellidos", MEDIDAS["apellidos"], ft.alignment.center_left),
            ("Sexo", MEDIDAS["sexo"], ft.alignment.center),
            ("CCAA", MEDIDAS["ccaa"], ft.alignment.center_left),
            ("Localidad", MEDIDAS["localidad"], ft.alignment.center_left),
            ("Categoria", MEDIDAS["categoria"], ft.alignment.center),
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
        """Crea una celda de encabezado individual."""
        return ft.Container(
            content=ft.Text(texto, weight=ft.FontWeight.BOLD),
            padding=5,
            width=ancho,
            border=ft.border.all(1, COLORES["borde"]),
            alignment=alineacion,
            #bgcolor=COLORES["encabezado"],
        )
    
    def _crear_filas_datos(self):
        """Crea todas las filas de datos de los inscritos."""
        return [
            self._crear_fila_inscrito(inscrito)
            for inscrito in self.inscritos
        ]
    
    def _crear_fila_inscrito(self, inscrito):
        """Crea una fila individual para un inscrito."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    self._crear_celda_datos(str(inscrito.dorsal), MEDIDAS["dorsal"], ft.alignment.center),
                    self._crear_celda_datos(inscrito.nombre, MEDIDAS["nombre"], ft.alignment.center_left),
                    self._crear_celda_datos(inscrito.apellidos, MEDIDAS["apellidos"], ft.alignment.center_left),
                    self._crear_celda_datos(inscrito.sexo, MEDIDAS["sexo"], ft.alignment.center),
                    self._crear_celda_ccaa(inscrito.ccaa),
                    self._crear_celda_datos(inscrito.municipio, MEDIDAS["localidad"], ft.alignment.center_left),
                    self._crear_celda_datos(
                        self._calcular_categoria(inscrito.fecha_nacimiento), 
                        MEDIDAS["categoria"], 
                        ft.alignment.center
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            border_radius=4,
            padding=0,
            margin=1,
        )
    
    def _crear_celda_datos(self, texto, ancho, alineacion):
        """Crea una celda de datos individual."""
        return ft.Container(
            content=ft.Text(texto),
            padding=2,
            width=ancho,
            alignment=alineacion,
        )
    
    def _crear_celda_ccaa(self, ccaa):
        """Crea la celda especial para CCAA con bandera."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Image(
                        src=BANDERAS_CCAA.get(ccaa),
                        fit=ft.ImageFit.CONTAIN,
                        width=30,
                        height=20,
                    ),
                    ft.Text(ccaa, size=12),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            width=MEDIDAS["ccaa"],
            alignment=ft.alignment.center_left,
        )
    
    def _filtrar_todos(self, e):
        """Maneja el filtro para mostrar todos los inscritos."""
        self._aplicar_filtro("Todos", lambda: self.bd.obtener_inscritos_por_edicion(self.edicion))
    
    def _filtrar_trail(self, e):
        """Maneja el filtro para mostrar solo inscritos de trail."""
        self._aplicar_filtro("Trail", lambda: self.bd.obtener_inscritos_por_tipo_carrera("trail", self.edicion))
    
    def _filtrar_andarines(self, e):
        """Maneja el filtro para mostrar solo inscritos de andarines."""
        self._aplicar_filtro("Andarines", lambda: self.bd.obtener_inscritos_por_tipo_carrera("andarines", self.edicion))
    
    def _aplicar_filtro(self, nombre_filtro, obtener_datos):
        """Aplica un filtro y actualiza la interfaz."""
        try:
            log.info(f"Aplicando filtro: {nombre_filtro}")
            
            self.filtro_activo = nombre_filtro
            self.inscritos = obtener_datos()
            
            log.info(f"Cargados {len(self.inscritos)} inscritos con filtro {nombre_filtro}")
            
            self._construir_interfaz()
            self.update()
            
        except Exception as e:
            log.error(f"Error aplicando filtro {nombre_filtro}: {e}")
    
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



def main(page: ft.Page):
    page.title = "Listado de Inscritos"
    
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.add(Inscritos())

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)