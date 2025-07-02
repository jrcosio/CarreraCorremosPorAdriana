import flet as ft
from dorsal_solidario.dorsalsolidario_screen import DorsalSolidarioScreen
from home.home_screen import HomeScreen
from inscripciones.inscripciones_screen import InscripcionScreen
from galeria.galeria_screen import GaleriaScreen
from recorrido.recorrido_screen import RecorridoScreen
from barra_navegacion.barra_navegacion import NavBar
from contacto.contacto_screen import ContactoScreen
from inscritos.inscritos_screen import InscritosScreen
from configurar_web import trail, andarines

# NUEVO: Importar el manejador de rutas TPV
from utils.tpv_routes import manejar_rutas_tpv

class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        page.title = "Trail Peñasagra - Corremos por Adriana"
        # Metaetiquetas usando page.meta (diccionario)
        page.meta = {
            "description": "Toda la información del Trail Peñasagra: inscripciones, recorridos, clasificaciones y galería de fotos.",
            "og:type": "website",
            "og:title": "Trail Peñasagra – Corremos por Adriana",
            "og:description": "Únete al Trail Peñasagra y apoya la causa de Adriana. Distancias de 30 km y 12 km andarines.",
            "og:image": "https://trailpenasagra.com/assets/images/logomenu.png", # Asegúrate que esta ruta sea accesible
            "og:url": "https://trailpenasagra.com/",
            "twitter:card": "summary_large_image",
            # Puedes añadir más metaetiquetas aquí si es necesario
            "keywords": "trail, peñasagra, carrera, montaña, adriana, cosio, cosío, nansa, cantabria, soplao",
        }
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        
        # Mapeo de botones a pantallas
        self.screens = {
            "btn_home": HomeScreen(on_click=None),
            "btn_inscripcion": InscripcionScreen(),
            "btn_inscritos": InscritosScreen(),
            "btn_galeria": GaleriaScreen(),
            "btn_trail": RecorridoScreen(recorrido_data=trail),
            "btn_andarines": RecorridoScreen(recorrido_data=andarines),
            "btn_contacto": ContactoScreen(),
            "btn_clasificacion": HomeScreen(),
            "btn_dorsal_solidario": DorsalSolidarioScreen(),
        }
        
        # Contenedor para mostrar la pantalla activa
        self.body_container = ft.Container(
            content=self.screens["btn_home"],
            expand=True,
            bgcolor="#173b4f",
        )
        
        # Barra de navegación
        self.nav_bar = NavBar(self.on_button_clicked)
        
        # Barra de footer
        self.footer = ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Container(ft.Text("© 2024 Trail Peñasagra - Corremos por Adriana", size=14, color=ft.Colors.WHITE),
                                col = {"xs": 12,"md": 3},
                                alignment=ft.alignment.center),
                    
                    ft.Container(ft.Text("Escuela Hackers Cosío (Pablo, Jose, Diego, Marina, Koldo)",size=14, color=ft.Colors.RED_400),
                                col = {"xs": 12,"md": 5},
                                alignment=ft.alignment.center),
    
                    ft.Container(ft.TextButton("Aviso Legal y de Protección de Datos",
                                               style=ft.ButtonStyle(
                                                   color=ft.Colors.WHITE),
                                                on_click=lambda e: self.page.open(self.ventana_avisolegal() if self.page else None),),
                                col = {"xs": 12,"md": 3}),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLUE_GREY_900,
            alignment= ft.alignment.center,
        )
        
        # Estructura principal de la página
        self.page.add(
            ft.Column(
                [
                    self.nav_bar,
                    ft.Column(
                        [self.body_container],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    ),
                    self.footer
                ],
                spacing=0,
                expand=True
            )
        )

        # NUEVO: Configurar el manejador de rutas (incluyendo TPV)
        self.page.on_route_change = self.route_change
        
        # Configuración inicial del responsive
        self.page.on_resize = self.on_page_resize
        self.on_page_resize(None)
    
    # NUEVO: Manejador de rutas que incluye las rutas del TPV
    def route_change(self, route):
        """Maneja los cambios de ruta, incluyendo las rutas del TPV"""
        print(f"🔄 Ruta solicitada: {route.route}")
        
        # PASO 1: Verificar si es una ruta del TPV
        if manejar_rutas_tpv(self.page, route.route):
            print("✅ Ruta del TPV procesada")
            return
        
        # NUEVO: Verificar si es una ruta de formulario de pago
        if route.route.startswith('/formulario_pago/'):
            numero_pedido = route.route.split('/')[-1]
            self._mostrar_formulario_pago(numero_pedido)
            return
        
        print(f"ℹ️ Ruta normal: {route.route}")
    
    def _mostrar_formulario_pago(self, numero_pedido: str):
        """Muestra el formulario de pago TPV como página web"""
        from utils.PagoTPVSantander import PagoTPVSantander
        
        if hasattr(PagoTPVSantander, '_formularios_temp'):
            html_content = PagoTPVSantander._formularios_temp.get(numero_pedido)
            if html_content:
                print(f"📄 Sirviendo formulario para pedido: {numero_pedido}")
                
                # Limpiar la página y mostrar mensaje
                self.page.clean()
                self.page.add(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🔒 Formulario de Pago Generado", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("El formulario se ha generado correctamente.", size=16),
                            ft.Text(f"Número de pedido: {numero_pedido}", size=14),
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                "📋 Ver formulario en nueva pestaña",
                                on_click=lambda e: self._mostrar_html_raw(html_content),
                                bgcolor=ft.colors.BLUE,
                                color=ft.colors.WHITE
                            ),
                            ft.ElevatedButton(
                                "🏠 Volver al inicio",
                                on_click=lambda e: self.on_button_clicked(type('obj', (object,), {'control': type('ctrl', (object,), {'data': 'btn_home'})()})()),
                                bgcolor=ft.colors.GREEN,
                                color=ft.colors.WHITE
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                        expand=True
                    )
                )
                self.page.update()
                
                # También intentar abrir automáticamente
                try:
                    self._mostrar_html_raw(html_content)
                except:
                    pass
                
                return
        
        print("❌ Formulario no encontrado")

