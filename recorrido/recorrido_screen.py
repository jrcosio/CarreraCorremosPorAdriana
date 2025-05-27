import flet as ft
from recorrido.WikilocMapContainer import WikilocMapContainer


class RecorridoScreen(ft.Container):
    """
    Pantalla que muestra los detalles de un recorrido incluyendo información
    básica, mapa y estadísticas del recorrido.
    """
    
    def __init__(self, recorrido_data):
        """
        Inicializa la pantalla del recorrido.
        
        Args:
            recorrido_data (dict): Diccionario con los datos del recorrido que debe contener:
                - titulo: Título del recorrido
                - descripcion: Descripción del recorrido
                - fecha: Fecha del recorrido
                - hora: Hora del recorrido
                - lugar: Lugar del recorrido
                - wikilog: ID del trail en Wikiloc
                - distancia: Distancia en km
                - desnivel: Desnivel en metros
        """
        self.recorrido_data = recorrido_data
        
        super().__init__(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self._create_header(),
                    self._create_main_content(),
                    self._create_boton_tracking(),
                    self._create_map3D_container(),
                ]
            )
        )
    
    def _create_header(self):
        """Crea la sección del encabezado con título y descripción."""
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    self.recorrido_data["titulo"],
                    weight=ft.FontWeight.BOLD,
                    size=48,
                    color=ft.Colors.BLACK,
                    font_family="Roboto",
                ),
                ft.Text(
                    self.recorrido_data["descripcion"],
                    size=24,
                    color=ft.Colors.BLACK,
                    font_family="Roboto",
                ),
            ]
        )
    
    def _create_main_content(self):
        """Crea el contenido principal con información del recorrido y mapa."""
        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self._create_left_info_panel(),
                self._create_map_container(),
                self._create_right_info_panel(),
            ]
        )
    
    def _create_left_info_panel(self):
        """Crea el panel izquierdo con información de fecha y lugar."""
        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,  # Espaciado entre los círculos
            controls=[
                self._create_date_container(),
                self._create_location_container(),
            ]
        )
    
    def _create_right_info_panel(self):
        """Crea el panel derecho con información de distancia y desnivel."""
        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,  # Espaciado entre los contenedores
            controls=[
                self._create_distance_container(),
                self._create_elevation_container(),
            ]
        )
    
    def _create_date_container(self):
        """Crea el contenedor circular con información de fecha y hora."""
        return self._create_circular_info_container(
            image_src="imagenes_recorrido/calendario.png",
            primary_text=self.recorrido_data['fecha'],
            secondary_text=self.recorrido_data['hora'],
            label_text="FECHA"
        )
    
    def _create_location_container(self):
        """Crea el contenedor circular con información del lugar."""
        return self._create_circular_info_container(
            image_src="imagenes_recorrido/punto.png",
            primary_text=self.recorrido_data['lugar'],
            secondary_text="Cantabria",
            label_text="LUGAR"
        )
    
    def _create_circular_info_container(self, image_src, primary_text, secondary_text, label_text):
        """
        Crea un contenedor circular con imagen y textos.
        
        Args:
            image_src (str): Ruta de la imagen
            primary_text (str): Texto principal
            secondary_text (str): Texto secundario (opcional)
            label_text (str): Etiqueta descriptiva
            
        Returns:
            ft.Container: Contenedor circular con la información
        """
        controls = [
            ft.Image(
                src=image_src,
                width=45,
                height=45,
                fit=ft.ImageFit.CONTAIN
            ),
            ft.Text(
                primary_text,
                size=24,
                color=ft.Colors.BLACK,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            )
        ]
        
        # Solo agregar texto secundario si no está vacío
        if secondary_text.strip():
            controls.append(
                ft.Text(
                    secondary_text,
                    size=14,
                    color=ft.Colors.BLACK,
                    text_align=ft.TextAlign.CENTER
                )
            )
        
        controls.append(
            ft.Text(
                label_text,
                size=9,
                color=ft.Colors.BLACK54,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            )
        )
        
        return ft.Container(
            content=ft.Column(
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=controls
            ),
            **self._get_circular_container_style()
        )
    
    def _create_distance_container(self):
        """Crea el contenedor circular con información de distancia."""
        return self._create_circular_info_container(
            image_src="imagenes_recorrido/run.png",
            primary_text=f"{self.recorrido_data['distancia']} km",
            secondary_text="",  # Sin texto secundario
            label_text="DISTANCIA"
        )
    
    def _create_elevation_container(self):
        """Crea el contenedor circular con información de desnivel."""
        return self._create_circular_info_container(
            image_src="imagenes_recorrido/mont.png",
            primary_text=f"{self.recorrido_data['desnivel']} m",
            secondary_text="",  # Sin texto secundario
            label_text="DESNIVEL"
        )
    
    def _create_map_container(self):
        """Crea el contenedor del mapa."""
        return WikilocMapContainer(
            trail_id=self.recorrido_data["wikilog"],
            width=1000,
            height=600,
        )
        
    def _create_map3D_container(self):
        """Crea el contenedor del mapa."""
        return WikilocMapContainer(
            trail_id=self.recorrido_data["wikilog"],
            width=1000,
            height=600,
        )
    
    def download_track(self, e, track):          # Función para descargar la imagen
        self.page.launch_url(track, web_popup_window=True)
        
        
    
    def _create_boton_tracking(self):
        """Crea el botón de tracking para iniciar el recorrido."""
        return ft.Container(
            content=ft.ElevatedButton(
            content=ft.Row(
                controls=[
                ft.Icon(ft.Icons.DOWNLOAD),
                ft.Text(
                    "Descargar track de la ruta",
                    size=24,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            on_click=lambda e: self.download_track(e, self.recorrido_data["track"]),
            height=50,
            width=400,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(20),
        )
    
    def _get_circular_container_style(self):
        """
        Retorna el estilo para contenedores circulares de información.
        
        Returns:
            dict: Diccionario con las propiedades de estilo circular
        """
        return {
            "bgcolor": "#f1f18c",
            "border": ft.border.all(2, ft.Colors.BLACK),
            "border_radius": ft.border_radius.all(75),  # Radio para hacer círculo perfecto
            "width": 150,
            "height": 150,
            "padding": ft.padding.all(10),
            "alignment": ft.alignment.center,
        }
   