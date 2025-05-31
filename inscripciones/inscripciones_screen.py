# import flet as ft
# from .cont_campos import Campos
# from barra_navegacion.barra_navegacion import NavBar

# class InscripcionScreen(ft.Container):
#     def __init__(self):
#         super().__init__(
#             content=Campos()
#         )

# if __name__ == "__main__":
#     print("Esta clase no se puede ejecutar de forma independiente.")

import flet as ft

class InscripcionScreen(ft.Container):
    def __init__(self):
        # Inicializar todos los campos del formulario
        self.inicializar_campos()
        
        super().__init__(
            alignment=ft.Alignment(0, 0),
            content=self.crear_contenedor_principal()
        )

    def inicializar_campos(self):
        """Inicializa todos los campos del formulario"""
        # Campos de texto personales
        self.txtf_nombre = None
        self.txtf_apellido = None
        self.txtf_tlfno = None
        self.txtf_email = None
        self.txtf_rep_email = None
        self.txtf_direccion = None
        self.txtf_provincia = None
        self.txtf_poblacion = None
        self.txtf_dni_codigo = None
        
        # Campos de emergencia
        self.txtf_nombre_emergencia = None
        self.txtf_numero_emergencia = None
        
        # Campos de selección
        self.radio_sexo = None
        self.radio_carrera = None
        self.drop_dia = None
        self.drop_mes = None
        self.drop_año = None
        self.drop_doc = None
        
        # Botón
        self.btn_enviar = None

    def crear_campos_personales(self):
        """Crea los campos de información personal básica"""
        estilo_campo = {
            "bgcolor": "#FFFFFF",
            "expand": True,
            #"color": ft.Colors.WHITE,
            "scroll_padding": ft.Padding(left=10, right=10, top=10, bottom=10)
        }
        
        self.txtf_nombre = ft.TextField(
            label="Nombre",
            value="",
            **estilo_campo
        )
        
        self.txtf_apellido = ft.TextField(
            label="Apellidos",
            value="",
            **estilo_campo
        )
        
        self.txtf_tlfno = ft.TextField(
            label="Teléfono",
            value="",
            **estilo_campo
        )
        
        self.txtf_email = ft.TextField(
            label="Email",
            value="",
            **estilo_campo
        )
        
        self.txtf_rep_email = ft.TextField(
            label="Repetir Email",
            value="",
            **estilo_campo
        )
        
        self.txtf_direccion = ft.TextField(
            label="Dirección",
            value="",
            **estilo_campo
        )
        
        self.txtf_provincia = ft.TextField(
            label="Provincia",
            value="",
            **estilo_campo
        )
        self.txtf_poblacion = ft.TextField(
            label="Municipio",
            value="",
            **estilo_campo
        )

    def crear_campos_seleccion(self):
        """Crea los campos de selección (radio buttons y dropdowns)"""
        self.radio_sexo = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="M", label="Masculino"),
                    ft.Radio(value="F", label="Femenino")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        
        self.radio_carrera = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="trail", label="Trail"),
                    ft.Radio(value="andarines", label="Andarines"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def crear_campos_fecha(self):
        """Crea los dropdowns para la fecha de nacimiento"""
        
        self.drop_dia = ft.Dropdown(
            label="Día",
            options=[ft.DropdownOption(str(day)) for day in range(1, 32)],
            width=105,
            bgcolor="#FFFFFF"
        )
        
        self.drop_mes = ft.Dropdown(
            label="Mes",
            options=[ft.DropdownOption(str(month)) for month in range(1, 13)],
            width=105,
            bgcolor="#FFFFFF"
        )
        
        self.drop_año = ft.Dropdown(
            label="Año",
            options=[ft.DropdownOption(str(year)) for year in range(1940, 2015)],
            width=105,
            bgcolor="#FFFFFF"
        )

    def crear_campos_documento(self):
        """Crea los campos relacionados con la documentación"""
        self.drop_doc = ft.Dropdown(
            label="Tipo de documento",
            options=[
                ft.DropdownOption("DNI"),
                ft.DropdownOption("NIE"),
                ft.DropdownOption("Pasaporte")
            ],
            width=200,
            bgcolor="#FFFFFF",
        )
        
        self.txtf_dni_codigo = ft.TextField(
            label="Número de documento",
            value="",
            bgcolor="#FFFFFF",
            expand=True,
            scroll_padding=ft.Padding(left=10, right=10, top=10, bottom=10)
        )

    def crear_campos_emergencia(self):
        """Crea los campos de contacto de emergencia"""
        self.txtf_nombre_emergencia = ft.TextField(
            label="Nombre de emergencia",
            value="",
            bgcolor="#FFFFFF",
            expand=True,
        )
        
        self.txtf_numero_emergencia = ft.TextField(
            label="Número de emergencia",
            value="",
            bgcolor="#FFFFFF",
            expand=True,
            scroll_padding=ft.Padding(left=10, right=10, top=10, bottom=10)
        )

    def crear_botones(self):
        """Crea los botones del formulario"""
        self.btn_enviar = ft.ElevatedButton(
            text="Enviar",
            icon=ft.Icons.SEND,
            bgcolor=ft.Colors.GREEN_400,
            color=ft.Colors.WHITE,
            width=150,
            height=60,
            expand=True,
            on_click=self.al_enviar_formulario
        )

    def crear_fila_fecha(self):
        """Crea la fila con los dropdowns de fecha"""
        return ft.Row(
            controls=[self.drop_dia, self.drop_mes, self.drop_año],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def crear_titulo_emergencia(self):
        """Crea el título de la sección de emergencia"""
        return ft.Text(
            "Datos de emergencia",
            weight=ft.FontWeight.BOLD
        )

    def crear_formulario(self):
        """Crea el formulario completo con todos los campos"""
        # Crear todos los campos
        self.crear_campos_personales()
        self.crear_campos_seleccion()
        self.crear_campos_fecha()
        self.crear_campos_documento()
        self.crear_campos_emergencia()
        self.crear_botones()
        
        return ft.Column(
            controls=[
                self.txtf_nombre,
                self.txtf_apellido,
                self.radio_sexo,
                self.crear_fila_fecha(),
                self.txtf_tlfno,
                self.txtf_email,
                self.txtf_rep_email,
                self.drop_doc,
                self.txtf_dni_codigo,
                self.txtf_direccion,
                self.txtf_provincia,
                self.txtf_poblacion,
                self.radio_carrera,
                self.crear_titulo_emergencia(),
                self.txtf_nombre_emergencia,
                self.txtf_numero_emergencia,
                self.btn_enviar
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

    def crear_encabezado(self):
        """Crea el encabezado del formulario"""
        return ft.Container(
            content=ft.Text(
                "Formulario de inscripción",
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
                size=24,
            ),
            alignment=ft.Alignment(0, 0),
            bgcolor="#7BACF0",
            height=50,
            border_radius=ft.BorderRadius(
                top_left=15, top_right=15, bottom_left=0, bottom_right=0
            ),
        )

    def crear_contenedor_formulario(self):
        """Crea el contenedor principal del formulario"""
        return ft.Container(
            content=self.crear_formulario(),
            bgcolor="#DBF3D6",
            padding=ft.Padding(10, 10, 10, 10),
            expand=True,
        )

    def crear_contenedor_principal(self):
        """Crea el contenedor principal de toda la pantalla"""
        return ft.Column(
            controls=[
                self.crear_encabezado(),
                self.crear_contenedor_formulario(),
            ],
            spacing=0,
            width=800,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def obtener_datos_formulario(self):
        """Obtiene todos los datos del formulario en un diccionario"""
        return {
            "nombre": self.txtf_nombre.value,
            "apellido": self.txtf_apellido.value,
            "sexo": self.radio_sexo.value,
            "dia": self.drop_dia.value,
            "mes": self.drop_mes.value,
            "año": self.drop_año.value,
            "telefono": self.txtf_tlfno.value,
            "email": self.txtf_email.value,
            "repetir_email": self.txtf_rep_email.value,
            "tipo_documento": self.drop_doc.value,
            "codigo_documento": self.txtf_dni_codigo.value,
            "direccion": self.txtf_direccion.value,
            "carrera": self.radio_carrera.value,
            "nombre_emergencia": self.txtf_nombre_emergencia.value,
            "numero_emergencia": self.txtf_numero_emergencia.value,
        }

    def validar_formulario(self):
        """Valida que todos los campos requeridos estén completos"""
        datos = self.obtener_datos_formulario()
        
        campos_requeridos = [
            "nombre", "apellido", "sexo", "telefono", 
            "email", "repetir_email", "codigo_documento"
        ]
        
        for campo in campos_requeridos:
            if not datos[campo] or datos[campo].strip() == "":
                return False, f"El campo {campo} es requerido"
        
        # Validar que los emails coincidan
        if datos["email"] != datos["repetir_email"]:
            return False, "Los emails no coinciden"
        
        return True, "Formulario válido"

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        if self.txtf_nombre:
            self.txtf_nombre.value = ""
            self.txtf_apellido.value = ""
            self.txtf_tlfno.value = ""
            self.txtf_email.value = ""
            self.txtf_rep_email.value = ""
            self.txtf_direccion.value = ""
            self.txtf_dni_codigo.value = ""
            self.txtf_nombre_emergencia.value = ""
            self.txtf_numero_emergencia.value = ""
            
            self.radio_sexo.value = None
            self.radio_carrera.value = None
            self.drop_dia.value = None
            self.drop_mes.value = None
            self.drop_año.value = None
            self.drop_doc.value = None

    def al_enviar_formulario(self, e):
        """Maneja el evento de envío del formulario"""
        es_valido, mensaje = self.validar_formulario()
        
        if es_valido:
            datos = self.obtener_datos_formulario()
            print("Formulario enviado:", datos)
            # Aquí puedes agregar la lógica para procesar los datos
            self.mostrar_mensaje("Formulario enviado correctamente", ft.Colors.GREEN)
        else:
            self.mostrar_mensaje(f"Error: {mensaje}", ft.Colors.RED)

    def mostrar_mensaje(self, texto, color):
        """Muestra un mensaje al usuario"""
        # Aquí puedes implementar la lógica para mostrar mensajes
        # Por ejemplo, usando un SnackBar o Dialog
        print(f"Mensaje: {texto}")

if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")