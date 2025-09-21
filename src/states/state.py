from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class Email(BaseModel):
    id: str = Field(..., description="El identificador único del correo electrónico.")
    subject: str = Field(..., description="El asunto del correo electrónico.")
    sender: str = Field(..., description="La dirección de correo electrónico del remitente.")
    date: str = Field(..., description="La fecha en que se envió el correo electrónico.")
    body: str = Field(..., description="El contenido del cuerpo del correo electrónico.")
    message_id: str = Field(..., description="El ID del mensaje para hilos de correo electrónico.")
    references: str = Field(..., description="Las referencias del correo electrónico para hilos.")
    thread_id: str = Field(..., description="El ID del hilo del correo electrónico.")
    
class GraphState(TypedDict):
    current_email: Email | str
    email_category: str
    email_response: Email | str
    messages: Annotated[list[AnyMessage], add_messages]
    