import flet as ft
import random
import os


class GaleriaScreen(ft.Container):
    def __init__(self, page=None):  # Add page parameter
        super().__init__(
            alignment=ft.alignment.center,
            expand=True
        )
        self.page = page  # Store the page reference
        
        #------------------------------------------------------------
        fuentes_disponibles=["Algerian","Courier New","Georgia","Cooper Black","Impact","Tahoma","Stencil","Bauhaus 93","Forte","Bernard MT Condensed",]
        colores_disponibles=[
            ft.Colors.RED_900, ft.Colors.GREEN_900, ft.Colors.BLUE_900, ft.Colors.YELLOW_900, ft.Colors.PURPLE_900,
            ft.Colors.BLACK]
        fuente_aleatoria = random.choice(fuentes_disponibles)
        color_aleatorio=random.choice(colores_disponibles)
        
        MAX_WIDTH = 1250
        
        Cabecera = ft.Container(
            content=ft.Text("TRAIL SIERRA DE PEÑASAGRA 2024 - Corremos por Adriana", size=40, 
                            color=color_aleatorio, font_family=fuente_aleatoria),
            border_radius=ft.border_radius.all(20),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.BLUE_GREY_100,
            padding=10,
            margin=10,
            expand=True,
            width=MAX_WIDTH,
        )

        def obtener_fotografias(carpeta):
            # Make sure the os module is used properly
            extensiones_validas = (".jpg", ".jpeg", ".png", ".gif")
            fotos = []
            try:
                fotos = [
                    f"imagenes_galeria/{archivo}"
                    for archivo in os.listdir(carpeta)
                    if archivo.lower().endswith(extensiones_validas)
                ]
            except FileNotFoundError:
                print(f"Error: Carpeta no encontrada: {carpeta}")
            except Exception as e:
                print(f"Error al obtener fotografías: {e}")
            return fotos

        carpeta = "assets\\imagenes_galeria"
        
        fotografias = obtener_fotografias(carpeta)
        
        def dlg_modal(foto):
            # Use self.page instead of page
            if self.page is None:
                print("Error: page is not defined")
                return None
                
            dialogo = ft.AlertDialog( 
                modal=True,
                title=ft.Text("Foto seleccionada"),
                content=ft.Image(src=foto, fit=ft.ImageFit.CONTAIN),#, width=800, height=800),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.close(dialogo)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )    
            return dialogo
                
        def imagen_contenedor(foto, width, height):
            return ft.Container(
                content=ft.Image(src=foto, fit=ft.ImageFit.COVER),
                width=width,
                height=height,
                border_radius=10,
                margin=0,
                bgcolor=ft.Colors.GREY_100,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=5,
                    color=ft.Colors.BLACK26,
                    offset=ft.Offset(2, 2)
                ),
                on_click=lambda e: self.page.open(dlg_modal(foto)) if self.page else None,
            )

        def obtener_datos_imagenes(fotografias):
            datos = []
            for foto in fotografias:
                width = random.choice([300])
                height = random.choice([200,300,350,400])
                datos.append((foto, width, height))
            random.shuffle(datos)
            return datos

        datos_imagenes = obtener_datos_imagenes(fotografias)

        celdas = [imagen_contenedor(foto, width, height) for foto, width, height in datos_imagenes]

        def crear_columnas(celdas, num_columnas):
            columnas = [[] for _ in range(num_columnas)]
            for i, celda in enumerate(celdas):
                columnas[i % num_columnas].append(celda)
            return [
                ft.Column(
                    col,
                    alignment=ft.MainAxisAlignment.START,  # Alineación vertical de los elementos
                    spacing=10 # Puedes ajustar el espacio entre las imágenes dentro de cada columna
                )
                for col in columnas
            ]

        columnas = crear_columnas(celdas, 4)

        Cuerpo = ft.Row(
            columnas,
            vertical_alignment=ft.CrossAxisAlignment.START,  # Alineación horizontal de las columnas dentro del Row
            alignment=ft.MainAxisAlignment.CENTER,  # Alineación vertical de las columnas dentro del Row
            spacing=15,
            expand=True,
            width=MAX_WIDTH,
        )

        # Create the main layout
        main_column = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[Cabecera, Cuerpo],
            expand=True,
        )
        
        # Set the content of the container
        self.content = main_column
        
        #-------------------------------------------------------------
        
        
if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")