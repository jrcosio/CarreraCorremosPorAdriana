from datetime import datetime
import os
from dotenv import load_dotenv
import flet as ft
from utils.TrailDataBase import TrailDataBase, Inscrito
import logging

from utils.gmail import Gmail

log = logging.getLogger(__name__)
# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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
        self.drop_ccaa = None
        self.txtf_poblacion = None
        self.txtf_dni_codigo = None
        self.drop_camiseta = None
        
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
        
        self.condiciones = None
        self.precio_carrera = ""
        self.error_condiciones = None
        
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
        
      
        self.txtf_poblacion = ft.TextField(
            label="Municipio",
            value="",
            **estilo_campo
        )
        
        self.condiciones = ft.Checkbox(
            label="Acepto el reglamento de la carrera",
            value=False,  
            label_style=ft.TextStyle(size=20),
        )
        
        self.error_condiciones = ft.Text(
            "",
            color=ft.Colors.RED,
            size=14,
            visible=False
        )
    def crear_campo_ccaa(self):
        """Crea el campo de selección de comunidad autónoma"""
        self.drop_ccaa = ft.Dropdown(
            label="Comunidad Autónoma",
            options=[
                ft.DropdownOption("Andalucía"),
                ft.DropdownOption("Aragón"),
                ft.DropdownOption("Asturias"),
                ft.DropdownOption("Islas Baleares"),
                ft.DropdownOption("Canarias"),
                ft.DropdownOption("Cantabria"),
                ft.DropdownOption("Castilla-La Mancha"),
                ft.DropdownOption("Castilla y León"),
                ft.DropdownOption("Cataluña"),
                ft.DropdownOption("Extremadura"),
                ft.DropdownOption("Galicia"),
                ft.DropdownOption("Madrid"),
                ft.DropdownOption("Murcia"),
                ft.DropdownOption("Navarra"),
                ft.DropdownOption("La Rioja"),
                ft.DropdownOption("País Vasco"),
            ],
            width=200,
            bgcolor="#FFFFFF",
            filled=True,
            fill_color=ft.Colors.WHITE,
        )
    
    def crear_campos_seleccion(self):
        """Crea los campos de selección (radio buttons y dropdowns)"""
        self.radio_sexo = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Text("Sexo:"),
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
                    ft.Text("Tipo de prueba:", size=24),
                    ft.Radio(value="trail", label="Trail [20€]", label_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)),
                    ft.Radio(value="andarines", label="Andarines [15€]", label_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_change=self.calcula_precio_carrera
        )

    def calcula_precio_carrera(self,e):
        """Calcula el precio de la carrera según la selección"""
        self.precio_carrera = "15" if self.radio_carrera.value == "trail" else "10"

    def crear_campos_fecha(self):
        """Crea los dropdowns para la fecha de nacimiento"""
        
        self.drop_dia = ft.Dropdown(
            label="Día",
            options=[ft.DropdownOption(str(day)) for day in range(1, 32)],
            width=105,
            bgcolor="#FFFFFF",
            filled=True,
            fill_color=ft.Colors.WHITE,
        )
        
        self.drop_mes = ft.Dropdown(
            label="Mes",
            options=[ft.DropdownOption(str(month)) for month in range(1, 13)],
            width=105,
            bgcolor="#FFFFFF",
            filled=True,
            fill_color=ft.Colors.WHITE,
        )
        
        self.drop_año = ft.Dropdown(
            label="Año",
            options=[ft.DropdownOption(str(year)) for year in range(1940, 2015)],
            width=105,
            bgcolor="#FFFFFF",
            filled=True,
            fill_color=ft.Colors.WHITE,
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
            filled=True,
            fill_color=ft.Colors.WHITE,
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
            label="Nombre de contacto en caso de emergencia",
            value="",
            bgcolor="#FFFFFF",
            expand=True,
        )
        
        self.txtf_numero_emergencia = ft.TextField(
            label="Número de teléfono de contacto en caso de emergencia",
            value="",
            bgcolor="#FFFFFF",
            expand=True,
            scroll_padding=ft.Padding(left=10, right=10, top=10, bottom=10)
        )
    
    def crear_drop_camiseta(self):
        self.drop_camiseta = ft.Dropdown(
            label="Talla de camiseta",
            options=[
                ft.DropdownOption("S"),
                ft.DropdownOption("M"),
                ft.DropdownOption("L"),
                ft.DropdownOption("XL"),
                ft.DropdownOption("XXL")                
            ],
            width=200,
            bgcolor="#FFFFFF",
            filled=True,
            fill_color=ft.Colors.WHITE,
        )

    def crear_botones(self):
        """Crea los botones del formulario"""
        self.btn_enviar = ft.ElevatedButton(
            text="Enviar formulario de inscripción",
            icon=ft.Icons.SEND,
            bgcolor=ft.Colors.GREEN_400,
            color=ft.Colors.WHITE,
            width=350,
            height=60,
            expand=True,
            on_click=self.al_enviar_formulario
        )

    def crear_fila_fecha(self):
        """Crea la fila con los dropdowns de fecha"""
        return ft.Row(
            controls=[ft.Text("Fecha de nacimiento:"), self.drop_dia, self.drop_mes, self.drop_año],
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
        self.crear_campo_ccaa()
        self.crear_drop_camiseta()
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
                ft.Row(
                    controls=[
                        self.drop_doc,
                        self.txtf_dni_codigo
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.txtf_direccion,
                ft.Row(
                    controls=[
                        self.drop_ccaa,
                        self.txtf_poblacion
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.radio_carrera,
                self.drop_camiseta,
                ft.Divider(),
                self.crear_titulo_emergencia(),
                self.txtf_nombre_emergencia,
                self.txtf_numero_emergencia,
                ft.Divider(),
                ft.Row(
                    controls=[
                        self.condiciones,
                        ft.TextButton(
                            "Leer REGLAMENTO DE LA CARRERA",
                            on_click=lambda e: self.page.open(self.ventana_condiciones() if self.page else None),
                            style=ft.ButtonStyle(
                                color=ft.Colors.BLUE_400,
                                text_style=ft.TextStyle(size=20)
                            )
                        )  
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.error_condiciones,
                            ft.Text(
                                "Asociación Sierra de Peñasagra - NIF: G21911052",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK
                            ),  
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.Alignment(0, 0)
                ),
                ft.Divider(),
                ft.Container(
                    content=self.btn_enviar,
                    alignment=ft.Alignment(0, 0),
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    def ventana_condiciones(self):
        
        from inscripciones.reglamento import reglamento
        
        if self.page is None:
            print("Error: page is not defined")
            return None
            
        dialogo = ft.AlertDialog( 
            title=ft.Text("REGLAMENTO TRAIL SIERRA DE PEÑASAGRA"),
            modal=False,
            bgcolor=ft.Colors.BLUE_GREY_100,
            content=ft.Column(
                controls=[
                    ft.Text(
                        reglamento,
                        size=20,
                        color=ft.Colors.BLACK,
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
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
            "nombre": self.txtf_nombre.value.lower().title(),
            "apellido": self.txtf_apellido.value.upper(),
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
            "ccaa": self.drop_ccaa.value,
            "poblacion": self.txtf_poblacion.value,
            "carrera": self.radio_carrera.value,
            "talla": self.drop_camiseta.value,
            "nombre_emergencia": self.txtf_nombre_emergencia.value,
            "numero_emergencia": self.txtf_numero_emergencia.value,
            "condiciones": self.condiciones.value,
            "precio_carrera": self.precio_carrera,
        }

    def validar_formulario(self):
        """Valida que todos los campos requeridos estén completos"""
        datos = self.obtener_datos_formulario()
     
        if not datos["nombre"] or datos["nombre"].strip() == "":
            self.txtf_nombre.error_text = "El campo Nombre es requerido"
            self.txtf_nombre.update()
            return False, "El campo 'nombre' es requerido"
        else:
            self.txtf_nombre.error_text = ""
            self.txtf_nombre.update()
        if not datos["apellido"] or datos["apellido"].strip() == "":
            self.txtf_apellido.error_text = "El campo Apellido es requerido"
            self.txtf_apellido.update()
            return False, "El campo 'apellido' es requerido"
        else:
            self.txtf_apellido.error_text = ""
            self.txtf_apellido.update()
        if not datos["telefono"] or datos["telefono"].strip() == "":
            self.txtf_tlfno.error_text = "El campo Teléfono es requerido"
            self.txtf_tlfno.update()
            return False, "El campo 'telefono' es requerido"
        else:
            self.txtf_tlfno.error_text = ""
            self.txtf_tlfno.update()
        if not datos["sexo"]:
            self.radio_sexo.error_text = "El campo Sexo es requerido"
            self.radio_sexo.update()
            return False, "El campo 'sexo' es requerido"
        else:
            self.radio_sexo.error_text = ""
            self.radio_sexo.update()
        if not datos["dia"] or not datos["mes"] or not datos["año"]:
            self.drop_dia.error_text = "El campo 'Día' es requerido"
            self.drop_mes.error_text = "El campo 'Mes' es requerido"
            self.drop_año.error_text = "El campo 'Año' es requerido"
            self.drop_dia.update()
            self.drop_mes.update()
            self.drop_año.update()
            return False, "La fecha de nacimiento es requerida"
        else:
            self.drop_dia.error_text = ""
            self.drop_mes.error_text = ""
            self.drop_año.error_text = ""
            self.drop_dia.update()
            self.drop_mes.update()
            self.drop_año.update()
        if not datos["email"] or datos["email"].strip() == "":
            self.txtf_email.error_text = "El campo Email es requerido"
            self.txtf_email.update()
            return False, "El campo 'email' es requerido"
        else:
            self.txtf_email.error_text = ""
            self.txtf_email.update()
        if not datos["repetir_email"] or datos["repetir_email"].strip() == "":
            self.txtf_rep_email.error_text = "El campo Repetir Email es requerido"
            self.txtf_rep_email.update()
            return False, "El campo 'repetir email' es requerido"
        else:
            self.txtf_rep_email.error_text = ""
            self.txtf_rep_email.update()
        if not datos["codigo_documento"] or datos["codigo_documento"].strip() == "":
            self.txtf_dni_codigo.error_text = "El campo Código de Documento es requerido"
            self.txtf_dni_codigo.update()
            return False, "El campo 'número documento' es requerido"
        else:
            self.txtf_dni_codigo.error_text = ""
            self.txtf_dni_codigo.update()
        if not datos["tipo_documento"]:
            self.drop_doc.error_text = "El campo Tipo de Documento es requerido"
            self.drop_doc.update()
            return False, "El campo 'tipo documento' es requerido"
        else:
            self.drop_doc.error_text = ""
            self.drop_doc.update()
        if not datos["direccion"] or datos["direccion"].strip() == "":
            self.txtf_direccion.error_text = "El campo Dirección es requerido"
            self.txtf_direccion.update()
            return False, "El campo 'direccion' es requerido"
        else:
            self.txtf_direccion.error_text = ""
            self.txtf_direccion.update()
        if not datos["ccaa"] or datos["ccaa"].strip() == "":
            self.drop_ccaa.error_text = "El campo Comunidad Autónoma es requerido"
            self.drop_ccaa.update()
            return False, "El campo 'ccaa' es requerido"
        else:
            self.drop_ccaa.error_text = ""
            self.drop_ccaa.update()
        if not datos["poblacion"] or datos["poblacion"].strip() == "":
            self.txtf_poblacion.error_text = "El campo Municipio es requerido"
            self.txtf_poblacion.update()
            return False, "El campo 'poblacion' es requerido"
        else:
            self.txtf_poblacion.error_text = ""
            self.txtf_poblacion.update()
        if not datos["carrera"] or datos["carrera"].strip() == "":
            self.radio_carrera.error_text = "El campo Carrera es requerido"
            self.radio_carrera.update()
            return False, "El campo 'carrera' es requerido"
        else:
            self.radio_carrera.error_text = ""
            self.radio_carrera.update()
        if not datos["nombre_emergencia"] or datos["nombre_emergencia"].strip() == "":
            self.txtf_nombre_emergencia.error_text = "El campo Nombre de Emergencia es requerido"
            self.txtf_nombre_emergencia.update()
            return False, "El campo 'nombre emergencia' es requerido"
        else:
            self.txtf_nombre_emergencia.error_text = ""
            self.txtf_nombre_emergencia.update()
            
        if not datos["numero_emergencia"] or datos["numero_emergencia"].strip() == "":
            self.txtf_numero_emergencia.error_text = "El campo Número de Emergencia es requerido"
            self.txtf_numero_emergencia.update()
            return False, "El campo 'numero emergencia' es requerido"
        else:
            self.txtf_numero_emergencia.error_text = ""
            self.txtf_numero_emergencia.update()
            
        if not datos["condiciones"]:
            # En lugar de usar error_text, mostrar el mensaje de error
            self.error_condiciones.value = "Debes aceptar el reglamento de la carrera"
            self.error_condiciones.visible = True
            self.error_condiciones.update()
            return False, "Debes aceptar el reglamento de la carrera"
        else:
            self.error_condiciones.visible = False
            self.error_condiciones.update()
        
        # Validar que los emails coincidan
        if datos["email"] != datos["repetir_email"]:
            self.txtf_email.error_text = "Los emails no coinciden"
            self.txtf_rep_email.error_text = "Los emails no coinciden"
            self.txtf_email.update()
            self.txtf_rep_email.update()
            return False, "Los emails no coinciden"
        
        return True, "Formulario válido"

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        """Limpia todos los campos del formulario"""
        self.txtf_nombre.value = ""
        self.txtf_apellido.value = ""
        self.txtf_tlfno.value = ""
        self.txtf_email.value = ""
        self.txtf_rep_email.value = ""
        self.txtf_direccion.value = ""
        self.drop_ccaa.value = None
        self.txtf_poblacion.value = ""
        self.radio_sexo.value = None
        self.radio_carrera.value = None
        self.drop_dia.value = None
        self.drop_mes.value = None
        self.drop_año.value = None
        self.drop_doc.value = None
        self.txtf_dni_codigo.value = ""
        self.txtf_nombre_emergencia.value = ""
        self.txtf_numero_emergencia.value = ""
        self.condiciones.value = False
        
        self.update()

    def dlg_modal(self, texto, color=ft.Colors.GREEN_200):
        # Use self.page instead of page
        if self.page is None:
            print("Error: page is not defined")
            return None
            
        dialogo = ft.AlertDialog( 
            modal=False,
            bgcolor=color,
            content=ft.Text(
                texto,
                size=20,
                color=ft.Colors.WHITE,
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.close(dialogo),
                                style=ft.ButtonStyle(color=ft.Colors.BLACK)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )    
        return dialogo
        
    def al_enviar_formulario(self, e):
        """Maneja el evento de envío del formulario"""
        es_valido, mensaje = self.validar_formulario()
        
        if es_valido:
            datos = self.obtener_datos_formulario()
            print("Formulario enviado:", datos)
            # Aquí puedes agregar la lógica para procesar los datos
            #------------------------------------------------------
            try:
                db = TrailDataBase()
            except Exception as ex:
                log.error(f"Error al conectar a la base de datos: {ex}")
                self.mostrar_mensaje("Error al conectar a la base de datos. Por favor, inténtalo de nuevo.", ft.Colors.RED_200)
                return
            
            if datos["carrera"] == "trail":
                dorsal = str((int(db.obtener_ultimo_dorsal(datetime.now().year, tipo_carrera="trail") or "000") + 1)).zfill(3)
            else:
                dorsal = str((int(db.obtener_ultimo_dorsal(datetime.now().year, tipo_carrera="andarines") or "299") + 1)).zfill(3)
            
            inscrito = Inscrito(
                dorsal=dorsal,  # El dorsal se asignará automáticamente
                nombre=datos["nombre"],
                apellidos=datos["apellido"],
                sexo=datos["sexo"],
                fecha_nacimiento=datetime(int(datos["año"]), int(datos["mes"]), int(datos["dia"])),
                telefono=datos["telefono"],
                email=datos["email"],
                tipo_documento=datos["tipo_documento"],
                numero_documento=datos["codigo_documento"],
                direccion=datos["direccion"],
                ccaa=datos["ccaa"],
                municipio=datos["poblacion"],
                tipo_carrera=datos["carrera"],
                talla=datos["talla"],
                contacto_emergencia=datos["nombre_emergencia"],
                telefono_emergencia=datos["numero_emergencia"],
                edicion=datetime.now().year,
            )
            
            try:
                load_dotenv()

                # Obtener credenciales de Gmail desde .env
                gmail_user = os.getenv('GMAIL_USER')
                gmail_pass = os.getenv('GMAIL_PASSWORD')

                # Crear instancia de Gmail y enviar contacto
                gmail = Gmail(gmail_user, gmail_pass)
                
                gmail.enviar_email_inscrito(inscrito)
                
                db.insertar(inscrito)
                
                self.mostrar_mensaje("El Formulario ha sido enviado correctamente")
                self.limpiar_formulario()
            
            except Exception as ex:
                log.error(f"Error al insertar el inscrito: {ex}")
                self.mostrar_mensaje("Error al realizar la inscripción. Por favor, inténtalo de nuevo.", ft.Colors.RED_200)
            
  

    def mostrar_mensaje(self, texto, color=ft.Colors.GREEN_200):
        """Muestra un mensaje al usuario"""
        self.page.open(self.dlg_modal(texto, color) if self.page else None)

if __name__ == "__main__":
    print("Esta clase no se puede ejecutar de forma independiente.")