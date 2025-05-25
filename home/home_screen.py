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
            content=ft.Text("Escrito sobre la enfermadad de Adri", size=40, color=ft.Colors.BLACK, 
                font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True),
            alignment=ft.alignment.center,
            height=100,  
            bgcolor=ft.Colors.RED_100
        )   
        
        imagen1=ft.Image(src="imagenes_patrocinadores/descarga.jpg")
        imagen2=ft.Image(src="imagenes_patrocinadores/imagen1.jpg")
        imagen3=ft.Image(src="imagenes_patrocinadores/imagen2.jpg")
        imagen4=ft.Image(src="imagenes_patrocinadores/imagen3.jpg")
        
        def main(page: ft.Page):
            page.title = "Contador Regresivo"
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Fecha objetivo (ejemplo: 6 horas en el futuro)
    #target = datetime.now() + timedelta(hours=6)
        target = datetime(2025, 7, 12, 10, 00, 00)  # Fecha objetivo específica
    
        def on_countdown_finish(timer):
                page.snack_bar = ft.SnackBar(content=ft.Text("¡Cuenta regresiva completada!"))
                page.snack_bar.open = True
                page.update()
    
    # Crear un contenedor centrado para el contador
        countdown_container = ft.Container(
                content=CountdownTimer(
                target_date=target,
                on_finish=on_countdown_finish,
                padding=5,
                bgcolor=None,  # Transparente para que se vea el fondo del contenedor principal
        ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.WHITE,
            padding=20,
    )
        
            
        
        andarines = ft.Container(
            content=ft.Stack(
                [
                    ft.Image(
                        src="imagenes_home/andarines.jpg", 
                        fit=ft.ImageFit.CONTAIN,
                        expand=True,  # Añadido aquí
                    ),
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
                        padding=10,  # Añadido padding
                        expand=True,  # Movido expand=True al contenedor    
        ),
                    # ft.Container(
                    #     content=ft.Text(
                    #     "Andarines",
                    #         size=32,
                    #         color=ft.Colors.WHITE,
                    #         font_family="Britanic Bold",
                    #         weight=ft.FontWeight.BOLD,
                    #         italic=True,
                    # ),
                    #     alignment=ft.alignment.bottom_center,  # Posiciona el texto en la parte inferior
                    #     padding=10,  # Añadido padding
                    #     expand=True,  # Movido expand=True al contenedor    
                   
                    # ),
                ],
            ),
        expand=True,
        )   

        runers = ft.Container(
            content=ft.Stack(
                [
                    ft.Image(
                        src="imagenes_home/trail.jpg", 
                        fit=ft.ImageFit.CONTAIN,
                    ),
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
                padding=10,  # Añadido padding
                expand=True,  # Movido expand=True al contenedor
        ),
                ],
            ),
            expand=True,  # Movido expand=True al contenedor
        )
        cabecera = ft.Row(
            [fecha_carrera, lugar_carrera],  # Eliminada coma adicional
            alignment=ft.MainAxisAlignment.CENTER,
        )

        portada = ft.Row(
            [andarines, runers],  # Eliminada coma adicional
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        patrocinadores = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Patrocinadores", size=40, color=ft.Colors.BLACK, 
                    font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True),
                        
                    ft.Row([imagen1, imagen2, imagen3, imagen4]),  # Añadido para mostrar las imágenes
            # Añadido para que tenga una altura fija 
         
                ],
        ),
        )
        
        
        colaboradores = ft.Container(
            content=ft.Text("Colaboradores", size=40, color=ft.Colors.BLACK, 
                font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True),
            expand=True,
            alignment=ft.alignment.top_center,  # Cambiado a una alineación estándar
            bgcolor=ft.Colors.GREEN,  
        )    
        
        self.content = ft.Column(
            [
                adriana,
                countdown_container,
                cabecera,
                portada,
                patrocinadores,
                colaboradores,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            expand=True,
        )
    #------------------------------------------------------------
        
        
        
if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")