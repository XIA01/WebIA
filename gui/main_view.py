import flet as ft
from gui.components.buttons.exit_button import create_exit_button  # Función que crea el botón de salida
from gui.components.panels.info_panel import build_info_panel
from gui.components.panels.canvas_panel import build_canvas_panel
from gui.components.panels.prompt_panel import build_prompt_panel
from gui.components.panels.agent_panel import build_agent_panel
from gui.components.verifiers.python_verifier import verify_python

def main_view(page: ft.Page):
    """
    Vista principal que organiza:
      - Un encabezado superior con título, descripción y créditos (enlaces).
      - Cuatro paneles (Información, Canvas/GPU, Prompt y Agentes) en dos filas.
      - Una fila de botones para verificar cada panel.
      - Un botón de salida al final.
    """
    # Configuración inicial de la página
    page.title = "Proyecto de Agentes"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    
    # ---------------------------
    # Encabezado Superior
    # ---------------------------
    header_title = ft.Text("Proyecto Agentes creadores de Webs", size=32, weight="bold")
    header_description = ft.Text("Esta aplicación open source gestiona agentes de IA.", size=18)
    # Se crean botones de texto para que sean enlaces clicables a TikTok y GitHub
    credits_buttons = ft.Row(
        controls=[
            ft.Text("Créditos: Desarrollado por XIA01 - "),
            ft.TextButton("TikTok", url="https://www.tiktok.com/@b166er14"),
            ft.Text(" - "),
            ft.TextButton("GitHub", url="https://github.com/XIA01")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5
    )
    
    header_container = ft.Container(
        content=ft.Column(
            controls=[
                header_title,
                header_description,
                credits_buttons,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=20,
        alignment=ft.alignment.center
    )
    
    # ---------------------------
    # Paneles (Inicialmente deshabilitados)
    # ---------------------------
    info_panel_container = build_info_panel(verified=False)
    canvas_panel_container = build_canvas_panel(verified=False)
    prompt_panel_container = build_prompt_panel(verified=False)
    agent_panel_container = build_agent_panel(verified=False)
    
    # ---------------------------
    # Funciones de Verificación para cada panel
    # ---------------------------
    def verify_info(e):
        is_py, version = verify_python()
        if is_py:
            new_panel = build_info_panel(verified=True, version=version)
            info_panel_container.content = new_panel.content
            info_panel_container.opacity = new_panel.opacity
        page.update()
    
    def verify_canvas(e):
        new_panel = build_canvas_panel(verified=True)
        canvas_panel_container.content = new_panel.content
        canvas_panel_container.opacity = new_panel.opacity
        page.update()
    
    def verify_prompt(e):
        new_panel = build_prompt_panel(verified=True, prompt="Ejemplo de prompt")
        prompt_panel_container.content = new_panel.content
        prompt_panel_container.opacity = new_panel.opacity
        page.update()
    
    def verify_agents(e):
        new_panel = build_agent_panel(verified=True)
        agent_panel_container.content = new_panel.content
        agent_panel_container.opacity = new_panel.opacity
        page.update()
    
    # ---------------------------
    # Botones de Verificación para cada panel
    # ---------------------------
    verify_info_button = ft.ElevatedButton("Verificar Info", on_click=verify_info)
    verify_canvas_button = ft.ElevatedButton("Verificar GPU", on_click=verify_canvas)
    verify_prompt_button = ft.ElevatedButton("Verificar Prompt", on_click=verify_prompt)
    verify_agents_button = ft.ElevatedButton("Verificar Agentes", on_click=verify_agents)
    
    buttons_row = ft.Row(
        controls=[
            verify_info_button,
            verify_canvas_button,
            verify_prompt_button,
            verify_agents_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )
    
    # ---------------------------
    # Panel de Salida
    # ---------------------------
    exit_row = ft.Row(
        controls=[create_exit_button(page)],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    # ---------------------------
    # Organización General de la Vista
    # ---------------------------
    # Los paneles se organizan en dos filas: la primera con el Panel 1 y 2, y la segunda con el Panel 3 y 4.
    row_top = ft.Row(
        controls=[info_panel_container, canvas_panel_container],
        expand=True,
        spacing=10
    )
    row_bottom = ft.Row(
        controls=[prompt_panel_container, agent_panel_container],
        expand=True,
        spacing=10
    )
    
    main_layout = ft.Column(
        controls=[header_container, row_top, row_bottom, buttons_row, exit_row],
        expand=True,
        spacing=20
    )
    
    page.add(main_layout)

if __name__ == "__main__":
    # Arranca la aplicación en modo navegador para facilitar pruebas multiplataforma.
    ft.app(target=main_view, view=ft.WEB_BROWSER)
