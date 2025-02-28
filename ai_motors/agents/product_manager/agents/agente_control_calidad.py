# ai_motors/agents/product_manager/agents/agente_control_calidad.py
from swarm import Agent, Swarm
from openai import OpenAI

# Configuración del cliente usando el servidor Ollama local
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
client = Swarm(ollama_client)

# Definimos la variable global para el estado de sellado (en este caso para el informe del Líder)
sellado_lider = False

def instrucciones_control_calidad(context_variables):
    informe_secundario1 = context_variables.get("informe_secundario1", "")
    informe_secundario2 = context_variables.get("informe_secundario2", "")
    return f"""
Eres un agente de Control de Calidad.

Tu tarea es revisar el documento que se te presenta (prompt) y compararlo con los informes secundarios proporcionados en las variables de contexto ("informe_secundario1" e "informe_secundario2").
Informes secundarios:
- Informe 1: {informe_secundario1}
- Informe 2: {informe_secundario2}

Verifica que el documento incluya todos los elementos esenciales, y que sea coherente y claro.

- Si detectas errores o inconsistencias, responde indicando las correcciones necesarias.
- Si, y solo si, el documento cumple con todos los criterios, **no devuelvas ningún texto**; en su lugar, invoca directamente la función de sellado (sin mencionar 'sellar()' en tu respuesta) para finalizar tu trabajo y marcar el documento como aprobado.
"""

def sellar(**kwargs):
    """
    Función sellar: valida el documento.
    """
    global sellado_lider
    sellado_lider = True
    return "[Documento Sellado]"

control_calidad = Agent(
    model="qwen2.5-coder:7b",
    name="Agente Control de Calidad",
    instructions=instrucciones_control_calidad,
    functions=[sellar]
)

if __name__ == "__main__":
    # Prueba independiente
    documento_inicial = "Documento técnico: contiene todos los elementos esenciales, es claro y coherente."
    context_vars = {
        "informe_secundario1": "Informe de Líder de Producto Aprobado.",
        "informe_secundario2": "Informe de Diseño Aprobado."
    }
    response = client.run(
        agent=control_calidad,
        messages=[{"role": "user", "content": documento_inicial}],
        context_variables=context_vars
    )
    print("Respuesta de Control de Calidad:")
    print(response.messages[-1]["content"])
