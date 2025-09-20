import os
from dotenv import load_dotenv
load_dotenv()  # Carga las variables de entorno desde el archivo .env

# Configuración de LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "langgraph-gmail")
if os.getenv("LANGSMITH_WORKSPACE_ID"):
    os.environ["LANGCHAIN_WORKSPACE_ID"] = os.getenv("LANGSMITH_WORKSPACE_ID")