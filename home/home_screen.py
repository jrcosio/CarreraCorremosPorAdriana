import flet as ft


class HomeScreen(ft.Container):
    def __init__(self):
        super().__init__(
            alignment=ft.alignment.center,
            expand=True
        )

        #------------------------------------------------------------
        adriana = ft.Container(
            content=ft.Text("Escrito sobre la enfermadad de Adri", size=40, color=ft.Colors.BLACK, 
            font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True),
            expand=True,
            alignment=ft.alignment.center,
            height=100,  
        )   
        
        andarines = ft.Container(
            content=ft.Stack(
            [
                ft.Image(src="imagenes_home/andarines.jpg", fit=ft.ImageFit.CONTAIN, width=800, height=800),
                    ft.Container(
                    content=ft.Text(
                        "Andarines",
                        size=50,
                        color=ft.Colors.WHITE,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        italic=True,
                   
                ),
                alignment=ft.alignment.center,  # Posiciona el texto en la parte superior
                padding=20,
                bgcolor=ft.Colors.BLACK45,
                border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20)
            ),
                ft.Container(
                    content=ft.Text(
                        "12 de Julio de 2025",
                        size=40,
                        color=ft.Colors.WHITE,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        italic=True,
                        
                    ),
                    alignment=ft.alignment.bottom_center,  # Posiciona el texto en la parte inferior
                    padding=10,  # Espaciado opcional
                    bgcolor=ft.Colors.BLACK54,
                    border_radius=ft.border_radius.only(top_left=20, top_right=20)
                ),
            ]
        ),
                width=800,
                expand=True,
                alignment=ft.alignment.center,
                padding=10,
                margin=0,
                bgcolor=ft.Colors.WHITE,
            )

        runers = ft.Container(
            content=ft.Stack(
            [    
                ft.Image(src="imagenes_home/trail.jpg", fit=ft.ImageFit.CONTAIN, width=800, 
                            height=800),
                    ft.Container(
                        content=ft.Text(
                            "Cosío - Rionansa",
                            size=40,
                            color=ft.Colors.WHITE,
                            font_family="Britanic Bold",
                            weight=ft.FontWeight.BOLD,
                            italic=True
                        ),
                    alignment=ft.alignment.bottom_center,  # Posiciona el texto en la parte inferior
                    padding=10,  # Espaciado opcional
                    bgcolor=ft.Colors.BLACK54,
                    border_radius=ft.border_radius.only(top_left=20, top_right=20)
                ),
            ]
        ),
                width=800,
                expand=True,
                alignment=ft.alignment.center,
                padding=10,
                margin=0,
                bgcolor=ft.Colors.WHITE,
        )

        portada= ft.Row(
            [andarines,
            runers,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        patrocinadores= ft.Container(
            ft.Text("Patrocinadores", size=40, color=ft.Colors.BLACK, 
                    font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True),
            expand=True,
            alignment=ft.Alignment(0, -1),
            bgcolor=ft.Colors.YELLOW, 
        )
        
        colaboradores= ft.Container(ft.Text("Colaboradores", size=40, color=ft.Colors.BLACK, 
                    font_family="Britanic Bold", weight=ft.FontWeight.BOLD, italic=True),
            expand=True,
            alignment=ft.Alignment(0, -1),
            bgcolor=ft.Colors.GREEN,  
        )    
        
        self.content = ft.Column(
            [
                adriana,
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