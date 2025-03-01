import json
from colorama import init, Fore, Style
init(autoreset=True)


# Importamos nuestros tres nuevos agentes y sus correctores
from agents_segunda_etapa.agente_arquitectura import (
    arquitecto,
    
    client as client_arquitecto
)
from agents_segunda_etapa.agente_ejecucion_comando import (
    ejecutor,
    client as client_creacion
)

def run_bioinspired_pipeline(informe_lider, documento_tecnico, informe_disenio, documento_final):
    """
    Pipeline bio-inspirado: 3 nuevos agentes
      1. Arquitecto de Software (genera blueprint)
      2. Agente de Creación de Archivos (crea la estructura)
      3. Agente de Verificación (valida la estructura final)
    Con la misma técnica iterativa, usando colorama para distinguir etapas.
    """

    print(Fore.CYAN + "=== Paso 1: Arquitecto de Software - Generación del Blueprint ===")
    context_architect = {
        "informe_lider": informe_lider,
        "documento_tecnico": documento_tecnico,
        "informe_disenio": informe_disenio,
        "documento_final": documento_final
    }
    # Llamada inicial al Arquitecto
    response_arquitecto = client_arquitecto.run(
        agent=arquitecto,
        messages=[{"role": "user", "content": "Genera el blueprint de la arquitectura.usando {informe_lider}, {documento_tecnico}, {informe_disenio}, {documento_final}."}],
        context_variables={},
        model_override=None,
        execute_tools=True
    )
    blueprint = response_arquitecto.messages[-1]["content"]
    print(Fore.GREEN + "Blueprint generado (Arquitecto):")
    print(blueprint, "\n")

    # Paso opcional: iterar correcciones para el blueprint si no fuera aceptable.
    # ...
    
    print(Fore.CYAN + "=== Paso 2: Creación de Archivos según el Blueprint ===")
    # Mismo estilo iterativo:
    blueprint_aprobado = False
    iter_creacion = 0
    log_creacion = ""
    while not blueprint_aprobado:
        iter_creacion += 1
        print(Fore.YELLOW + f"Creación de Archivos - Iteración {iter_creacion}")
        context_creacion = {"blueprint": blueprint}
        resp_creacion = client_creacion.run(
            agent=ejecutor,
            messages=[{"role": "user", "content": f"Crea la estructura exacta. del blueprint {blueprint}."}],
            context_variables=context_creacion,
            model_override=None,
            execute_tools=True
        )
        log_creacion = resp_creacion.messages[-1]["content"]
        print(Fore.MAGENTA + "Respuesta del Agente de Creación de Archivos:")
        print(log_creacion, "\n")
        
    print(Fore.CYAN + "blueprint:", blueprint)
    print(Fore.CYAN + "log_creacion:", log_creacion)
    return  blueprint, log_creacion

if __name__ == "__main__":
    # Ejemplo de uso
    informes = {
        "informe_lider": "Informe Líder (contenido)...",
        "documento_tecnico": "Documento Técnico (contenido)...",
        "informe_disenio": "Informe de Diseño (contenido)...",
        "documento_final": "Documento Final (contenido)..."
    }
    result_pipeline = run_bioinspired_pipeline(
        informes["informe_lider"],
        informes["documento_tecnico"],
        informes["informe_disenio"],
        informes["documento_final"]
    )
    print("\n=== Resultado Final del Pipeline Bio-Inspirado ===")
    print(json.dumps(result_pipeline, indent=4, ensure_ascii=False))
