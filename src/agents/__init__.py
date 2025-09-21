from .email_categorizer import categorize_email
from .email_writer import query_or_email, write_email_with_context

AGENTS_REGISTRY = {
    "categorize_email": categorize_email(),
    "query_or_email": query_or_email(),
    "write_email_with_context": write_email_with_context()
}