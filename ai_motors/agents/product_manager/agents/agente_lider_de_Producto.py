# ai_motors\agents\product_manager\agents\agente_lider_de_Producto.py
from swarm import Agent, Swarm
from openai import OpenAI

# Configuración del cliente usando el servidor Ollama local
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",  # URL del servidor local de Ollama
    api_key="ollama"                       # La API key es requerida, pero no se usa realmente
)
client = Swarm(ollama_client)

def instrucciones_lider_de_producto(context_variables):
    """
    Eres un agente Líder de Producto / Product Manager.

    Tu tarea es recibir el requerimiento del cliente (contenido en el prompt) y generar un informe final sellado que contenga:
      - Resumen Ejecutivo: Una descripción concisa de la visión general del proyecto.
      - Objetivos: Una lista de objetivos específicos y medibles.
      - Alcance: Definición clara de lo que se incluye y lo que se excluye en el proyecto.
      - Restricciones: Limitaciones tecnológicas y operativas (Solo usar HTML, CSS y JavaScript).

    Debes ser ultradetallado y estructurar el informe de manera profesional y coherente.
    No simules una conversación ni intentes agendar reuniones; utiliza exclusivamente el requerimiento proporcionado para elaborar el informe final.
    """
    return instrucciones_lider_de_producto.__doc__

# Definición del agente Líder de Producto
agente_lider_de_producto = Agent(
    model="qwen2.5-coder:14b",
    name="Agente Líder de Producto",
    instructions=instrucciones_lider_de_producto
)


def corrector_instrucciones_lider_de_producto(context_variables):
    documento_anterior = context_variables.get("documento_anterior", "")
    return f"""
    Eres un agente Líder de Producto / Product Manager.

    Tu tarea era recibir el requerimiento del cliente (contenido en el prompt) y generar un informe final sellado que contenga:
    - Resumen Ejecutivo: Una descripción concisa de la visión general del proyecto.
    - Objetivos: Una lista de objetivos específicos y medibles.
    - Alcance: Definición clara de lo que se incluye y lo que se excluye en el proyecto.
    - Restricciones: Limitaciones tecnológicas y operativas (Solo usar HTML, CSS y JavaScript).

    Tu informe ha sido revisado por control de calidad y se han detectado errores que debes corregir:
    -----------------------
    Documento anterior:
    {documento_anterior}
    -----------------------

    Escribe un informe final completo que contenga los elementos solicitados y que corrija los errores encontrados.
    """


# Definicion del agente corrector Lider de producto
corrector_documento_lider = Agent(
    model="qwen2.5-coder:14b",
    name="Agente Corrector Líder de Producto",
    instructions=corrector_instrucciones_lider_de_producto
)








if __name__ == "__main__":
    # Ejemplo de requerimiento del cliente
    prompt = (
        "El cliente solicita una plataforma web juntar dinero para un robot que quiere ser presidente. "
        "Se debera juntar dinero para su campaña. "
        "Se requiere un diseño moderno y atractivo, con una interfaz intuitiva y fácil de usar. "
        "El ademas debera contener todas la paginas necesarias para la campaña politica un robot que quiere ser presidente del mundo. "
        "El cliente solicita que el proyecto se realice utilizando HTML, CSS y JavaScript."
        "El robot es argentino pero quiere conquistar el mundo."
    )
    response = client.run(
        agent=agente_lider_de_producto,
        messages=[{"role": "user", "content": prompt}],
        context_variables={}
    )
    print(response.messages[-1]["content"])
