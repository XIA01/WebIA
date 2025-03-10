from swarm import Agent, Swarm
from openai import OpenAI

# Configuración del cliente usando tu servidor Ollama local
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",  # URL del servidor local de Ollama
    api_key="ollama"                      # La API key es requerida, pero no se usa realmente
)
client = Swarm(ollama_client)

def instrucciones_saludo(context_variables):
    """
    instrucciones
    """
    print(context_variables)
    name = context_variables.get("name", "Usuario")
    print(name)
    return f"""
    Eres un agente de saludo.      
    
    Tu tarea es saludar al usuario de nombre: '{name}', de manera cordial, indicando que el sistema funciona correctamente y hay agentes corriendo en el sistema.
    No ofrescas asistencia, simplemente indicale que el sistema tiene agentes corriendo, por lo tanto funciona bien!
    """

# Definición del agente de saludo usando el modelo de 14B
saludador = Agent(
    model="qwen2.5-coder:14b",
    name="Agente Saludo",
    instructions=instrucciones_saludo
)

if __name__ == "__main__":
    # Ejecutamos el agente pasando la variable de contexto "name"
    response = client.run(
        agent=saludador,
        messages=[{"role": "user", "content": "Salúdame"}],
        context_variables={"name": "ente biologico pensante"}
    )
    print(response.messages[-1]["content"])
