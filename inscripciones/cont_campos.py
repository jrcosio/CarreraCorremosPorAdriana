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
                            top_left=15, top_right=15, bottom_left=15, bottom_right=15
                        ),
                    ),
                    ft.Row(
                        controls = [
                            ft.Text("Nombre:"),
                            txtf_nombre
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls = [
                            ft.Text("Apellidos:"),
                            txtf_apellido
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row( 
                        controls = [
                            ft.Text("Sexo:"),
                            radio_sexo,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls = [
                            ft.Text("Fecha de nacimiento:"),
                            drop_edad,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls = [
                            ft.Text("Teléfono:"),
                            txtf_tlfno,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls = [
                            ft.Text("Email:"),
                            txtf_email
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls = [
                            ft.Text("Repite Email:"),
                            txtf_rep_email
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls = [
                            ft.Text("Dirección:"),
                            txtf_direccion
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(controls = [
                            ft.Text("Carrera:"),
                            radio_carrera,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Row(
                        controls = [
                            drop_doc,
                            ft.Container(width = 10),
                            txtf_dni_codigo
                        ],
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.CENTER
                    ),
                    txt_emergencia,
                    txtf_nombre_emergencia,
                    txtf_numero_emergencia,
                    btn_enviar
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                alignment = ft.MainAxisAlignment.CENTER,
            ),
            alignment = ft.Alignment(0, 0),
            height= 900,
            width = 800,
            bgcolor = ft.Colors.BLACK26,
            border_radius=ft.BorderRadius(
                top_left=15, top_right=15, bottom_left=15, bottom_right=15
            )
        )

