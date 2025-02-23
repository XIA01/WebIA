# main.py

from gui.main_view import main_view
import flet as ft
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process

if __name__ == "__main__":
    # Lanza la aplicación Flet en modo escritorio.
    # Para pruebas en navegador, puedes usar view=ft.WEB_BROWSER
    # ft.app(target=main_view, view=ft.FLET_APP)
    ft.app(target=main_view, view=ft.WEB_BROWSER)