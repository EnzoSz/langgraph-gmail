from langgraph.graph import START, StateGraph
from ..nodes import NODES
from ..states.state import GraphState

class EmailSupportGraph:
    """
    Grafo que escucha el correo más reciente y lo categoriza.
    """
    def __init__(self):
        workflow = StateGraph(GraphState)
        workflow.add_node('load_email', NODES['email_listener'])
        workflow.add_node('categorize_email', NODES['email_categorizer'])
        workflow.add_edge(START, 'load_email')
        workflow.add_edge('load_email', 'categorize_email')
        
        self.graph = workflow.compile()