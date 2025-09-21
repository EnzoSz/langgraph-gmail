from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from ..utils.rag_utils import get_retriever_tool
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
        workflow.add_node('query_or_email', NODES['query_or_email'])
        workflow.add_node('retrieve', ToolNode([get_retriever_tool()]))
        workflow.add_node('email_writer_with_context', NODES['email_writer_with_context'])
        workflow.add_node('email_sender', NODES['email_sender'])
        
        workflow.add_edge(START, 'load_email')
        workflow.add_edge('load_email', 'categorize_email')
        workflow.add_edge('categorize_email', 'query_or_email')
        workflow.add_conditional_edges(
            "query_or_email",
            tools_condition,
            {
                "tools": 'retrieve',
                END: "email_writer_with_context"
            }
        )
        workflow.add_edge('retrieve', 'email_writer_with_context')
        workflow.add_edge('email_writer_with_context', 'email_sender')
        workflow.add_edge('email_sender', END)
        
        self.graph = workflow.compile()