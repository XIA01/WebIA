import json
from colorama import init, Fore, Style

from bioinspired_pipeline import run_bioinspired_pipeline
init(autoreset=True)

import agents.agente_control_calidad as ac  # ac.sellado_lider se usa en los controles previos

from agents.agente_lider_de_Producto import (
    agente_lider_de_producto, 
    corrector_documento_lider, 
    client as client_lider
)
from agents.agente_analista_de_negocio import (
    analista_de_negocio,
    corrector_documento_analista, 
    client as client_analista
)
from agents.agente_disenador_uxui import (
    disenador_uxui,
    corrector_documento_disenador, 
    client as client_disenador
)
from agents.agente_control_calidad import control_calidad, client as client_control
from agents.agente_experto_en_documentacion import experto_documentacion, client as client_experto

# Importamos el módulo completo para el control final de documentación
import agents.agente_control_documentacion as doc_control
from agents.agente_control_documentacion import control_documentacion, client as client_control_doc

# Asumimos que ya tienes un agente corrector para la documentación final
from agents.agente_corrector_experto_documentacion import corrector_documento_experto, client as client_corrector_experto

def run_product_pipeline(prompt: str) -> dict:
    """
    Ejecuta el pipeline completo del Producto, incluyendo controles y la integración final.
    
    Flujo:
      1. Genera el informe del Líder de Producto.
      2. Genera el documento técnico (Analista de Negocio).
      3. Genera el informe de diseño (Diseñador UX/UI).
      4. Aplica control de calidad a cada informe mediante bucles (mientras la variable global no se apruebe).
      5. Integra los historiales de control de calidad en un único mensaje.
      6. El agente Experto en Documentación integra la información en un documento final.
      7. Se valida el documento final con el agente de Control de Documentación en un bucle.
    
    Retorna:
      dict - Con los informes finales y el documento final integrado.
    """
    # Paso 1: Informe del Líder de Producto
    print(Fore.CYAN + "=== Paso 1: Generación del Informe del Líder de Producto ===")
    response_lider = client_lider.run(
        agent=agente_lider_de_producto,
        messages=[{"role": "user", "content": prompt}],
        context_variables={},
        model_override=None,
        execute_tools=True
    )
    informe_lider = response_lider.messages[-1]["content"]
    print(Fore.GREEN + "Informe Líder de Producto generado:")
    print(informe_lider, "\n")
    
    # Paso 2: Documento Técnico (Analista de Negocio)
    print(Fore.CYAN + "=== Paso 2: Generación del Documento Técnico (Analista de Negocio) ===")
    response_analista = client_analista.run(
        agent=analista_de_negocio,
        messages=[{"role": "user", "content": informe_lider}],
        context_variables={},
        model_override=None,
        execute_tools=True
    )
    documento_tecnico = response_analista.messages[-1]["content"]
    print(Fore.GREEN + "Documento Técnico generado:")
    print(documento_tecnico, "\n")
    
    # Paso 3: Informe de Diseño (Diseñador UX/UI)
    print(Fore.CYAN + "=== Paso 3: Generación del Informe de Diseño (Diseñador UX/UI) ===")
    response_disenador = client_disenador.run(
        agent=disenador_uxui,
        messages=[{"role": "user", "content": documento_tecnico}],
        context_variables={},
        model_override=None,
        execute_tools=True
    )
    informe_disenio = response_disenador.messages[-1]["content"]
    print(Fore.GREEN + "Informe de Diseño generado:")
    print(informe_disenio, "\n")
    
    # Paso 4: Control de Calidad para el Informe del Líder
    print(Fore.CYAN + "=== Paso 4: Control de Calidad para Informe del Líder ===")
    ac.sellado_lider = False
    control_sellado_lider = 0
    conversation_history_lider = []
    while not ac.sellado_lider:
        control_sellado_lider += 1
        print(Fore.YELLOW + f"Control de Calidad (Informe Líder) - Iteración {control_sellado_lider}")
        context_vars = {
            "informe_secundario1": documento_tecnico,
            "informe_secundario2": informe_disenio
        }
        resp_control = client_control.run(
            agent=control_calidad,
            messages=[{"role": "user", "content": informe_lider}],
            context_variables=context_vars,
            model_override=None,
            execute_tools=True
        )
        conversation_history_lider.extend(resp_control.messages)
        result_lider = resp_control.messages[-1]["content"]
        print(Fore.MAGENTA + "Respuesta de Control de Calidad para Informe Líder:")
        print(result_lider, "\n")
        if not ac.sellado_lider:
            history = resp_control.messages.copy()
            history.append({"role": "user", "content": result_lider})
            resp_corrector = client_lider.run(
                agent=corrector_documento_lider,
                messages=history,
                context_variables={"documento_anterior": informe_lider},
                model_override=None,
                execute_tools=True
            )
            informe_lider = resp_corrector.messages[-1]["content"]
            conversation_history_lider.extend(resp_corrector.messages)
            print(Fore.GREEN + "Informe Líder corregido. Nueva versión:")
            print(informe_lider, "\n")
    
    # Paso 5: Control de Calidad para el Documento Técnico
    print(Fore.CYAN + "=== Paso 5: Control de Calidad para Documento Técnico ===")
    ac.sellado_lider = False
    control_sellado_tecnico = 0
    conversation_history_tecnico = []
    while not ac.sellado_lider:
        control_sellado_tecnico += 1
        print(Fore.YELLOW + f"Control de Calidad (Documento Técnico) - Iteración {control_sellado_tecnico}")
        context_vars = {
            "informe_secundario1": informe_lider,
            "informe_secundario2": informe_disenio
        }
        resp_control = client_control.run(
            agent=control_calidad,
            messages=[{"role": "user", "content": documento_tecnico}],
            context_variables=context_vars,
            model_override=None,
            execute_tools=True
        )
        conversation_history_tecnico.extend(resp_control.messages)
        result_tecnico = resp_control.messages[-1]["content"]
        print(Fore.MAGENTA + "Respuesta de Control de Calidad para Documento Técnico:")
        print(result_tecnico, "\n")
        if not ac.sellado_lider:
            history = resp_control.messages.copy()
            history.append({"role": "user", "content": result_tecnico})
            resp_corrector = client_analista.run(
                agent=corrector_documento_analista,
                messages=history,
                context_variables={"documento_anterior": documento_tecnico},
                model_override=None,
                execute_tools=True
            )
            documento_tecnico = resp_corrector.messages[-1]["content"]
            conversation_history_tecnico.extend(resp_corrector.messages)
            print(Fore.GREEN + "Documento Técnico corregido. Nueva versión:")
            print(documento_tecnico, "\n")
    
    # Paso 6: Control de Calidad para el Informe de Diseño
    print(Fore.CYAN + "=== Paso 6: Control de Calidad para Informe de Diseño ===")
    ac.sellado_lider = False
    control_sellado_disenio = 0
    conversation_history_disenio = []
    while not ac.sellado_lider:
        control_sellado_disenio += 1
        print(Fore.YELLOW + f"Control de Calidad (Informe de Diseño) - Iteración {control_sellado_disenio}")
        context_vars = {
            "informe_secundario1": informe_lider,
            "informe_secundario2": documento_tecnico
        }
        resp_control = client_control.run(
            agent=control_calidad,
            messages=[{"role": "user", "content": informe_disenio}],
            context_variables=context_vars,
            model_override=None,
            execute_tools=True
        )
        conversation_history_disenio.extend(resp_control.messages)
        result_disenio = resp_control.messages[-1]["content"]
        print(Fore.MAGENTA + "Respuesta de Control de Calidad para Informe de Diseño:")
        print(result_disenio, "\n")
        if not ac.sellado_lider:
            history = resp_control.messages.copy()
            history.append({"role": "user", "content": result_disenio})
            resp_corrector = client_disenador.run(
                agent=corrector_documento_disenador,
                messages=history,
                context_variables={"documento_anterior": informe_disenio},
                model_override=None,
                execute_tools=True
            )
            informe_disenio = resp_corrector.messages[-1]["content"]
            conversation_history_disenio.extend(resp_corrector.messages)
            print(Fore.GREEN + "Informe de Diseño corregido. Nueva versión:")
            print(informe_disenio, "\n")
    
    # Paso 7: Integración Final con el Experto en Documentación
    print(Fore.CYAN + "=== Paso 7: Integración Final (Experto en Documentación) ===")
    messages_experto = [
        {"role": "user", "content": (
            "Utiliza los siguientes informes aprobados:\n\n"
            f"--- Informe del Líder de Producto ---\n{informe_lider}\n\n"
            f"--- Documento Técnico ---\n{documento_tecnico}\n\n"
            f"--- Informe de Diseño ---\n{informe_disenio}\n\n"
            "Integra toda esta información en un DOCUMENTO FINAL UNIFICADO, sin recomendaciones adicionales."
        )}
    ]
    resp_experto = client_experto.run(
        agent=experto_documentacion,
        messages=messages_experto,
        context_variables={},
        model_override=None,
        execute_tools=True
    )
    documento_final = resp_experto.messages[-1]["content"]
    print(Fore.GREEN + "Documento Final Integrado:")
    print(documento_final, "\n")
    
    # Paso 8: Control Final de Documentación con el Agente de Control de Documentación
    print(Fore.CYAN + "=== Paso 8: Control Final de Documentación ===")
    # Usamos la variable global del módulo doc_control para que se actualice correctamente
    doc_control.sellado_documentacion = False
    control_final_iter = 0
    conversation_history_documentacion = []
    # copia del documento final para el control final
    documento_final2 = documento_final
    while not doc_control.sellado_documentacion:
        control_final_iter += 1
        print(Fore.YELLOW + f"Control Final de Documentación - Iteración {control_final_iter}")
        resp_control_doc = client_control_doc.run(
            agent=control_documentacion,
            messages=[{"role": "user", "content": documento_final}],
            context_variables={"documento_final": documento_final2},
            model_override=None,
            execute_tools=True
        )
        conversation_history_documentacion.extend(resp_control_doc.messages)
        result_doc = resp_control_doc.messages[-1]["content"]
        print(Fore.MAGENTA + "Respuesta de Control de Documentación:")
        print(result_doc, "\n")
        if not doc_control.sellado_documentacion:
            history = resp_control_doc.messages.copy()
            history.append({"role": "user", "content": result_doc})
            resp_corrector = client_corrector_experto.run(
                agent=corrector_documento_experto,
                messages=history,
                context_variables={"documento_final": documento_final2},
                model_override=None,
                execute_tools=True
            )
            documento_final = resp_corrector.messages[-1]["content"]
            conversation_history_documentacion.extend(resp_corrector.messages)
            print(Fore.GREEN + "Documento Final corregido. Nueva versión:")
            print(documento_final, "\n")
    
    print(Fore.GREEN + "Documento Final aprobado!")
    
    # Unificamos todo el historial de conversación final (opcional)
    conversation_history_final = "\n".join([
        "=== Historial - Informe Líder ===",
        "\n".join([msg["content"] for msg in conversation_history_lider]),
        "=== Historial - Documento Técnico ===",
        "\n".join([msg["content"] for msg in conversation_history_tecnico]),
        "=== Historial - Informe de Diseño ===",
        "\n".join([msg["content"] for msg in conversation_history_disenio]),
        "=== Historial - Control Final de Documentación ===",
        "\n".join([msg["content"] for msg in conversation_history_documentacion])
    ])
    bp, log = run_bioinspired_pipeline(informe_lider, documento_tecnico, informe_disenio, documento_final)
    print(Fore.CYAN + "blueprint:", bp)
    print(Fore.CYAN + "log_creacion:", log)
    return {
        "informe_lider": informe_lider,
        "documento_tecnico": documento_tecnico,
        "informe_disenio": informe_disenio,
        "documento_final": documento_final,
        "historial_conversacion": conversation_history_final
    }

if __name__ == "__main__":
    ejemplo_prompt = (
        "El cliente solicita una plataforma web para una especie extraterrestre parasita que quiero dominar el mundo, utilizan un lenguaje cuniforme para comunicarse, pero haz todo es español."
        "Se requiere un diseño moderno, intuitivo y accesible, con páginas completas para la campaña. "
        "El proyecto se realizará utilizando HTML, CSS y JavaScript."
    )
    informes_finales = run_product_pipeline(ejemplo_prompt)
    print("\n=== Informes Finales Sellados e Integrados ===")
    print(json.dumps(informes_finales, indent=4, ensure_ascii=True))
    print("\n=== Documento Final ===")
    print(informes_finales["documento_final"])
