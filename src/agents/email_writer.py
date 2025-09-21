from ..utils.rag_utils import get_retriever_tool
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from ..prompts import EMAIL_WRITER_PROMPT
from ..states.state import Email
from dotenv import load_dotenv
import os
load_dotenv()  # Carga las variables de entorno desde el archivo .env


def _create_email_writer_chain(use_rag:bool, use_structured_output:bool):
    """Crea una cadena de escritura de emails con o sin RAG y con o sin salida estructurada."""
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        temperature=0,
    )
    if use_rag:
        llm = llm.bind_tools([get_retriever_tool()])

    email_writer_prompt_template = PromptTemplate(
        template=EMAIL_WRITER_PROMPT,
        input_variables=["email_content", "email_category", "context"]
    )
    email_writer_chain = email_writer_prompt_template | llm
    if use_structured_output:
        email_writer_chain = email_writer_prompt_template | llm.with_structured_output(Email)
    return email_writer_chain

def query_or_email():
    """Crea una cadena de escritura de emails que usa RAG pero no salida estructurada."""
    return _create_email_writer_chain(use_rag=True, use_structured_output=False)

def write_email_with_context():
    """Crea una cadena de escritura de emails que usa RAG y salida estructurada."""
    return _create_email_writer_chain(use_rag=True, use_structured_output=True)