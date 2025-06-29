import time
import flet as ft
import logging
import threading
from utils.PagoTPVSantander import PagoTPVSantander


log = logging.getLogger(__name__)
# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DorsalSolidarioScreen(ft.Container):
    def __init__(self, on_click=None):
        super().__init__()
        self.pago_instance = None  # Inicializamos la instancia de PagoTPVSantander
        
        self.on_click = on_click
        
        self.cantidad_field = ft.TextField(
            label="Cantidad (€)",
            value="5",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE),
            color=ft.Colors.WHITE,
            cursor_color=ft.Colors.WHITE,
            text_style=ft.TextStyle(color=ft.Colors.WHITE,size=30),
        )
        self.Comentario_field = ft.TextField(
            label="Comentario (opcional)",
            value="Dorsal Solidario",
            width=600,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE),
            color=ft.Colors.WHITE,
            cursor_color=ft.Colors.WHITE,
            text_style=ft.TextStyle(color=ft.Colors.WHITE,size=30),
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
            self.Comentario_field,
            
            ft.Container(
                content=ft.ElevatedButton(
                text="PAGAR",
                bgcolor="#ffcb2e",
                color=ft.Colors.BLACK,
                width=200,
                height=50,
                on_click=self.on_click_solicitar_dorsal,
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

    def on_click_solicitar_dorsal(self, e):
        """ Metodo que se llama al hacer clic en el botón de pagar """
        print("Dorsal Solidario solicitado con cantidad:", self.cantidad_field.value)
        print("Comentario:", self.Comentario_field.value)
        try:
            
            if self.pago_instance is None:
                log.info(f"Dorsal Solidario Iniciando pasarela de pago: {self.cantidad_field.value} y comentario: {self.Comentario_field.value}")
                self.pago_instance = PagoTPVSantander(
                    concepto=self.Comentario_field.value,
                    importe=float(self.cantidad_field.value),
                    entorno_test=False,
                    callback_exito=lambda datos: self.page.open(self.ventana_pago_exitoso(mensaje=datos["mensaje"], numero_pedido=datos["numero_pedido"]) if self.page else None),
                    callback_error=lambda mensaje: self.page.open(self.ventana_error_pago(mensaje) if self.page else None)
                )
            else:
                log.info("Reutilizando instancia de PagoTPVSantander")
                self.pago_instance.pago_completado = False  # Reiniciamos el estado de pago
                timestamp = str(int(time.time()))
                self.pago_instance.numero_pedido = timestamp[-8:]  # Generamos un nuevo número de pedido basado en el timestamp
                log.info(f"Número de pedido generado: {self.pago_instance.numero_pedido}")
            
            def iniciar_pago_thread():
                self.pago_instance.start(debug=True, mantener_vivo=False)
                
            threading.Thread(target=iniciar_pago_thread, daemon=True).start()
            
        except Exception as ex:
            log.error(f"Error al solicitar el dorsal solidario: {ex}")
    
    def ventana_pago_exitoso(self, mensaje: str = None, numero_pedido: str = None):
        """ Ventana de pago exitoso """
        
        if self.page is None:
            print("Error: page is not defined")
            return None
        
        def cerrar_y_limpiar(e):
             # Limpiar los campos
            self.cantidad_field.value = "5"
            self.Comentario_field.value = "Dorsal Solidario"  
            self.pago_instance = None # Limpiar la instancia de PagoTPVSantander
    
            self.page.update()  # Actualizar la página para reflejar los cambios
            self.page.close(dialogo) # Cerrar el diálogo
         
        dialogo = ft.AlertDialog( 
            title=ft.Text("Pago realizado con éxito"),
            modal=False,
            bgcolor=ft.Colors.GREEN_100,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "El pago se ha realizado correctamente.",
                        size=14,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        f"Mensaje: {mensaje} \nNúmero de pedido: {numero_pedido}",
                        size=14,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "Gracias por tu colaboración. ¡Nos vemos en la carrera!",
                        size=14,
                        color=ft.Colors.BLACK,
                    )
                ],
                scroll=ft.ScrollMode.AUTO, # Permite el scroll si el contenido es largo
                tight=True, # Ajusta el tamaño del contenido al texto
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=cerrar_y_limpiar,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(size=20),
                                    color=ft.Colors.BLACK)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )    
        return dialogo
    
    def ventana_error_pago(self, mensaje: str = None):
        """ Ventana de error al realizar el pago """
        
        if self.page is None:
            print("Error: page is not defined")
            return None
        
        def cerrar_y_limpiar(e):
             # Limpiar los campos
            self.cantidad_field.value = "5"
            self.Comentario_field.value = "Dorsal Solidario"  
            self.pago_instance = None # Limpiar la instancia de PagoTPVSantander
    
            self.page.update()  # Actualizar la página para reflejar los cambios
            self.page.close(dialogo) # Cerrar el diálogo
            
            
        dialogo = ft.AlertDialog( 
            title=ft.Text("Error al realizar el pago"),
            modal=False,
            bgcolor=ft.Colors.RED_100,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Ha ocurrido un error al procesar el pago. Por favor, inténtelo de nuevo más tarde.",
                        size=14,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        f"Error al realizar el pago: {mensaje}",
                        size=14,
                        color=ft.Colors.BLACK,
                    )
                ],
                scroll=ft.ScrollMode.AUTO, # Permite el scroll si el contenido es largo
                tight=True, # Ajusta el tamaño del contenido al texto
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=cerrar_y_limpiar,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(size=20),
                                    color=ft.Colors.BLACK)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )  
        
        return dialogo
           
        
        
    
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