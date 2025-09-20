from ..agents import AGENTS_REGISTRY
from ..states.state import GraphState, Email

def email_categorizer_node(state: GraphState):
    """
    Nodo que categoriza el email actual usando el agente categorizador de emails.
    """
    body = ""
    email = state.get('current_email')
    if not email:
        state['email_category'] = "No email"
        return state
    if isinstance(email, Email):
        body = email.body
    result = AGENTS_REGISTRY["categorize_email"].invoke({"email": body})
    state['email_category'] = result.category.value
    return state