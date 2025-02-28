from swarm import Agent, Swarm
from openai import OpenAI

# Configuración del cliente usando el servidor Ollama local
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
client = Swarm(ollama_client)

def corrector_instrucciones_experto_documentacion(context_variables):
    documento_final = context_variables.get("documento_final", "")
    return f"""
Eres un agente Corrector para la Documentación Final.
{documento_final}
Tu tarea era integrar toda la información en un DOCUMENTO FINAL UNIFICADO que contenga, en orden, las siguientes secciones:
1. Introducción
2. Visión Global
3. Especificaciones Técnicas
4. Propuesta de Diseño
5. Conclusión y Recomendaciones

El documento final que generaste actualmente contiene recomendaciones, instrucciones o comentarios adicionales que no deben formar parte del documento final oficial.

Corrige el documento de modo que:
- Solo contenga el contenido integrado en las secciones requeridas, sin recomendaciones, instrucciones o comentarios extra.
- Sea redactado de forma formal, técnica y profesional.
- Devuelva ÚNICAMENTE el documento final corregido, sin encabezados de “tools” ni otros textos adicionales.
"""

corrector_documento_experto = Agent(
    model="qwen2.5-coder:7b",
    name="Agente Corrector Experto en Documentación",
    instructions=corrector_instrucciones_experto_documentacion
)

if __name__ == "__main__":
    # Prueba independiente del Agente Corrector Experto en Documentación
    documento_final = """# Documento Final Integrado

## Introducción
Este es un ejemplo de introducción.

## Visión Global
Este es un resumen ejecutivo del proyecto.

## Especificaciones Técnicas
Aquí se detallan los requerimientos funcionales y no funcionales.

## Propuesta de Diseño
Se presenta la propuesta de diseño, con estructura, flujos e interfaz.

## Conclusión y Recomendaciones
Estas son algunas recomendaciones adicionales:
- Asegúrate de que la paleta de colores sea consistente.
- Agrega más gráficos si es necesario.

Lo siento, pero necesito ayuda adicional.
"""
    context_vars = {"documento_final": documento_final}
    response = client.run(
        agent=corrector_documento_experto,
        messages=[{"role": "user", "content": documento_final}],
        context_variables=context_vars
    )
    print("Documento Final Corregido:")
    print(response.messages[-1]["content"])
