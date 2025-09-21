from ..agents import AGENTS_REGISTRY
from ..states.state import GraphState, Email

def _get_email_data(state: GraphState):
    """
    Función auxiliar para obtener el cuerpo y la categoría del email actual.
    """
    current_email = state.get('current_email')
    category = state.get('email_category')
    
    if not current_email or not category:
        print("No hay email actual o categoría en el estado.")
        return "", "No email"

    body = current_email.body if isinstance(current_email, Email) else ""
    return body, category

def _process_email_writer_result(state: GraphState, result):
    """
    Función auxiliar para procesar el resultado del agente escritor de emails y actualizar el estado.
    """
    # Solo agregar el resultado a messages si es un mensaje válido, no reemplazar toda la lista
    if hasattr(result, 'content'):
        # Si result es un mensaje, agregarlo a la lista existente
        current_messages = state.get('messages', [])
        current_messages.append(result)
        state['messages'] = current_messages
    
    state['email_response'] = result
    return state

def query_or_email_node(state: GraphState):
    """
    Nodo que genera una respuesta al email actual usando el agente escritor de emails sin salida estructurada.
    """
    email_data = _get_email_data(state)
    if not email_data[0]:
        state['email_response'] = ""
        return state
        
    body, category = email_data
    result = AGENTS_REGISTRY["query_or_email"].invoke({"email_content": body, "email_category": category, "context": ""})
    return _process_email_writer_result(state, result)

def email_writer_with_context_node(state: GraphState):
    """
    Nodo que genera una respuesta al email actual usando el agente escritor de emails con salida estructurada.
    """
    email_data = _get_email_data(state)
    if not email_data[0]:
        state['email_response'] = ""
        return state
        
    body, category = email_data
    context = state.get('messages')[-1].content if state.get('messages') else ""
    result = AGENTS_REGISTRY["write_email_with_context"].invoke({"email_content": body, "email_category": category, "context": context})
    state['email_response'] = result
    return state