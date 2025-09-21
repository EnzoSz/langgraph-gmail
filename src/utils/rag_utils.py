from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from dotenv import load_dotenv
import os
load_dotenv()  # Carga las variables de entorno desde el archivo .env

loader = TextLoader("src/data/data.txt", encoding="utf-8")

documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

docs_split = text_splitter.split_documents(documents)

embedding = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION_EMBEDDING"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)
vectorstore = Chroma.from_documents(
    documents=docs_split,
    embedding=embedding,
    persist_directory="./chroma_db",
)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="recuperar_informacion_productos_servicios",
    description="Útil para responder preguntas sobre los productos y servicios que ofrece la empresa."
)

def get_retriever_tool():
    return retriever_tool