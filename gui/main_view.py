import flet as ft
from gui.components.buttons.exit_button import create_exit_button
from gui.components.panels.info_panel import build_info_panel
from gui.components.panels.canvas_panel import build_canvas_panel
from gui.components.panels.prompt_panel import build_prompt_panel
from gui.components.panels.agent_panel import build_agent_panel
from gui.components.verifiers.python_verifier import verify_python
from ai_motors.agents.test_agents.agente_saludo import obtener_saludo

def main_view(page: ft.Page):
    page.title = "Proyecto de Agentes"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    header_title = ft.Text("Proyecto Agentes creadores de Webs", size=32, weight="bold")
    header_description = ft.Text("Esta aplicación open source gestiona agentes de IA.", size=18)

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
            controls=[header_title, header_description, credits_buttons],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=20,
        alignment=ft.alignment.center
    )

    # Paneles
    info_panel_container = build_info_panel()
    canvas_panel_container = build_canvas_panel(verified=False)
    prompt_panel_container = build_prompt_panel(verified=False)
    agent_panel_container = build_agent_panel(verified=False)

    # Texto de estado para mostrar mensajes de verificación
    status_text = ft.Text("", size=20, weight="bold", color="blue600")

    def verify_info(e):
        # 1) Deshabilitar botón y mostrar texto
        verify_info_button.disabled = True
        status_text.value = "Verificando..."
        page.update()

        # 2) Ejecutar verificación real
        is_py, version = verify_python()
        saludo = obtener_saludo()

        # 3) Actualizar el panel con el resultado
        new_panel = build_info_panel(verified=is_py, version=version, saludo=saludo)
        info_panel_container.content = new_panel.content
        info_panel_container.opacity = new_panel.opacity

        # 4) Si hubo error, volvemos a habilitar el botón; si fue correcto, lo dejamos deshabilitado
        if not is_py:
            status_text.value = "Error al verificar. ¡Intenta de nuevo!"
            verify_info_button.disabled = False
        else:
            status_text.value = "¡Verificado con éxito!"

        page.update()

    def verify_canvas(e):
        verify_canvas_button.disabled = True
        status_text.value = "Verificando GPU..."
        page.update()

        # Lógica de verificación de GPU (ejemplo simulado)
        new_panel = build_canvas_panel(verified=True)
        canvas_panel_container.content = new_panel.content
        canvas_panel_container.opacity = new_panel.opacity

        # Suponiendo que es exitoso, lo dejamos deshabilitado; si fallara, re-habilitaríamos
        status_text.value = "GPU Verificada con éxito"
        page.update()

    def verify_prompt(e):
        verify_prompt_button.disabled = True
        status_text.value = "Verificando Prompt..."
        page.update()

        # Lógica de verificación (aquí solo simulamos)
        new_panel = build_prompt_panel(verified=True, prompt_text="Ejemplo de prompt")
        prompt_panel_container.content = new_panel.content
        prompt_panel_container.opacity = new_panel.opacity

        status_text.value = "¡Prompt Verificado!"
        page.update()

    def verify_agents(e):
        verify_agents_button.disabled = True
        status_text.value = "Verificando Agentes..."
        page.update()

        # Lógica simulada de verificación de agentes
        new_panel = build_agent_panel(verified=True)
        agent_panel_container.content = new_panel.content
        agent_panel_container.opacity = new_panel.opacity

        status_text.value = "¡Agentes Verificados!"
        page.update()

    # Botones de verificación
    verify_info_button = ft.ElevatedButton("Verificar Info", on_click=verify_info)
    verify_canvas_button = ft.ElevatedButton("Verificar GPU", on_click=verify_canvas)
    verify_prompt_button = ft.ElevatedButton("Verificar Prompt", on_click=verify_prompt)
    verify_agents_button = ft.ElevatedButton("Verificar Agentes", on_click=verify_agents)

    buttons_row = ft.Row(
        controls=[verify_info_button, verify_canvas_button, verify_prompt_button, verify_agents_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    # Fila con botón Salir y texto de estado
    exit_row = ft.Row(
        controls=[create_exit_button(page), status_text],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30
    )

    # Layout principal
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


def update_panel(panel_container, panel_builder, *args):
    # Esta función puede usarse si quieres reutilizar la lógica de cambio en paneles.
    new_panel = panel_builder(verified=True, *args)
    panel_container.content = new_panel.content
    panel_container.opacity = new_panel.opacity
