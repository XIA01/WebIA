from swarm import Agent, Swarm
from openai import OpenAI

# Configuración del cliente usando el servidor Ollama local
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
client = Swarm(ollama_client)

def instrucciones_experto_documentacion(context_variables):
    
    return f"""
Eres un agente Experto en Documentación con conocimientos avanzados en integración de información y redacción profesional.

Tu tarea es integrar de forma coherente y estructurada la información de los siguientes informes aprobados:


Debes redactar un DOCUMENTO FINAL UNIFICADO que contenga, en orden, las siguientes secciones:

1. **Introducción:** Describe brevemente el proyecto, su propósito y el contexto.
2. **Visión Global:** Resume de forma ejecutiva la propuesta del proyecto.
3. **Especificaciones Técnicas:** Detalla los requerimientos funcionales y no funcionales, incluyendo tecnología utilizada y limitaciones.
4. **Propuesta de Diseño:** Resume la propuesta de diseño, la estructura de la interfaz, los flujos de usuario y las pautas visuales.
5. **Conclusión y Recomendaciones:** Ofrece un cierre que sintetice el contenido y recomiende pasos para la implementación.

Es MUY IMPORTANTE que:
- El documento final sea único, claro, cohesivo y sin comentarios adicionales ni instrucciones.
- No incluyas mensajes que indiquen dudas, disculpas o incapacidad de integrar la información.
- Utilices un tono formal y técnico, tal como se espera en un documento oficial de proyecto.

Devuelve ÚNICAMENTE el documento final integrado, sin encabezados de “tools” ni textos que no formen parte del documento final.
"""

experto_documentacion = Agent(
    model="qwen2.5-coder:14b",
    name="Agente Experto en Documentación",
    instructions=instrucciones_experto_documentacion
)

if __name__ == "__main__":
    # Prueba independiente del agente Experto en Documentación
    informe_lider = "Informe Líder de Producto: [Contenido aprobado]."
    documento_tecnico = "Documento Técnico: [Contenido aprobado]."
    informe_disenio = "Informe de Diseño: [Contenido aprobado]."
    context_vars = {
        "informe_lider": informe_lider,
        "documento_tecnico": documento_tecnico,
        "informe_disenio": informe_disenio
    }
    response = client.run(
        agent=experto_documentacion,
        messages=[{"role": "user", "content": "Integra toda la documentación en un único documento final."}],
        context_variables=context_vars
    )
    print("Documento Final de Proyecto:")
    print(response.messages[-1]["content"])
