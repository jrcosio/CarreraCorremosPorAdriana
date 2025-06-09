import flet as ft
import flet_video as fv
import flet_webview as fw
from home.contador import CountdownTimer # Asumimos que este import es correcto
from datetime import datetime
from configurar_web import imagenes_colaboradores, imagenes_organizadores, imagenes_patrocinadores


class HomeScreen(ft.Container):
    def __init__(self, page: ft.Page = None, on_click=None):
        super().__init__(
            alignment=ft.alignment.center,
            expand=True
        )
        self.page = page
        self.on_click = on_click
        
        # --- SECCIÓN 1: CABECERA CON 3 IMÁGENES ---
        portada1 = ft.Image(
            src="imagenes_home/izquierda.png",
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(20),
            height=104,
        )
        portada2 = ft.Image(
            src="imagenes_home/banner_adriana_rosa.png",
            fit=ft.ImageFit.CONTAIN,
        )
        portada3 = ft.Image(
            src="imagenes_home/derecha.png",
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(20),
            height=104,
        )
        
        # --- SECCIÓN NEW --- Boton de Inscripción ---
        btn_inscripcion = ft.TextButton(
                " Inscríbete aquí ",
                data="btn_inscripcion",
                on_click= self.on_click,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        size=30,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.RED_300,
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=ft.padding.all(20)
                ),
            )

        # --- SECCIÓN 2: CONTADOR ---
        target = datetime(datetime.now().year, 7, 12, 10, 0, 0)
        countdown_container = ft.Container(
            content=ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Tan solo nos faltan", size=30, color=ft.Colors.BLACK),
                    CountdownTimer(target_date=target, on_finish=lambda: None),                ]
            ),
            
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.WHITE,
        )
        
        
        # --- SECCIÓN 4: VÍDEOS (ANDARINES Y RUNNERS) ---
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
                    # height=580,
                ),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: self.page.close(dialogo),
                                  style=ft.ButtonStyle(color=ft.Colors.BLACK)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )    
            return dialogo

        fecha_carrera = ft.Container(
            content=ft.Text("12 de Julio de 2025", size=30, color=ft.Colors.BLACK,
                            font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True, text_align=ft.TextAlign.CENTER),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.YELLOW,
            expand=True,
            padding=10,
            border_radius=ft.border_radius.only(top_left=20, top_right=20)
        )
        lugar_carrera = ft.Container(
            content=ft.Text("Cosío - Rionansa", size=30, color=ft.Colors.BLACK,
                            font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True, text_align=ft.TextAlign.CENTER),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.YELLOW,
            expand=True,
            padding=10,
            border_radius=ft.border_radius.only(top_left=20, top_right=20)
        )
        andarines = ft.Container(
            content=ft.Image(src="imagenes_home/andarines.png", fit=ft.ImageFit.CONTAIN, expand=True),
            # expand=True,
            on_click=lambda e: self.page.open(dlg_modal("videos/andarines.mp4")) if self.page else None,
        )
        trail = ft.Container(
            content=ft.Image(src="imagenes_home/principal_trail1.png", fit=ft.ImageFit.CONTAIN, expand=True),
            expand=True,
            on_click=lambda e: self.page.open(dlg_modal("videos/trail.mp4")) if self.page else None,
        )
         
        andarine_block = ft.Container(
            col={"md": 6, "xs": 12, "sm": 12},
            expand=True,
            content=ft.Column(
                spacing=0,
                controls=[
                    fecha_carrera,
                    andarines
                ],
            )
        )      
        
        trail_block = ft.Container(
            col={"md": 6, "xs": 12, "sm": 12},
            expand=True,
            content=ft.Column(
                spacing=0,
                controls=[
                    lugar_carrera,
                    trail
                ],
            )
        )
        
        
        # --- SECCIÓN 5: LOGOS (FUNCIÓN REFACTORIZADA) ---
        def logos_container_responsive(titulo, lista, color_fondo=ft.Colors.TRANSPARENT):
            # Esta función ahora devuelve un container con un ResponsiveRow dentro
            return ft.Container(
                padding=20,
                bgcolor=color_fondo,
                content=ft.Column([
                    ft.Text(
                        value=titulo,
                        size=27,
                        color=ft.Colors.BLACK,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        italic=True
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            # Cada logo es ahora un control dentro de ResponsiveRow
                            ft.Container(
                                content=ft.Image(
                                    src=img[0],
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                on_click=lambda e, url=img[1]: self.page.launch_url(url) if self.page else None,
                                bgcolor=ft.Colors.TRANSPARENT,
                                border_radius=10,
                                padding=5,
                                # --- La magia del responsive ---
                                # En pantallas pequeñas (xs, sm) ocupa 6 de 12 columnas (2 por fila)
                                # En medianas (md) ocupa 4 de 12 columnas (3 por fila)
                                # En grandes (lg) ocupa 3 de 12 columnas (4 por fila)
                                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
                            )
                            for img in lista
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ])
            )

        patrocinadores = logos_container_responsive("Patrocinadores", imagenes_patrocinadores, ft.Colors.YELLOW_100)
        colaboradores = logos_container_responsive("Colaboradores", imagenes_colaboradores, ft.Colors.GREEN_100)
        organizadores = logos_container_responsive("Organizadores", imagenes_organizadores, ft.Colors.BLUE_GREY_300)

        # --- ESTRUCTURA PRINCIPAL CON RESPONSIVEROW ---
        # Reemplazamos la Column principal por un ResponsiveRow.
        # Cada elemento es ahora un Container con una propiedad `col` que define su ancho.
        self.content = ft.ResponsiveRow(
            spacing=20,
            run_spacing=0,
            controls=[
                # --- Cabecera de 3 imágenes ---
                # En escritorio (md): 3-6-3 columnas. En móvil (xs, sm): 12 columnas (apilado)
                ft.Container(portada1, col={"md": 3, "xs": 12, "sm": 12}),
                ft.Container(portada2, col={"md": 6, "xs": 12, "sm": 12}, alignment=ft.alignment.center, padding=10 ),
                ft.Container(portada3, col={"md": 3, "xs": 12, "sm": 12}),
                
                ft.Container(height=20),  # Espacio entre secciones
                ft.Container(btn_inscripcion, col=12, alignment=ft.alignment.center),
                
                # --- Contador ---
                ft.Container(countdown_container, col=12, expand= True, alignment=ft.alignment.center),
                
                ft.Container(height=20),  # Espacio entre secciones
                # --- Fecha y Lugar ---
                andarine_block,
                trail_block,
                # --- Logos ---
                # Cada sección de logos ya es responsive por sí misma y ocupa todo el ancho
                ft.Container(patrocinadores, col=12),
                ft.Container(colaboradores, col=12),
                ft.Container(organizadores, col=12),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START
        )


        
        
        
if __name__ == "__main__":
    print("A donde vas so animal... no se ejecuta este archivo")
    print("Ve a main.py y ejecuta desde ahí")