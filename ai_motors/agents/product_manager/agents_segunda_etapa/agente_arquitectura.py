from swarm import Agent, Swarm
from openai import OpenAI

# Configuración del cliente (puedes centralizarlo)
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
client = Swarm(ollama_client)

def instrucciones_arquitectura(context_variables):
    # No se usan variables de contexto: todo se recibe en el mensaje
    return """
Eres un agente de Arquitectura. Tu tarea es recibir CUATRO documentos integrados (Informe del Líder, Documento Técnico, Informe de Diseño y Documento Final)
mediante un único mensaje de usuario. A partir de esa información, debes generar un blueprint de la arquitectura del proyecto.
Utiliza conceptos bio-inspirados: imagina que cada documento es una "célula" con información genética y que, mediante procesos de cooperación y selección,
debes definir la estructura de directorios, los nombres y extensiones de archivos, las relaciones entre módulos y cualquier dependencia necesaria.
Tu respuesta debe incluir:
  1. La estructura de directorios (por ejemplo: src/, docs/, tests/).
  2. Nombres y descripciones breves de los archivos principales.
  3. Las dependencias y relaciones entre los módulos.
  4. Una breve explicación de cómo esta arquitectura permite adaptabilidad y evolución.
Devuelve ÚNICAMENTE el blueprint final sin comentarios ni instrucciones adicionales.
"""

arquitecto = Agent(
    model="qwen2.5-coder:14b",
    name="Agente de Arquitectura",
    instructions=instrucciones_arquitectura
)

if __name__ == "__main__":
    # Prueba independiente: los 4 documentos se concatenan en un único mensaje
    documentos = (
        "--- Informe del Líder ---\nContenido del informe del líder...\n\n" +
        "--- Documento Técnico ---\nContenido del documento técnico...\n\n" +
        "--- Informe de Diseño ---\nContenido del informe de diseño...\n\n" +
        "--- Documento Final ---\nContenido del documento final..."
    )
    response = client.run(
        agent=arquitecto,
        messages=[{"role": "user", "content": documentos}],
        context_variables={}
    )
    print("Blueprint de Arquitectura:")
    print(response.messages[-1]["content"])
