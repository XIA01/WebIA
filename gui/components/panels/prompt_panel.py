import flet as ft

def build_prompt_panel(verified: bool = False, prompt: str = "") -> ft.Container:
    """
    Construye un panel de Prompt.
    
    Parámetros:
      verified: Si True, el panel se muestra habilitado (opacidad 1.0, ícono verde).
                Si False, se muestra deshabilitado (opacidad 0.5, ícono rojo).
      prompt:   Valor inicial del campo de texto (por ejemplo, un prompt de ejemplo).
    """
    text_field = ft.TextField(label="Escribe tu prompt", width=300, value=prompt)
    icon_color = ft.colors.GREEN if verified else ft.colors.RED
    status_icon = ft.Icon(name=ft.icons.CHECK_CIRCLE, color=icon_color, size=30)
    opacity_value = 1.0 if verified else 0.5

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Página y Prompt", size=20, weight="bold"),
                text_field,
                status_icon,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=ft.colors.YELLOW,
        padding=10,
        alignment=ft.alignment.center,
        opacity=opacity_value
    )
