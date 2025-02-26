from swarm import Agent, Swarm
from openai import OpenAI

# Configuración del cliente usando el servidor Ollama local
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",  # URL del servidor local de Ollama
    api_key="ollama"                       # La API key es requerida, pero no se usa realmente
)
client = Swarm(ollama_client)

def instrucciones_disenador_uxui(context_variables):
    """
    Eres un agente Diseñador UX/UI.

    Tu tarea es recibir el documento técnico generado por el Analista de Negocio y:
      1. Analizar la información para extraer los elementos esenciales de la experiencia de usuario y la interfaz visual.
      2. Elaborar una propuesta de diseño que incluya:
         - La estructura de la interfaz.
         - Esquemas de cada pantalla.
         - Flujos de usuario.
         - Una guía de estilo que defina la apariencia y el comportamiento interactivo.
      3. Detallar en un informe de diseño cada uno de estos aspectos de manera clara y precisa.
      4. Revisar la propuesta para garantizar que cumple con los requerimientos técnicos y de experiencia.
      5. Entregar el informe de diseño final sin omisiones al siguiente responsable.

    Debes ser ultradetallado y estructurar el informe de diseño de forma profesional.
    """
    return instrucciones_disenador_uxui.__doc__

# Definición del agente Diseñador UX/UI
disenador_uxui = Agent(
    model="qwen2.5-coder:14b",
    name="Agente Diseñador UX/UI",
    instructions=instrucciones_disenador_uxui
)

if __name__ == "__main__":
    # Prueba independiente del agente con un documento técnico simulado
    documento_tecnico = (
        "Documento técnico generado por el Analista de Negocio (simulado):\n"
        "Descripción de funcionalidades, flujos de interacción y criterios de aceptación..."
    )
    response = client.run(
        agent=disenador_uxui,
        messages=[{"role": "user", "content": documento_tecnico}],
        context_variables={}
    )
    print(response.messages[-1]["content"])
