import flet as ft

class DorsalSolidarioScreen(ft.Container):
    def __init__(self, on_click=None):
        super().__init__()
        self.on_click = on_click
        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Image(
                                    src="imagenes_dorsalsolidario/img_dorsal1.png",
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                expand=True,  # Se expande para ocupar espacio disponible
                                padding=5,
                            ),
                            ft.Container(
                                content=ft.Image(
                                    src="imagenes_dorsalsolidario/img_dorsal2.png",
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                expand=True,  # Se expande para ocupar espacio disponible
                                padding=5,
                            ),
                            ft.Container(
                                content=ft.Image(
                                    src="imagenes_dorsalsolidario/img_dorsal3.png",
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                expand=True,  # Se expande para ocupar espacio disponible
                                padding=5,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        tight=True,
                    ),
                    padding=ft.padding.only(bottom=20),
                ),
                
                ft.Container(
                    content=ft.Text(
                        "Dorsal Solidario",
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.WHITE,
                    ),
                    bgcolor="#ffcb2e",
                    border_radius=ft.border_radius.all(50),
                    padding=ft.padding.all(10),
                    alignment=ft.alignment.center,
                    width=400,
                ),
                ft.Container(
                    content = ft.Column(
                        [
                            ft.Text(
                                "Desde",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Text(
                                "5€",
                                size=80,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                        spacing= 0,
                    ),
                    bgcolor="#ffcb2e",
                    border_radius=ft.border_radius.all(50),
                    padding=ft.padding.all(10),
                    alignment=ft.alignment.center,
                    width=150,
                ),
                
                ft.Container(
                    content=ft.Text(
                        "Si no puedes venir al trail Peñasagra y quieres colaborar, puedes hacerlo con el 'dorsal solidario'",
                        text_align=ft.TextAlign.CENTER,
                        size=24,
                        color="#ffcb2e",
                    ),
                    padding=ft.padding.symmetric(horizontal=20),
                    width=None,  # Se adapta al contenido
                ),
                
                ft.Container(
                    content=ft.Text(
                        "Número de cuenta: ES38 0049 5335 5521 1601 8049\nConcepto: Dorsal Solidario\nAsociacion Sierra de Peñasagra",
                        text_align=ft.TextAlign.CENTER,
                        size=24,
                        color=ft.Colors.WHITE,
                    ),
                    padding=ft.padding.symmetric(horizontal=20),
                    width=None,  # Se adapta al contenido
                ),
                
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        )
        # Configuración responsive
        self.expand = True
        self.width = None
        self.height = None
        self.bgcolor = "#173b4f"
        self.padding = ft.padding.all(10)
        self.alignment = ft.alignment.center

    def on_solicitar_dorsal(self, e):
        if self.on_click:
            self.on_click("btn_solicitar_dorsal")
    
if __name__ == "__main__":
 
    class MainApp:
        def __init__(self, page: ft.Page):
            self.page = page
            self.page.padding = ft.padding.all(0)
            self.page.title = "Dorsal Solidario"
            self.page.theme_mode = ft.ThemeMode.LIGHT
            
            
            self.page.add(
                DorsalSolidarioScreen()
            )
        
    def main(page: ft.Page):
        # Envolvemos el contenido principal en una columna con scroll
        # para que la NavBar se quede fija arriba y el contenido sea el que se desplace.
        page.scroll = ft.ScrollMode.HIDDEN
        app = MainApp(page)

   
    ft.app(target=main)