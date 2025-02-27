from swarm import Agent, Swarm
from openai import OpenAI

# Configuración del cliente (puede compartirse o ser independiente)
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",  
    api_key="ollama"                       
)
client = Swarm(ollama_client)

def instrucciones_control_calidad(context_variables):
    informe_secundario1 = context_variables.get("informe_secundario1", "")
    informe_secundario2 = context_variables.get("informe_secundario2", "")
    return f"""
Eres un agente de Control de Calidad.

Tu tarea es revisar el documento que se te presenta (prompt) y compararlo con los informes secundarios 
que se te suministran en las variables de contexto ("informe_secundario1" e "informe_secundario2").

-----------------------
informe_secundario1:
{informe_secundario1}
-----------------------
informe_secundario2:
{informe_secundario2}

Verifica que el documento incluya todos los elementos esenciales, sea coherente y claro.

Si detectas que falta algún elemento o existe alguna inconsistencia, responde indicando las correcciones necesarias.

Si el documento cumple con los criterios, llama a la función sellar() para finalizar tu trabajo 
informando que el documento ha sido sellado.
"""

sellado_lider = False

def sellar(**kwargs):
    import agents.agente_control_calidad as ac
    print("Se está por sellar...", ac.sellado_lider)
    ac.sellado_lider = True
    print("Documento sellado:", ac.sellado_lider)

control_calidad = Agent(
    model="qwen2.5-coder:14b",
    name="Agente Control de Calidad",
    instructions=instrucciones_control_calidad,
    functions=[sellar]
)

if __name__ == "__main__":
    # Ejemplo de prueba
    documento_inicial = "Documento técnico: incluye funcionalidades, flujos y criterios incompletos."
    context_vars = {
        "informe_secundario1": "Informe de Líder de Producto",
        "informe_secundario2": "Informe de Diseño"
    }
    response = client.run(
        agent=control_calidad,
        messages=[{"role": "user", "content": documento_inicial}],
        context_variables=context_vars
    )
    print("Respuesta de Control de Calidad:\n", response.messages[-1]["content"])
