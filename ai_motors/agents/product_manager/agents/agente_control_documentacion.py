from swarm import Agent, Swarm
from openai import OpenAI

# Configuración del cliente usando el servidor Ollama local
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
client = Swarm(ollama_client)

# Variable global para indicar si el documento final ha sido aprobado.
sellado_documentacion = False

def instrucciones_control_documentacion(context_variables):
    
    return f"""
Eres un agente de Control de Documentación con amplia experiencia en la validación de informes integrados.

Tu tarea es revisar el DOCUMENTO FINAL INTEGRADO:  que se te proporciona y asegurarte de que cumpla con lo siguiente:
1. Contenga todas las secciones obligatorias: Introducción, Visión Global, Especificaciones Técnicas, Propuesta de Diseño y Conclusión.
2. La información debe estar redactada de forma clara, cohesiva y profesional.
3. NO debe incluir recomendaciones, instrucciones adicionales o comentarios que no formen parte del documento final.

Si el documento cumple con todos estos criterios, **NO devuelvas ningún texto**; en su lugar, invoca la función de sellado para marcar el documento como aprobado.
Si detectas errores o faltas, describe detalladamente las correcciones necesarias.

Por favor, asegúrate de que la respuesta final no contenga mensajes de disculpa ni recomendaciones; solo debe devolver el documento final aprobado mediante la función de sellado.
En caso contrario debes indicar los errores encontrados y las correcciones necesarias.
Se espera que tu respuesta sea clara, precisa y profesional. Marcando todos los errores y omisiones en el documento final.
"""

def sellar_documentacion(**kwargs):
    global sellado_documentacion
    sellado_documentacion = True
    return "[Documento Final Sellado]"

control_documentacion = Agent(
    model="qwen2.5-coder:14b",
    name="Agente de Control de Documentación",
    instructions=instrucciones_control_documentacion,
    functions=[sellar_documentacion]
)

if __name__ == "__main__":
    # Prueba independiente del Agente de Control de Documentación
    documento_final = """# Documento Final Integrado

## Introducción
Breve descripción del proyecto.

## Visión Global
Resumen ejecutivo del proyecto.

## Especificaciones Técnicas
Detalle de requerimientos funcionales y no funcionales.

## Propuesta de Diseño
Resumen de la propuesta de diseño, estructura, flujos e interfaz.

## Conclusión
Resumen final y recomendaciones para el desarrollo.
"""
    context_vars = {"documento_final": documento_final}
    response = client.run(
        agent=control_documentacion,
        messages=[{"role": "user", "content": documento_final}],
        context_variables=context_vars
    )
    print("Respuesta de Control de Documentación:")
    print(response.messages[-1]["content"])
