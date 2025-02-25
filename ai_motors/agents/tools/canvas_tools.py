from swarm import Agent, Swarm
from openai import OpenAI
# Configuración del cliente usando tu servidor Ollama local
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",  # URL del servidor local de Ollama
    api_key="ollama"                      # La API key es requerida, pero no se usa realmente
)
client = Swarm(ollama_client)

import psutil
import GPUtil

def get_system_info() -> dict:
    """
    Obtiene la RAM total (en GB), el nombre de la primera GPU detectada y su VRAM total (en GB).
    Si no se detecta ninguna GPU, se retorna 'No GPU detected' y 0 GB de VRAM.
    """
    # Obtener RAM total en GB
    ram_bytes = psutil.virtual_memory().total
    ram_gb = ram_bytes / (1024 ** 3)
    
    # Obtener información de la GPU (usando GPUtil)
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]
        gpu_name = gpu.name
        # memoryTotal está en MB, convertimos a GB
        vram_gb = gpu.memoryTotal / 1024
    else:
        gpu_name = "No GPU detected"
        vram_gb = 0.0

    return {"RAM": ram_gb, "GPU": gpu_name, "VRAM": vram_gb}
ram, gpu, vram = get_system_info().values()

def instrucciones(context_variables):
    print(context_variables)
    # Extraemos las variables de contexto
    name = context_variables.get("name", "Usuario")
    ram = context_variables.get("ram", 0)
    gpu = context_variables.get("gpu", "No GPU detected")
    vram = context_variables.get("vram", 0)
    
    return f"""Saluda a {name}. Eres un agente analista de sistema.
Recibes las siguientes variables de contexto:
- Nombre del usuario: {name}
- RAM: {ram:.2f} GB
- GPU: {gpu}
- VRAM: {vram:.2f} GB

Tu tarea es:
1. Saludar al usuario usando su nombre.
2. Informar la configuración actual de su sistema (RAM, GPU, VRAM).
3. Evaluar si el sistema cumple con los requisitos mínimos (al menos 16 GB de RAM y 6 GB de VRAM).
4. Si se cumplen, indica que el sistema es adecuado; de lo contrario, especifica qué componente no cumple y sugiere mejoras.

Devuelve un mensaje final que combine esta información."""


saludador = Agent(
    model="qwen2.5-coder:14b",  # Utiliza tu modelo de 14B
    name="Agente analista de sistema",
    instructions=instrucciones
)


