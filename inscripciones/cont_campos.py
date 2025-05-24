import flet as ft

txtf_nombre = ft.TextField(
    label="Nombre",
    value="",
    bgcolor="#976211",
    expand=True,
    color=ft.Colors.WHITE,
    scroll_padding=ft.Padding(left = 10, right = 10, top = 10, bottom = 10)
)
txtf_apellido = ft.TextField(
    label="Apellidos",
    value="",
    bgcolor="#976211",
    expand=True,
    scroll_padding=ft.Padding(left = 10, right = 10, top = 10, bottom = 10)
)
txtf_tlfno = ft.TextField(
    label="Teléfono",
    value="",
    bgcolor="#976211",
    expand=True,
    content_padding=ft.Padding(top=10, bottom=10, left=10, right=10),
)
txtf_email = ft.TextField(
    label="Email",
    value="",
    bgcolor="#976211",
    expand=True,
    scroll_padding=ft.Padding(left = 10, right = 10, top = 10, bottom = 10)
)
txtf_rep_email = ft.TextField(
    label="Repetir Email",
    value="",
    bgcolor="#976211",
    expand=True,
    scroll_padding=ft.Padding(left = 10, right = 10, top = 10, bottom = 10)
)
txtf_direccion = ft.TextField(
    label="Dirección",
    value="",
    bgcolor="#976211",
    expand=True,
    scroll_padding=ft.Padding(left = 10, right = 10, top = 10, bottom = 10)
)
txtf_dni_codigo = ft.TextField(
    label="Código",
    value="",
    bgcolor="#976211",
    expand=True,
    scroll_padding=ft.Padding(left = 10, right = 10, top = 10, bottom = 10)
)
txtf_nombre_emergencia = ft.TextField(
    label="Nombre de emergencia",
    value="",
    bgcolor="#976211",
    expand=True,
)
txtf_numero_emergencia = ft.TextField(
    label="Número de emergencia",
    value="",
    bgcolor="#976211",
    expand=True,
    scroll_padding=ft.Padding(left = 10, right = 10, top = 10, bottom = 10)
)
btn_enviar = ft.ElevatedButton(
    text="Enviar",
    icon=ft.Icons.SEND,
    bgcolor=ft.Colors.GREEN_400,
    color=ft.Colors.WHITE,
    width=150,
    expand=True
)

radio_sexo = ft.RadioGroup(
    content=ft.Row(
        controls = [
            ft.Radio(value="M", label="M"),
            ft.Radio(value="F", label="F")
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        vertical_alignment = ft.CrossAxisAlignment.CENTER,
    )
)
radio_carrera = ft.RadioGroup(
    content=ft.Row(
        controls = [
            ft.Radio(value="trail", label="Trail"),
            ft.Radio(value="andarines", label="Andarines"),
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        vertical_alignment = ft.CrossAxisAlignment.CENTER,
    )
)
drop_edad = ft.Row(
    controls = [
        ft.Dropdown(
            label="Día",
            options=[ft.DropdownOption(str(day)) for day in range(1, 32)],
            width=105,
            bgcolor="#976211"
        ),
        ft.Dropdown(
            label="Mes",
            options=[ft.DropdownOption(str(month)) for month in range(1, 13)],
            width=105,
            bgcolor="#976211"
        ),
        ft.Dropdown(
            label="Año",
            options=[ft.DropdownOption(str(year)) for year in range(1950, 2024)],
            width=105,
            bgcolor="#976211"
        )
    ],
    alignment=ft.MainAxisAlignment.CENTER,
)
drop_doc = ft.Dropdown(label = "Documentación", options=[ft.DropdownOption("DNI"), ft.DropdownOption("NIE"), ft.DropdownOption("Pasaporte")], width = 200)
txt_emergencia = ft.Text("Datos de emergencia", weight=ft.FontWeight.BOLD)

class Campos(ft.Container):
    def __init__(self):
        self.alignment = ft.MainAxisAlignment.CENTER
        super().__init__(
            content = ft.Column(
                controls = [
                    ft.Container(
                        content = ft.Text("Formulario de inscrpición", 
                                        weight = ft.FontWeight.BOLD,
                                        color = ft.Colors.WHITE,
                                        size = 16,
                                        ),
                        alignment = ft.Alignment(0, 0),
                        bgcolor = "#1F2937",
                        height = 50,
                        border_radius=ft.BorderRadius(
                            top_left=15, top_right=15, bottom_left=0, bottom_right=0
                        ),
                    ),
                    ft.Container(
                        content = self.formulario(),
                        bgcolor = "#B63333",
                        padding = ft.Padding(10, 10, 10, 10),
                        expand=True,
                    ),
                    
                ],
                spacing=0,
                width = 800,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        
    def formulario(self):
        return ft.Column(
            controls=[
                txtf_nombre,
                txtf_apellido,
                radio_sexo,
                drop_edad,
                txtf_tlfno,
                txtf_email,
                txtf_rep_email,
                drop_doc,
                txtf_dni_codigo,
                txtf_direccion,
                radio_carrera,
                txt_emergencia,
                txtf_nombre_emergencia,
                txtf_numero_emergencia,
                btn_enviar
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

