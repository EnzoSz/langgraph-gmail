from .emailCategorizer import email_categorizer_node
from .emailListener import email_listener_node
from .email_writer import email_writer_with_context_node, query_or_email_node
from .email_sender import email_sender_node
NODES={
    "email_listener": email_listener_node,
    "email_categorizer": email_categorizer_node,
    "email_writer_with_context": email_writer_with_context_node,
    "query_or_email": query_or_email_node,
    "email_sender": email_sender_node
}