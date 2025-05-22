import flet as ft
from datetime import datetime, timedelta
import threading
import time

class CountdownTimer(ft.Container):
    def __init__(
        self,
        target_date=None,
        on_finish=None,
        days_style=None,
        hours_style=None,
        minutes_style=None,
        seconds_style=None,
        label_style=None,
        box_style=None,
        **kwargs
    ):
        # Inicializar el container padre
        super().__init__(**kwargs)
        
        # Valores por defecto
        self.target_date = target_date or (datetime.now() + timedelta(hours=4, minutes=26, seconds=38))
        self.on_finish = on_finish
        
        # Estilos por defecto
        self._days_style = days_style or ft.TextStyle(size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
        self._hours_style = hours_style or ft.TextStyle(size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
        self._minutes_style = minutes_style or ft.TextStyle(size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
        self._seconds_style = seconds_style or ft.TextStyle(size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
        self._label_style = label_style or ft.TextStyle(size=16, color=ft.Colors.BLUE)
        self._box_style = box_style or {
            "bgcolor": ft.Colors.WHITE,
            "border_radius": 10,
            "padding": 20,
            "width": 120,
            "height": 150,  # Aumentado para dar más espacio
            "alignment": ft.alignment.center
        }
        
        # Crear componentes para los números y etiquetas
        self.days_text = ft.Text("0", style=self._days_style)
        self.hours_text = ft.Text("0", style=self._hours_style)
        self.minutes_text = ft.Text("0", style=self._minutes_style)
        self.seconds_text = ft.Text("0", style=self._seconds_style)
        
        # Etiquetas con textos explícitos
        self.days_label = ft.Text("Días", style=self._label_style)
        self.hours_label = ft.Text("Horas", style=self._label_style)
        self.minutes_label = ft.Text("Minutos", style=self._label_style)
        self.seconds_label = ft.Text("Segundos", style=self._label_style)
        
        # Crear los contenedores para cada unidad de tiempo con espaciado entre número y etiqueta
        self.days_box = ft.Container(
            content=ft.Column(
                [self.days_text, self.days_label],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10  # Espacio entre el número y la etiqueta
            ),
            **self._box_style
        )
        
        self.hours_box = ft.Container(
            content=ft.Column(
                [self.hours_text, self.hours_label],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            **self._box_style
        )
        
        self.minutes_box = ft.Container(
            content=ft.Column(
                [self.minutes_text, self.minutes_label],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            **self._box_style
        )
        
        self.seconds_box = ft.Container(
            content=ft.Column(
                [self.seconds_text, self.seconds_label],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            **self._box_style
        )
        
        # Crear el contenido principal con una fila de los contadores
        self.content = ft.Row(
            [self.days_box, self.hours_box, self.minutes_box, self.seconds_box],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        
        # Iniciar el temporizador
        self.is_running = False
        self.timer_thread = None
        self.stop_event = threading.Event()
        
    def did_mount(self):
        """Se llama cuando el componente es montado en la UI"""
        self.start()
        
    def will_unmount(self):
        """Se llama cuando el componente es desmontado de la UI"""
        self.stop()
        
    def _timer_loop(self):
        """Función que ejecuta el hilo del temporizador"""
        while not self.stop_event.is_set():
            # Actualizar los valores de tiempo
            self._update_time_values()
            # Solicitar actualización en el hilo principal
            if hasattr(self, 'page') and self.page:
                self.page.update()
            time.sleep(1)  # Esperar un segundo
    
    def start(self):
        """Inicia el contador"""
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self._update_time_values()  # Actualizar inmediatamente
            # Iniciar hilo para actualizaciones periódicas
            self.timer_thread = threading.Thread(target=self._timer_loop)
            self.timer_thread.daemon = True  # Hilo en segundo plano
            self.timer_thread.start()
    
    def stop(self):
        """Detiene el contador"""
        if self.is_running:
            self.is_running = False
            self.stop_event.set()  # Señal para detener el hilo
            if self.timer_thread:
                self.timer_thread.join(timeout=1)  # Esperar a que termine el hilo
                self.timer_thread = None
    
    def set_target_date(self, new_date):
        """Actualiza la fecha objetivo"""
        self.target_date = new_date
        self._update_time_values()
        if self.page:
            self.page.update()
    
    def _update_time_values(self):
        """Actualiza los valores de tiempo sin actualizar la UI"""
        now = datetime.now()
        
        # Calcular la diferencia de tiempo
        if now >= self.target_date:
            # Si ya pasó la fecha, mostrar 0 en todos los campos
            time_diff = timedelta(0)
            if self.on_finish and self.is_running:
                self.stop()
                # El callback se ejecutará después, no aquí
                if hasattr(self, 'page') and self.page:
                    # Ejecutamos el callback sólo cuando sea seguro
                    self.on_finish(self)
        else:
            time_diff = self.target_date - now
        
        # Extraer los componentes de tiempo
        days = time_diff.days
        seconds = time_diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        # Actualizar los textos
        self.days_text.value = str(days)
        self.hours_text.value = str(hours)
        self.minutes_text.value = str(minutes)
        self.seconds_text.value = str(seconds)
    
    def update_countdown(self):
        """Método público para actualizar manualmente el contador"""
        self._update_time_values()
        self.update()


# Ejemplo de uso del componente:
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
        #bgcolor=ft.Colors.LIGHT_BLUE_50,
        padding=20,
    )
    # titulo = ft.Text(
    #     "Contador Regresivo para COSIO",
    #     style=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
    #     text_align=ft.TextAlign.CENTER,
    # )
    page.add(titulo, countdown_container)

if __name__ == "__main__":
    ft.app(target=main)