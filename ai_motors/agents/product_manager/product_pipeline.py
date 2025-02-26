# ai_motors/agents/product_manager/product_pipeline.py

# Usamos importaciones relativas para evitar problemas con PYTHONPATH.
from agents.agente_lider_de_Producto import agente_lider_de_producto, client as client_lider
from agents.agente_analista_de_negocio import analista_de_negocio, client as client_analista

def run_product_pipeline(prompt: str) -> str:
    """
    Ejecuta el pipeline del Producto.
    
    1. Utiliza el agente Líder de Producto para transformar el requerimiento (prompt)
       en un informe inicial sellado.
    2. Utiliza el agente Analista de Negocio para analizar el informe inicial y generar un
       documento técnico final detallado.
    
    Parámetro:
      prompt: str - El requerimiento y notas del cliente.
      
    Retorna:
      str - Informe técnico final generado por el agente Analista de Negocio.
    """
    # Paso 1: Ejecutar el agente Líder de Producto
    response_lider = client_lider.run(
        agent=agente_lider_de_producto,
        messages=[{"role": "user", "content": prompt}],
        context_variables={}
    )
    informe_inicial = response_lider.messages[-1]["content"]
    print("Informe Lider de producto: ", informe_inicial)
    # Paso 2: Ejecutar el agente Analista de Negocio
    response_analista = client_analista.run(
        agent=analista_de_negocio,
        messages=[{"role": "user", "content": informe_inicial}],
        context_variables={}
    )
    informe_final = response_analista.messages[-1]["content"]
    return informe_final

if __name__ == "__main__":
    # Ejemplo de uso independiente del pipeline
    ejemplo_prompt = (
        "El cliente solicita una plataforma web para una inteligencia artificial argentina que quiere ser presidente de Chile "
        "Se deberá juntar dinero para su campaña. "
        "Se requiere un diseño moderno y atractivo, con una interfaz intuitiva y fácil de usar. "
        "Además, deberá contener todas las páginas necesarias para la campaña política de una IA que quiere ser presidente del mundo. "
        "El cliente solicita que el proyecto se realice utilizando HTML, CSS y JavaScript."
    )
    informe_final = run_product_pipeline(ejemplo_prompt)
    print(informe_final)
