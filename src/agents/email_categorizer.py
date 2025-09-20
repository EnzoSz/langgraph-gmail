from ..prompts import EMAIL_CATEGORIZER_PROMPT
from ..structured_outputs import CategorizerEmailOutput
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de entorno desde el archivo .env

def categorize_email():
    email_categorizer_prompt = PromptTemplate(
        input_variables=["email"],
        template=EMAIL_CATEGORIZER_PROMPT
    )
    
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        temperature=0,
    )
    return email_categorizer_prompt | llm.with_structured_output(CategorizerEmailOutput)