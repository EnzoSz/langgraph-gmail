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
        'email_category': '',
        'email_response': '',
        'messages': [""]
    }
    
    workflow = EmailSupportGraph()
    graph = workflow.graph
    
    for output in graph.stream(initial_state):
        for node, state in output.items():
            print(f"Node: \n {node}")
            print(f"State: \n {state}\n")
            

if __name__ == "__main__":
    main()
