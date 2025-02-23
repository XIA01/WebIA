import flet as ft

def build_agent_panel(verified: bool = False) -> ft.Container:
    """
    Construye un panel de Agentes.
    
    Si verified es False, se muestra deshabilitado (opacidad baja, mensaje e ícono rojo).
    Si es True, se muestra habilitado (opacidad normal, mensaje e ícono verde).
    """
    if verified:
        display_text = ft.Text("Equipo de agentes activado", size=16)
        icon_color = ft.colors.GREEN
        opacity_value = 1.0
    else:
        display_text = ft.Text("Agentes desactivados", size=16)
        icon_color = ft.colors.RED
        opacity_value = 0.5

    status_icon = ft.Icon(name=ft.icons.CHECK_CIRCLE, color=icon_color, size=30)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Agentes", size=20, weight="bold"),
                display_text,
                status_icon,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=ft.colors.RED,
        padding=10,
        alignment=ft.alignment.center,
        opacity=opacity_value
    )
