import flet as ft


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
        
        andarines = ft.Container(
            content=ft.Stack(
                [
                    ft.Image(
                        src="imagenes_home/andarines.jpg", 
                        fit=ft.ImageFit.CONTAIN,
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
                alignment=ft.alignment.center,
                expand=True,  # Movido expand=True al contenedor
        ),
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
                        color=ft.Colors.BLACK,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        italic=True,
            ),
                alignment=ft.alignment.center,
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
            content=ft.Text("Patrocinadores", size=40, color=ft.Colors.BLACK, 
            font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True),
            expand=True,
            alignment=ft.alignment.top_center,  # Cambiado a una alineación estándar
            bgcolor=ft.Colors.YELLOW, 
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