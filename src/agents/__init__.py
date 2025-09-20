from .email_categorizer import categorize_email

AGENTS_REGISTRY = {
    "categorize_email": categorize_email()
}