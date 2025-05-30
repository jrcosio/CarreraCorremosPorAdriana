import flet as ft
from home.contador import CountdownTimer
from datetime import datetime, timedelta
import flet_video as fv
import flet_webview as fw

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
        
        portada1 = ft.Image(
            src="imagenes_home/header_izq_adri.png",
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(20),
            # width=400,
            # height=200,
            )
        portada2 = ft.Image(
            src="imagenes_home/banner_adriana_rosa.png",
            expand=True,
            #width=400,
            height=200,
            fit=ft.ImageFit.CONTAIN,
        )
        portada3 = ft.Image(
            src="imagenes_home/header_der_adri.png",
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(20),
            # width=400,
            # height=200,
        )

        adriana = ft.Row(
            [portada1, portada2, portada3],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            #expand=True,
        )
     
        
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
        
            
        def dlg_modal(video):
            # Use self.page instead of page
            if self.page is None:
                print("Error: page is not defined")
                return None
                
            dialogo = ft.AlertDialog( 
                modal=False,
                bgcolor=ft.Colors.GREY_500,
                content=fv.Video(
                    playlist=[fv.VideoMedia(video)],
                    playlist_mode=fv.PlaylistMode.LOOP,
                    show_controls=True,
                    autoplay=True,
                    muted=True,  # Necesario para autoplay
                    width=1020,
                    height=580,
                ),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.close(dialogo),
                                  style=ft.ButtonStyle(color=ft.Colors.BLACK)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )    
            return dialogo
        
        andarines = ft.Container(
            content=ft.Image(
                    src="imagenes_home/andarines.png", 
                    fit=ft.ImageFit.CONTAIN,
                    expand=True,  # Añadido aquí
            ),
            expand=True,
            on_click=lambda e: self.page.open(dlg_modal("videos/andarines.mp4")) if self.page else None,
        )
        
        runers = ft.Container(
            content=ft.Image(
                src="imagenes_home/trail.png", 
                fit=ft.ImageFit.CONTAIN,
                expand=True,  # Añadido aquí
            ),
            expand=True,
            on_click=lambda e: self.page.open(dlg_modal("videos/trail.mp4")) if self.page else None, 
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
                                width=300,
                                height=300
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
            ("imagenes_patrocinadores/banner_LIS.png","URL"),
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
    print("A donde vas so animal... no se ejecuta este archivo")
    print("Ve a main.py y ejecuta desde ahí")