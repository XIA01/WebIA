# ai_motors/agents/test_agents/agente_saludo.py

from crewai import Agent, Task, Crew, Process
from ai_motors.config.model_config import get_model

def obtener_saludo() -> str:
    """
    Crea un agente de saludo, le asigna una tarea de saludo, 
    ejecuta el Crew de forma secuencial y devuelve el resultado.
    """
    # Verificar que el modelo está disponible
    model = get_model()
    print("🔍 Modelo obtenido para el agente:", model)  # DEBUG: Verifica que el modelo es correcto

    # Definir el agente de saludo
    saludo_agent = Agent(
        role="Agente de Saludo",
        goal="Saludar de forma cordial, amistosa y en español.",
        backstory="Eres el encargado de dar un saludo cálido y personalizado a la audiencia. En español.",
        verbose=True,
        allow_delegation=False,  # Evita que CrewAI fuerce pasos innecesarios

        llm=model  # Asegurar que el modelo sea válido
    )
    
    # Definir la tarea de saludo
    saludo_task = Task(
        description= "Saluda a la audiencia de forma cálida ,amistosa y en español.",
        expected_output= "Hola humano!!",
        agent=saludo_agent
    )
    
    # Crear un Crew con este único agente y tarea
    crew = Crew(
        agents=[saludo_agent],
        tasks=[saludo_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Ejecutar el Crew y obtener la respuesta del saludo
    resultado = crew.kickoff()  # CrewAI devuelve el resultado directamente
    print("✅ Resultado del Crew:", resultado)  # Verificar salida
    return resultado  # CrewAI maneja la salida en `kickoff()`

if __name__ == "__main__":
    # Prueba de ejecución del Crew y del agente
    print("Saludo (CrewAI):", obtener_saludo())
    
    # Prueba directa usando litellm.completion
    '''from litellm import completion

    response = completion(
        model="ollama/llama2-uncensored", 
        messages=[{"content": "responde quiene eres y que eres capaz y porque te llamas uncensored, siempre en español", "role": "user"}], 
        api_base="http://localhost:11434"
    )
    print("Respuesta litellm.completion:", response.choices[0].message.content)'''

