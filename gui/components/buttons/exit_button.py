# gui/components/buttons/exit_button.py

import flet as ft

def create_exit_button(page: ft.Page) -> ft.ElevatedButton:
    """
    Crea y retorna un botón "Salir" con funcionalidad condicional:
      - En modo escritorio: cierra la ventana (window_destroy).
      - En modo web: limpia la página y muestra un mensaje de despedida.
    """
    def exit_action(e):
        if hasattr(page, "window_destroy"):
            page.window_destroy()
        else:
            # En modo web: reemplaza el contenido por un mensaje de despedida.
            page.controls.clear()
            goodbye_text = ft.Text("CHAU", size=50, weight="bold", text_align="center")
            page.add(
                ft.Container(
                    content=goodbye_text,
                    expand=True,
                    alignment=ft.alignment.center
                )
            )
            page.update()

    return ft.ElevatedButton(
        "Salir",
        bgcolor=ft.colors.RED,
        color=ft.colors.WHITE,
        on_click=exit_action
    )
