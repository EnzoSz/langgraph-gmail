from ..states.state import GraphState, Email
from ..utils.gmailUtils import send_reply_email
def email_sender_node(state: GraphState):
    """
    Nodo que envía el email generado al destinatario.
    """
    current_email = state['current_email']
    reply_email = state['email_response']
    
    if isinstance(current_email, Email) and isinstance(reply_email, Email):
        send_reply_email(current_email, reply_email)
    return state