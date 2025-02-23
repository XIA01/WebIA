import flet as ft

def build_info_panel(verified: bool = False, version: str = "No verificado") -> ft.Container:
    """
    Construye un panel de Información.
    
    Parámetros:
      verified: Si True, se muestra el panel habilitado (opacidad 1.0, ícono verde).
                Si False, se muestra deshabilitado (opacidad 0.5, ícono rojo).
      version:  Versión de Python a mostrar en caso de verificación exitosa.
    """
    if verified:
        display_version = version
        icon_color = ft.colors.GREEN
        opacity_value = 1.0
    else:
        display_version = "No verificado"
        icon_color = ft.colors.RED
        opacity_value = 0.5

    info_text = ft.Text(f"Versión de Python: {display_version}", size=16)
    status_icon = ft.Icon(name=ft.icons.CHECK_CIRCLE, color=icon_color, size=30)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Información del Sistema", size=20, weight="bold"),
                info_text,
                status_icon,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=ft.colors.LIGHT_BLUE,
        padding=10,
        alignment=ft.alignment.center,
        opacity=opacity_value
    )
