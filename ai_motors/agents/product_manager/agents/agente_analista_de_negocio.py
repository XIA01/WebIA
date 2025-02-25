# ai_motors/agents/product_manager/agents/agente_analista_de_negocio.py

from swarm import Agent, Swarm
from openai import OpenAI

# Configuración del cliente (se puede reutilizar el mismo de otros agentes)
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",  # URL del servidor local de Ollama
    api_key="ollama"                       # API key (no se utiliza realmente)
)
client = Swarm(ollama_client)

def instrucciones_analista_de_negocio(context_variables):
    """
    Eres un agente Analista de Negocio.

    Tu tarea es recibir el informe del Líder de Producto y:
      1. Leer detenidamente el informe para comprender la visión global del proyecto.
      2. Identificar y clasificar los requerimientos en funcionales y no funcionales.
      3. Transformar la información recopilada en un documento técnico detallado que incluya:
         - Descripciones precisas de cada funcionalidad.
         - Flujos de interacción.
         - Criterios de aceptación medibles.
      4. Revisar el documento para asegurar su claridad y completitud.
      5. Entregar el informe técnico final sin modificaciones pendientes al siguiente responsable.

    Debes ser ultradetallado y estructurar el documento de forma profesional.
    """
    return instrucciones_analista_de_negocio.__doc__

analista_de_negocio = Agent(
    model="qwen2.5-coder:14b",
    name="Agente Analista de Negocio",
    instructions=instrucciones_analista_de_negocio
)

if __name__ == "__main__":
    # Prueba independiente del agente con un informe simulado
    informe_inicial = (
        "Informe Inicial del Producto (simulado):\n"
        "Reunión y Agenda: ...\n"
        "Notas de la Reunión: ...\n"
        "Informe de Visión del Producto: ...\n"
        "Revisión Final: ..."
    )
    response = client.run(
        agent=analista_de_negocio,
        messages=[{"role": "user", "content": informe_inicial}],
        context_variables={}
    )
    print(response.messages[-1]["content"])
