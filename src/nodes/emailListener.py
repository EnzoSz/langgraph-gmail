from ..states.state import GraphState
from ..utils.gmailUtils import get_most_recent_email

def email_listener_node(state: GraphState):
    """
    Nodo que escucha el correo electrónico más reciente y actualiza el estado.
    """
    email_data = get_most_recent_email()
    state['current_email'] = email_data
    return state