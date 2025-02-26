# ai_motors/agents/product_manager/product_pipeline.py

# Usamos importaciones relativas para evitar problemas con PYTHONPATH.
from agents.agente_lider_de_Producto import agente_lider_de_producto, client as client_lider
from agents.agente_analista_de_negocio import analista_de_negocio, client as client_analista
from agents.agente_disenador_uxui import disenador_uxui, client as client_disenador

def run_product_pipeline(prompt: str) -> str:
    """
    Ejecuta el pipeline del Producto.
    
    El flujo es:
      1. El agente Líder de Producto transforma el requerimiento (prompt) en un informe inicial sellado.
      2. El agente Analista de Negocio analiza el informe inicial y genera un documento técnico detallado.
      3. El agente Diseñador UX/UI utiliza el documento técnico para elaborar un informe de diseño final.
    
    Parámetro:
      prompt: str - El requerimiento y notas del cliente.
      
    Retorna:
      str - Informe final de diseño generado por el agente Diseñador UX/UI.
    """
    # Paso 1: Ejecutar el agente Líder de Producto
    response_lider = client_lider.run(
        agent=agente_lider_de_producto,
        messages=[{"role": "user", "content": prompt}],
        context_variables={}
    )
    informe_inicial = response_lider.messages[-1]["content"]
    print("Informe Líder de Producto:\n", informe_inicial)
    
    # Paso 2: Ejecutar el agente Analista de Negocio
    response_analista = client_analista.run(
        agent=analista_de_negocio,
        messages=[{"role": "user", "content": informe_inicial}],
        context_variables={}
    )
    documento_tecnico = response_analista.messages[-1]["content"]
    print("Documento Técnico:\n", documento_tecnico)
    
    # Paso 3: Ejecutar el agente Diseñador UX/UI
    response_disenador = client_disenador.run(
        agent=disenador_uxui,
        messages=[{"role": "user", "content": documento_tecnico}],
        context_variables={}
    )
    informe_diseño = response_disenador.messages[-1]["content"]
    return informe_diseño

if __name__ == "__main__":
    # Ejemplo de uso independiente del pipeline
    ejemplo_prompt = (
        "El cliente solicita una plataforma web para una inteligencia artificial argentina que quiere ser presidente de Chile. "
        "Se deberá juntar dinero para su campaña. "
        "Se requiere un diseño moderno y atractivo, con una interfaz intuitiva y fácil de usar. "
        "Además, deberá contener todas las páginas necesarias para la campaña política de una IA que quiere ser presidente del mundo. "
        "El proyecto se realizará utilizando HTML, CSS y JavaScript."
    )
    informe_final = run_product_pipeline(ejemplo_prompt)
    print("\nInforme Final de Diseño:\n", informe_final)
