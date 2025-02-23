# ai_motors/config/model_config.py
import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM

load_dotenv()

MODEL_NAME = "ollama/llama2-uncensored"  # Usa el nombre con el prefijo "ollama/"
VERBOSE = True
API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

def get_model():
    return "ollama/nichonauta/pepita-2-2b-it-v5"  
