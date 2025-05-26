import flet as ft
from contador import CountdownTimer
from datetime import datetime, timedelta

class HomeScreen(ft.Container):
    def __init__(self):
        super().__init__(
            alignment=ft.alignment.center,
            expand=True
        )

        #------------------------------------------------------------
        fecha_carrera = ft.Container(
            content=ft.Text("12 de Julio de 2025", size=40, color=ft.Colors.BLACK, 
            font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True),
            alignment=ft.alignment.top_center,
            bgcolor=ft.Colors.YELLOW,  # Cambiado a un color estándar
            expand=True,
            border_radius=ft.border_radius.only(top_left=20, top_right=20)  
        )
        
        lugar_carrera = ft.Container(
            content=ft.Text("Cosío - Rionansa", size=40, color=ft.Colors.BLACK,
            font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True),
            alignment=ft.alignment.top_center,
            bgcolor=ft.Colors.YELLOW,  # Cambiado a un color estándar
            expand=True, 
            border_radius=ft.border_radius.only(top_left=20, top_right=20) 
        )
        
        adriana = ft.Container(
            content=ft.Text("Texto Adri", size=40, color=ft.Colors.BLACK, 
                font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True),
            alignment=ft.alignment.center,
            height=100,  
            bgcolor=ft.Colors.RED_100
        )   
        
       
        
        def main(page: ft.Page):
            page.title = "Contador Regresivo"
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Fecha objetivo (ejemplo: 6 horas en el futuro)
    #target = datetime.now() + timedelta(hours=6)
        target = datetime(2025, 7, 12, 10, 00, 00)  # Fecha objetivo específica
    
        def on_countdown_finish(timer):
            #TODO
            pass  # Aquí puedes definir lo que sucede cuando el contador llega a cero
    
    # Crear un contenedor centrado para el contador
        countdown_container = ft.Container(
            content= ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Tan solo nos faltan.", size=32, color=ft.Colors.BLACK),
                    CountdownTimer(
                        target_date=target,
                        on_finish=on_countdown_finish,
                        padding=5,
                        bgcolor=None,  # Transparente para que se vea el fondo del contenedor principal
                    ),
                ]
                
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.WHITE,
            padding=20,
        )
        
            
        
        andarines = ft.Container(
            content=ft.Stack(
                [
                    ft.Image(
                        src="imagenes_home/andarinesmubravos.jpg", 
                        fit=ft.ImageFit.CONTAIN,
                        expand=True,  # Añadido aquí
                    ),
                    ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            "Distancia: 14 km",
                            size=32,
                            color=ft.Colors.BLACK,
                            font_family="Britanic Bold",
                            weight=ft.FontWeight.BOLD,
                            italic=True,
                        ),
                        alignment=ft.alignment.top_center,
                        padding=10,
                    ),
                    ft.Container(
                        expand=True  # Contenedor vacío que ocupa el espacio intermedio
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Andarines",
                            size=32,
                            color=ft.Colors.BLACK,
                            font_family="Britanic Bold",
                            weight=ft.FontWeight.BOLD,
                            italic=True,
                        ),
                        alignment=ft.alignment.bottom_center,
                        padding=10,
                    ),
                ],
                expand=True,
            ),
        ],
    ),
    expand=True,
)
        runers = ft.Container(
            content=ft.Stack(
                [
                    ft.Image(
                        src="imagenes_home/trailnuevo.jpg", 
                        fit=ft.ImageFit.CONTAIN,
                        expand=True,  # Añadido aquí
                    ),
                    ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            "Distancia: 20 km",
                            size=32,
                            color=ft.Colors.YELLOW,
                            font_family="Britanic Bold",
                            weight=ft.FontWeight.BOLD,
                            italic=True,
                        ),
                        alignment=ft.alignment.top_center,
                        padding=10,
                    ),
                    ft.Container(
                        expand=True  # Contenedor vacío que ocupa el espacio intermedio
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Trail",
                            size=32,
                            color=ft.Colors.YELLOW,
                            font_family="Britanic Bold",
                            weight=ft.FontWeight.BOLD,
                            italic=True,
                        ),
                        alignment=ft.alignment.bottom_center,
                        padding=10,
                    ),
                ],
                # expand=True,
            ),
        ],
    ),
    expand=True,
)
        cabecera = ft.Row(
            [fecha_carrera, lugar_carrera],  # Eliminada coma adicional
            alignment=ft.MainAxisAlignment.CENTER,
        )

        portada = ft.Row(
            [andarines, runers],  # Eliminada coma adicional
            alignment=ft.MainAxisAlignment.CENTER,
        )

        
        
        def logos_container(titulo, imagenes_lista, color_fondo=ft.Colors.TRANSPARENT):
            # Agrupar las imágenes en filas de 4
            filas_imagenes = [
                imagenes_lista[i:i+4]
                for i in range(0, len(imagenes_lista), 4)
            ]

            return ft.Container(
                padding=10,
                bgcolor=color_fondo,
                content=ft.Column(
                [
                    ft.Text(
                    value=titulo,
                    size=27,
                    color=ft.Colors.BLACK,
                    font_family="Britanic Bold",
                    weight=ft.FontWeight.BOLD,
                    italic=True
                    ),
                    *[
                    ft.Row(
                        [
                        ft.Container(
                            content=ft.Image(
                                src=img[0],
                                fit=ft.ImageFit.CONTAIN,
                                width=200,
                                height=200
                            ),
                            on_click=lambda e, url=img[1]: print(f"Clicked: {url}"),
                            bgcolor=ft.Colors.TRANSPARENT,
                            border_radius=10,
                            padding=2,
                        )
                        for img in fila
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    )
                    for fila in filas_imagenes
                    ]
                ],
                ),
            )
        
        imagenes_patrocinadores = [
            ("imagenes_patrocinadores/patrocinador.png","URL"),
            ("imagenes_patrocinadores/patrocinador.png","URL"),
            ("imagenes_patrocinadores/patrocinador.png","URL"),
            ("imagenes_patrocinadores/patrocinador.png","URL"),
            ("imagenes_patrocinadores/patrocinador.png","URL"),
            ("imagenes_patrocinadores/patrocinador.png","URL"), 
        ]
        
        imagenes_colaboradores = [
            ("imagenes_colaboradores/colaborador.png","URL"),
            ("imagenes_colaboradores/colaborador.png","URL"),
            ("imagenes_colaboradores/colaborador.png","URL"),
            ("imagenes_colaboradores/colaborador.png","URL"),
            ("imagenes_colaboradores/colaborador.png","URL"),
            ("imagenes_colaboradores/colaborador.png","URL"),           
        ]
        
        imagenes_organizadores = [
            ("imagenes_organizadores/logo.png","URL"),
        ]
        
        
        patrocinadores = logos_container("Patrocinadores", imagenes_patrocinadores , ft.Colors.YELLOW_100)
        colaboradores = logos_container("Colaboradores", imagenes_colaboradores, ft.Colors.GREEN_100)
        organizadores = logos_container("Organizadores", imagenes_organizadores, ft.Colors.BLUE_GREY_300)
        
        
        self.content = ft.Column(
            [
                adriana,
                countdown_container,
                cabecera,
                portada,
                patrocinadores,
                colaboradores,
                organizadores
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            expand=True,
        )
    #------------------------------------------------------------
        
        
        
if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")