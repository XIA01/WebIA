# main.py
import sys
import flet as ft
from gui.main_view import main_view
from ai_motors.config.crew import LatestAiDevelopmentCrew


def run_crew():
    """
    Ejecuta el crew de CrewAI pasando inputs (por ejemplo, 'topic').
    """
    from crewai.project import crew

    inputs = {"topic": "Saluda en español"}
    LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)

def run_gui():
    """
    Lanza la aplicación Flet en modo navegador (o escritorio).
    """
    ft.app(target=main_view, view=ft.WEB_BROWSER)

if __name__ == "__main__":
    # Si se pasa el argumento "crew", se ejecuta el crew, de lo contrario, se lanza la GUI.
    if len(sys.argv) > 1 and sys.argv[1].lower() == "crew":
        run_crew()
    else:
        run_gui()
