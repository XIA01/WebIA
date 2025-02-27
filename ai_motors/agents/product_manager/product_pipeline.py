# ai_motors/agents/product_manager/product_pipeline.py
import json

import agents.agente_control_calidad as ac  # ac.sellado_lider será nuestra variable

from agents.agente_lider_de_Producto import agente_lider_de_producto, corrector_documento_lider, client as client_lider
from agents.agente_analista_de_negocio import analista_de_negocio, client as client_analista
from agents.agente_disenador_uxui import disenador_uxui, client as client_disenador
from agents.agente_control_calidad import control_calidad, client as client_control

def run_product_pipeline(prompt: str) -> dict:
    """
    Ejecuta el pipeline completo del Producto, incluyendo Control de Calidad.
    
    Flujo:
      1. El agente Líder de Producto genera el informe inicial.
      2. El agente Analista de Negocio genera el documento técnico.
      3. El agente Diseñador UX/UI genera el informe de diseño.
      4. Para cada informe se invoca el agente de Control de Calidad y se mantiene en un bucle
         mientras la variable de sellado (ac.sellado_lider) sea False.
         Si el agente detecta errores, se llama al agente Corrector para que corrija el informe.
    
    Retorna:
      dict - Los informes finales sellados.
    """
    # Paso 1: Agente Líder de Producto
    response_lider = client_lider.run(
        agent=agente_lider_de_producto,
        messages=[{"role": "user", "content": prompt}],
        context_variables={}
    )
    informe_lider = response_lider.messages[-1]["content"]
    # print("Informe Líder de Producto:\n", informe_lider)

    # Paso 2: Agente Analista de Negocio
    response_analista = client_analista.run(
        agent=analista_de_negocio,
        messages=[{"role": "user", "content": informe_lider}],
        context_variables={}
    )
    documento_tecnico = response_analista.messages[-1]["content"]
    # print("Documento Técnico:\n", documento_tecnico)

    # Paso 3: Agente Diseñador UX/UI
    response_disenador = client_disenador.run(
        agent=disenador_uxui,
        messages=[{"role": "user", "content": documento_tecnico}],
        context_variables={}
    )
    informe_disenio = response_disenador.messages[-1]["content"]
    # print("Informe de Diseño:\n", informe_disenio)

    # Paso 4: Control de Calidad para el informe del Líder
    # Reiniciamos la variable de sellado en el módulo de control
    ac.sellado_lider = False
    control_sellado_lider = 0
    while not ac.sellado_lider:
        control_sellado_lider += 1
        print(f"Control de Calidad (Informe Líder): Ejecutando revisión...{control_sellado_lider}")
        context_vars = {
            "informe_secundario1": documento_tecnico,
            "informe_secundario2": informe_disenio
        }
        resp_control = client_control.run(
            agent=control_calidad,
            messages=[{"role": "user", "content": informe_lider}],
            context_variables=context_vars
        )
        result_lider = resp_control.messages[-1]["content"]

        # Si la respuesta indica que se selló, se espera que ac.sellado_lider se haya puesto en True
        if not ac.sellado_lider:
            # Si hay correcciones, se llama al agente Corrector y se actualiza el informe.
            resp_corrector = client_lider.run(
                agent=corrector_documento_lider,
                messages=[{"role": "user", "content": result_lider}],
                context_variables={"documento_anterior": informe_lider}
            )
            informe_lider = resp_corrector.messages[-1]["content"]
            print("Informe corregido, se reevalúa en Control de Calidad.")

    return  informe_lider, documento_tecnico, informe_disenio
    

if __name__ == "__main__":
    ejemplo_prompt = (
        "El cliente solicita una plataforma web para una IA que quiere ser presidente. "
        "Se requiere un diseño moderno, intuitivo y accesible, con páginas completas para la campaña. "
        "El proyecto se realizará utilizando HTML, CSS y JavaScript."
    )
    informe_lider, documento_tecnico, informe_disenio = run_product_pipeline(ejemplo_prompt)
    print("Informes Finales Sellados:")
    print("Informe Líder de Producto:\n", informe_lider)
    print("Documento Técnico:\n", documento_tecnico)
    print("Informe de Diseño:\n", informe_disenio)
