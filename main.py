# main.py
import sys
import flet as ft
from gui.main_view import main_view



def run_gui():
    """
    Lanza la aplicación Flet en modo navegador (o escritorio).
    """
    ft.app(target=main_view, view=ft.WEB_BROWSER)

if __name__ == "__main__":
    
        run_gui()
