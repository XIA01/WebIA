# gui/main_view.py
import flet as ft
from gui.components.buttons.exit_button import create_exit_button
from gui.components.panels.info_panel import build_info_panel
from gui.components.panels.canvas_panel import build_canvas_panel
from gui.components.panels.prompt_panel import build_prompt_panel
from gui.components.panels.agent_panel import build_agent_panel
from gui.components.verifiers.python_verifier import verify_python

# Variable global para almacenar la referencia al TextField del prompt.
prompt_text_field = None

def main_view(page: ft.Page):
    global prompt_text_field  # para poder asignarla desde verify_canvas
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

    # Inicializamos los paneles con un placeholder
    info_panel_container = ft.Container(
        content=ft.Text("Info pendiente de verificación", size=16),
        expand=True,
        bgcolor=ft.colors.LIGHT_BLUE,
        padding=10,
        alignment=ft.alignment.center,
        opacity=0.5
    )
    canvas_panel_container = ft.Container(
        content=ft.Text("GPU pendiente de verificación", size=16),
        expand=True,
        bgcolor=ft.colors.LIGHT_GREEN,
        padding=10,
        alignment=ft.alignment.center,
        opacity=0.5
    )
    # El panel de prompt se inicializa con un mensaje de placeholder.
    prompt_panel_container = ft.Container(
        content=ft.Text("Prompt pendiente de verificación", size=16),
        expand=True,
        bgcolor=ft.colors.LIGHT_GREEN_ACCENT,
        padding=10,
        alignment=ft.alignment.center,
        opacity=0.5
    )
    agent_panel_container = ft.Container(
        content=ft.Text("Agentes pendientes de verificación", size=16),
        expand=True,
        bgcolor=ft.colors.PINK_ACCENT_700,
        padding=10,
        alignment=ft.alignment.center,
        opacity=0.5
    )

    # Texto de estado para mostrar mensajes de verificación
    status_text = ft.Text("", size=20, weight="bold", color="blue600")

    # Funciones de verificación
    def verify_info(e):
        verify_info_button.disabled = True
        status_text.value = "Verificando Info..."
        page.update()

        is_py, version = verify_python()
        new_panel = build_info_panel(verified=is_py, version=version)
        info_panel_container.content = new_panel.content
        info_panel_container.opacity = new_panel.opacity

        if not is_py:
            status_text.value = "Error al verificar Info. ¡Intenta de nuevo!"
            verify_info_button.disabled = False
        else:
            status_text.value = "¡Info Verificada con éxito!"
            # Habilitamos el siguiente botón
            verify_canvas_button.disabled = False

        page.update()

    def verify_canvas(e):
        verify_canvas_button.disabled = True
        status_text.value = "Verificando GPU..."
        page.update()

        new_panel = build_canvas_panel(verified=True)
        new_panel.expand = True
        constrained_container = ft.Container(
            content=new_panel,
            width=canvas_panel_container.width or 1000,
            height=canvas_panel_container.height or 300,
        )
        canvas_panel_container.content = constrained_container
        canvas_panel_container.opacity = new_panel.opacity

        status_text.value = "¡GPU Verificada!"
        # Al verificar GPU, construimos el panel de prompt y guardamos la referencia al TextField.
        prompt_panel, prompt_field = build_prompt_panel(verified=True, prompt="")
        prompt_panel_container.content = prompt_panel.content
        prompt_panel_container.opacity = prompt_panel.opacity
        # Guardamos el TextField globalmente para luego obtener su valor.
        global prompt_text_field
        prompt_text_field = prompt_field

        # Habilitamos el botón para verificar el prompt
        verify_prompt_button.disabled = False
        page.update()

    def verify_prompt(e):
        verify_prompt_button.disabled = True
        status_text.value = "Enviando prompt al agente..."
        page.update()

        # Obtenemos el prompt ingresado en el TextField
        prompt_value = prompt_text_field.value if prompt_text_field else ""
        
        # Llamamos al pipeline pasándole el prompt y obtenemos la respuesta del agente.
        from ai_motors.agents.product_manager.product_pipeline import run_product_pipeline
        agent_response = run_product_pipeline(prompt_value)
        
        status_text.value = "¡Prompt enviado y respuesta recibida!"
        page.update()

        # Habilitamos el siguiente botón para los agentes (si deseas usarlo para mostrar la respuesta)
        verify_agents_button.disabled = False


    def verify_agents(e):
        verify_agents_button.disabled = True
        status_text.value = "Verificando Agentes..."
        page.update()

        # En este ejemplo, podrías actualizar el panel de agentes con la respuesta obtenida.
        new_panel = build_agent_panel(verified=True)
        agent_panel_container.content = new_panel.content
        agent_panel_container.opacity = new_panel.opacity

        status_text.value = "¡Agentes Verificados!"
        page.update()

    # Inicialmente, solo el primer botón está habilitado.
    verify_info_button = ft.ElevatedButton("Verificar Info", on_click=verify_info)
    verify_canvas_button = ft.ElevatedButton("Verificar GPU", on_click=verify_canvas, disabled=True)
    verify_prompt_button = ft.ElevatedButton("Verificar Prompt", on_click=verify_prompt, disabled=True)
    verify_agents_button = ft.ElevatedButton("Verificar Agentes", on_click=verify_agents, disabled=True)

    buttons_row = ft.Row(
        controls=[verify_info_button, verify_canvas_button, verify_prompt_button, verify_agents_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    exit_row = ft.Row(
        controls=[create_exit_button(page), status_text],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30
    )

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
    new_panel = panel_builder(verified=True, *args)
    panel_container.content = new_panel.content
    panel_container.opacity = new_panel.opacity