def _mostrar_html_raw(self, html_content):
    """Muestra el HTML raw usando data URL"""
    import urllib.parse
    data_url = f"data:text/html;charset=utf-8,{urllib.parse.quote(html_content)}"
    try:
        self.page.launch_url(data_url)
        print("✅ Data URL abierta")
    except Exception as e:
        print(f"❌ Error con data URL: {e}")
        
    def ventana_avisolegal(self):
        
        from avisolegal import avisolegal
        
        if self.page is None:
            print("Error: page is not defined")
            return None
            
        dialogo = ft.AlertDialog( 
            title=ft.Text("Aviso Legal y Política de Protección de Datos"),
            modal=False,
            bgcolor=ft.Colors.BLUE_GREY_100,
            content=ft.Column(
                controls=[
                    ft.Text(
                        avisolegal,
                        size=14,
                        color=ft.Colors.BLACK,
                    )
                ],
                scroll=ft.ScrollMode.AUTO, # Permite el scroll si el contenido es largo
                tight=True, # Ajusta el tamaño del contenido al texto

            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.close(dialogo),
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(size=20),
                                    color=ft.Colors.BLACK)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )    
        return dialogo

    
    def on_button_clicked(self, e):
        """Se ejecuta al hacer clic en una opción de navegación."""
        button_id = e.control.data
        if button_id in self.screens:
            self.body_container.content = self.screens[button_id]
            # Reaplicamos la lógica responsive para mantener la consistencia del UI
            self.on_page_resize(None)

    def on_page_resize(self, e):
        """
        Función central que gestiona la apariencia de la app según el tamaño.
        """
        breakpoint_mobile = 768
        width = self.page.width or 1024 # Usamos un valor por defecto si es None
        is_mobile = width < breakpoint_mobile

        # 1. Ordena a la NavBar que actualice la visibilidad de sus vistas
        self.nav_bar.update_visibility(is_mobile)

        # 2. Ajusta los paddings
        if is_mobile:
            self.nav_bar.padding = ft.padding.symmetric(horizontal=20, vertical=10)
            self.body_container.padding = ft.padding.symmetric(horizontal=20)
        else:
            self.nav_bar.padding = ft.padding.symmetric(horizontal=60, vertical=10)
            self.body_container.padding = ft.padding.symmetric(horizontal=60)
        
        # 3. Actualiza la página para aplicar todos los cambios
        self.page.update()

def main(page: ft.Page):
    # Envolvemos el contenido principal en una columna con scroll
    # para que la NavBar se quede fija arriba y el contenido sea el que se desplace.
    page.scroll = ft.ScrollMode.HIDDEN
    app = MainApp(page)

if __name__ == "__main__":
    ft.app(target=main, port=80, view=ft.WEB_BROWSER, host="0.0.0.0", assets_dir="assets")