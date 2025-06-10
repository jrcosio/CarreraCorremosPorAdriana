import flet as ft
import os
from dotenv import load_dotenv
import logging

load_dotenv()
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Inscritos(ft.Container):
    def __init__(self):
               
        
        
        
        super().__init__(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                [
                    ft.Text(
                        "Inscriptos",
                        size=40,
                        color=ft.Colors.GREEN_900,
                        font_family="Britanic Bold",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),  
        )