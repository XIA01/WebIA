from swarm import Agent, Swarm
from openai import OpenAI
import subprocess
import os
from colorama import init, Fore, Style

init(autoreset=True)

# Configuración del cliente
ollama_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
client = Swarm(ollama_client)

def ejecutar_comando_powershell(comando: str) -> str:
    """
    Ejecuta el comando indicado y luego lista el contenido del directorio actual.
    Además, verifica (según lo esperado) la existencia de elementos.
    Devuelve un string que incluye:
      - El comando ejecutado.
      - La salida (stdout o stderr) del comando.
      - El contenido del directorio (usando 'dir' en Windows o 'ls -la' en Unix).
    """
    print(Fore.CYAN + "Ejecutando comando:", comando)
    try:
        # Si estamos en Windows usamos cmd con la opción /C
        if os.name == "nt":
            resultado = subprocess.run(
                ["cmd", "/C", comando],
                capture_output=True,
                text=True
            )
        else:
            resultado = subprocess.run(
                comando, shell=True, capture_output=True, text=True
            )
        print(Fore.YELLOW + "Código de retorno:", resultado.returncode)
        if resultado.stdout:
            print(Fore.YELLOW + "Salida estándar:", resultado.stdout)
        if resultado.stderr:
            print(Fore.YELLOW + "Error estándar:", resultado.stderr)
        output = resultado.stdout.strip() if resultado.stdout else resultado.stderr.strip()
        
        # Listamos el contenido del directorio actual
        list_cmd = "dir" if os.name == "nt" else "ls -la"
        resultado_ls = subprocess.run(list_cmd, shell=True, capture_output=True, text=True)
        ls_output = resultado_ls.stdout.strip() if resultado_ls.stdout else resultado_ls.stderr.strip()
        print(Fore.MAGENTA + "Contenido del directorio tras ejecución:")
        print(ls_output)
        
        return (
            f"Comando ejecutado: {comando}\n"
            f"Salida del comando:\n{output}\n\n"
            f"Contenido del directorio:\n{ls_output}\n"
        )
    except Exception as e:
        print(Fore.RED + "Excepción al ejecutar el comando:", str(e))
        return f"Error al ejecutar el comando: {str(e)}"

def instrucciones_ejecucion(context_variables):
    return """
Eres un Agente de Ejecución de Comando para Windows. Tu misión es convertir una orden natural a un comando CMD válido, 
ejecutarlo y devolver únicamente el log de la ejecución.
Llama a tu función ejecutar_comando_powershell y devuelve el log resultante.
"""

ejecutor = Agent(
    model="qwen2.5-coder:14b",
    name="Agente de Ejecución de Comando",
    instructions=instrucciones_ejecucion,
    functions=[ejecutar_comando_powershell]
)

if __name__ == "__main__":
    # Ejemplo: en Windows se usa cmd con /C para ejecutar el comando.
    # La orden natural se envía en el mensaje del usuario y aquí usamos un comando de ejemplo.
    # Este comando creará una carpeta "IA" y un archivo "IA\index.html" con contenido básico.
    if os.name == "nt":
        comando = (
            "mkdir IA && type nul > IA\\index.html && echo ^<!DOCTYPE html^>^<html lang=\"es\"^>^<head^>^<meta charset=\"UTF-8\"^>^<title^>Página Básica^</title^>^</head^>^<body^>^<h1^>¡Hola, Mundo!^</h1^>^</body^>^</html^> >> IA\\index.html"
        )
    else:
        comando = "mkdir -p IA && touch IA/index.html && echo '<!DOCTYPE html><html lang=\"es\"><head><meta charset=\"UTF-8\"><title>Página Básica</title></head><body><h1>¡Hola, Mundo!</h1></body></html>' > IA/index.html"
        
    response = client.run(
        agent=ejecutor,
        messages=[{"role": "user", "content": f"{comando}"}],
        context_variables={}
    )
    print(Style.BRIGHT + "\nLog de Ejecución:")
    print(response.messages[-1]["content"])
