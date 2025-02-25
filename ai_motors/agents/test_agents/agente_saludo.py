# ai_motors/agents/test_agents/agente_saludo.py


def obtener_saludo() -> str:
    """
    Crea un agente de saludo, le asigna una tarea de saludo, 
    
    """
    resultado = "Hola, soy un agente de saludo. ¿En qué puedo ayudarte?"    
    return resultado  

if __name__ == "__main__":
    # Prueba de ejecución del Crew y del agente
    print("Saludo (ia):", obtener_saludo())
    