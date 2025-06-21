import flet as ft

class DorsalSolidarioScreen(ft.Container):
    def __init__(self, on_click=None):
        super().__init__()
        self.on_click = on_click
        self.cantidad_field = ft.TextField(
            label="Cantidad (€)",
            value="5",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE),
            color=ft.Colors.WHITE,
            cursor_color=ft.Colors.WHITE,
        )
        
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
                    expand=True,
                    padding=5,
                    ),
                    ft.Container(
                    content=ft.Image(
                        src="imagenes_dorsalsolidario/img_dorsal2.png",
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    expand=True,
                    padding=5,
                    ),
                    ft.Container(
                    content=ft.Image(
                        src="imagenes_dorsalsolidario/img_dorsal3.png",
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    expand=True,
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
                content=ft.Text(
                "Si no puedes venir al trail Peñasagra y quieres colaborar, puedes hacerlo con el 'dorsal solidario'",
                text_align=ft.TextAlign.CENTER,
                size=24,
                color="#ffcb2e",
                ),
                padding=ft.padding.symmetric(horizontal=20),
                width=None,
            ),
            
            self.cantidad_field,
            
            ft.Container(
                content=ft.ElevatedButton(
                text="PAGAR",
                bgcolor="#ffcb2e",
                color=ft.Colors.BLACK,
                width=200,
                height=50,
                on_click=self.on_solicitar_dorsal,
                ),
                alignment=ft.alignment.center,
            ),
            
            ft.Container(
                content=ft.Text(
                "Sino dessea usar la pasarela de pago puede hacer transferecia:\nNúmero de cuenta: ES38 0049 5335 5521 1601 8049\nConcepto: Dorsal Solidario\nAsociacion Sierra de Peñasagra",
                text_align=ft.TextAlign.CENTER,
                size=18,
                color=ft.Colors.WHITE,
                ),
                padding=ft.padding.symmetric(horizontal=20),
                width=None,
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
        print("Dorsal Solidario solicitado con cantidad:", self.cantidad_field.value)
    
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