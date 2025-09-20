from src.graph.email_graph import EmailSupportGraph
from src.states.state import Email

def main():
    print("Starting Email Support Graph...")
    initial_state = {
        'customer_email': {
            'id': '',
            'subject': '',
            'body': '',
            'sender': '',
            'date': '',
            'body': ''
        },
        'email_category': ''
    }
    
    workflow = EmailSupportGraph()
    graph = workflow.graph
    
    for output in graph.stream(initial_state):
        for _, value in output.items():
            current_email = value.get('current_email', {})
            if isinstance(current_email, Email):
                print(current_email.body)
                print(value.get('email_category', ''))

if __name__ == "__main__":
    main()
