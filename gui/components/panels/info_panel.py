import flet as ft
from ai_motors.config.model_config import get_model


def build_info_panel(verified: bool = False, version: str = "No verificado", saludo: str = "No verificado") -> ft.Container:
    """
    Construye un panel de Información que muestra:
      - La versión de Python verificada manualmente.
      - El modelo configurado obtenido con get_model().
      - Un saludo obtenido de la ejecución del agente de saludo.

    Si todos los elementos están verificados correctamente, el panel se muestra
    habilitado (opacidad 1.0 e ícono verde). En caso contrario, se muestra con
    opacidad reducida (0.5) y un ícono rojo indicando error.
    """

    # -----------------------------
    # Verificación Global
    # -----------------------------
    final_verified = verified and saludo is not None and "Error" not in saludo
    icon_color = ft.colors.GREEN if final_verified else ft.colors.RED
    opacity_value = 1.0 if final_verified else 0.5

    # -----------------------------
    # Creación del Panel
    # -----------------------------
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Información del Sistema", size=20, weight="bold"),
                ft.Text(f"✅ Versión de Python: {version}", size=16),
                ft.Text(f"🤖 Modelo configurado: {get_model()}", size=16),
                ft.Text(f"💬 Saludo del agente: {saludo}", size=16),
                ft.Icon(name=ft.icons.CHECK_CIRCLE, color=icon_color, size=30),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        expand=True,
        bgcolor=ft.colors.LIGHT_BLUE,
        padding=10,
        alignment=ft.alignment.center,
        opacity=opacity_value
    )
