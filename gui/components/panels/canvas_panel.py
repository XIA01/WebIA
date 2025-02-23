import flet as ft

def build_canvas_panel(verified: bool = False) -> ft.Container:
    """
    Construye un panel de Canvas/GPU.
    
    Si verified es False, se muestra con opacidad baja y un mensaje/ícono rojo.
    Si es True, se muestra habilitado con opacidad normal, indicando que la prueba fue exitosa.
    """
    if verified:
        display_text = ft.Text("Prueba GPU: Correcta. Sonrisa dibujada.", size=16)
        icon_color = ft.colors.GREEN
        opacity_value = 1.0
    else:
        display_text = ft.Text("Prueba GPU: No verificado", size=16)
        icon_color = ft.colors.RED
        opacity_value = 0.5

    status_icon = ft.Icon(name=ft.icons.CHECK_CIRCLE, color=icon_color, size=30)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Prueba GPU", size=20, weight="bold"),
                display_text,
                status_icon,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=ft.colors.LIGHT_GREEN,
        padding=10,
        alignment=ft.alignment.center,
        opacity=opacity_value
    )
