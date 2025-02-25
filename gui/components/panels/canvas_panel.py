import flet as ft
from ai_motors.agents.tools.canvas_tools import client, ram, gpu, vram,saludador
def build_canvas_panel(verified: bool = False) -> ft.Container:
    if verified:
        global client
        response = client.run(
            agent=saludador,
            messages=[{"role": "user", "content": "Hola"}],
            context_variables={"name": "ente biológico inteligente", "ram": ram, "gpu": gpu, "vram": vram}
        )

        # Extraer el mensaje del agente
        agent_message = response.messages[-1]["content"]

        # Crear un widget para mostrar la respuesta del agente
        display_text = ft.Text(agent_message, size=12)
        status_list = ft.ListView(
            expand=True,
            spacing=5,
            controls=[display_text]
        )
        icon_color = ft.colors.GREEN
        opacity_value = 1.0
    else:
        display_text = ft.Text("Prueba GPU: No verificado", size=16)
        # Definir status_list también en el caso no verificado
        status_list = ft.ListView(
            expand=True,
            spacing=5,
            controls=[display_text]
        )
        icon_color = ft.colors.RED
        opacity_value = 0.5

    status_icon = ft.Icon(name=ft.icons.CHECK_CIRCLE, color=icon_color, size=30)

    # Lista base de controles (texto e icono)
    content_controls = [
        ft.Text("Prueba GPU", size=20, weight="bold"),
        status_list,
        status_icon,
        ft.Divider(),
    ]

    return ft.Container(
        content=ft.Column(
            controls=content_controls,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=ft.colors.LIGHT_GREEN,
        padding=10,
        alignment=ft.alignment.center,
        opacity=opacity_value
    )
