from google_auth_oauthlib.flow import InstalledAppFlow # Esta clase permite manejar el flujo de autenticación OAuth 2.0 para aplicaciones instaladas.
from google.oauth2.credentials import Credentials # Esta clase representa las credenciales de un usuario autenticado.
from google.auth.transport.requests import Request # Esta clase permite realizar solicitudes HTTP para obtener tokens de acceso.
from googleapiclient.discovery import build # Esta función permite construir un cliente para interactuar con la API de Gmail.
from email.mime.text import MIMEText
import base64
import datetime
import uuid
import os
from ..states.state import Email
SCOPES = ['https://www.googleapis.com/auth/gmail.modify'] # Define el alcance de acceso a la API de Gmail (modificación de correos).

def _get_gmail_service():
    """Obtiene un servicio autenticado de Gmail API."""
    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Si no hay credenciales válidas, solicita al usuario que inicie sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para la próxima ejecución.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def _parser_email_message(message) -> Email:
    """
        Extracts email data from a Gmail API message resource.
        Returns a dict with id, subject, sender, date, and body.
    """
    headers_list = message.get('payload', {}).get('headers', [])
    headers = {header['name'].lower(): header['value'] for header in headers_list}
    subject = headers.get('subject', 'No Subject')
    sender = headers.get('from', 'No Sender')
    date = headers.get('date', 'No Date')
    message_id = headers.get('message-id', '')
    references = headers.get('references', '')
    body = ''
    payload = message.get('payload', {})
    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain':
                body = part.get('body', {}).get('data', '')
                break
    else:
        body = payload.get('body', {}).get('data', '')
    if body:
        try:
            body = base64.urlsafe_b64decode(body).decode('utf-8')
        except Exception:
            body = ''
    return Email(
        id=message['id'],
        subject=subject,
        sender=sender,
        date=date,
        body=body,
        message_id=message_id,
        references=references,
        thread_id=message['threadId']
    )

def get_most_recent_email() -> Email | str:
    """Obtiene el correo electrónico más reciente de la bandeja de entrada."""
    service = _get_gmail_service()
    today = datetime.datetime.now().date()
    query = f'after:{today.strftime("%Y/%m/%d")}' # after:YYYY/MM/DD
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
        email_messages = results.get('messages', [])[0]
        if not email_messages:
            return None
        message = service.users().messages().get(userId='me', id=email_messages['id']).execute()
        return _parser_email_message(message)
    except Exception as e:
        print(f'Error retrieving email: {e}')
        return None

def send_reply_email(original_email: Email, reply_email: Email) -> bool:
    """
    Send a reply email to the original sender that will appear as a threaded reply.
    """
    try:
        service = _get_gmail_service()

        sender_email = original_email.sender # Micorreo <micorreo@gmail.com>
        if '<' in sender_email and '>' in sender_email:
            sender_email = sender_email.split('<')[1].split('>')[0]

        print(f"Reply will be sent to: {sender_email}")

        reply_subject = reply_email.subject
        original_subject = original_email.subject
        if original_subject.startswith('Re:'):
            reply_subject = original_subject
        else:
            reply_subject = f"Re: {original_subject}" # Re: no me gustan tus productos

        message_id = original_email.message_id
        references = original_email.references
        thread_id = original_email.thread_id

        if not message_id:
            message_id = f"<{original_email.id}@gmail.com>"

        message = _create_reply_message_with_thread(
            to=sender_email,
            subject=reply_subject,
            message_text=reply_email.body,
            original_message_id=message_id,
            original_references=references,
            thread_id=thread_id
        )

        sent_message = service.users().messages().send(userId='me', body=message).execute()

        print(f"Threaded reply email sent successfully. Message ID: {sent_message['id']}")
        return True

    except Exception as error:
        print(f'An error occurred while sending reply email: {error}')
        return False

def _create_reply_message_with_thread(to: str, subject: str, message_text: str, original_message_id: str, original_references: str, thread_id: str) -> dict:
    """
    Create a reply message that will appear as a threaded reply with proper thread ID.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject

    if original_message_id:
        message['In-Reply-To'] = original_message_id
        if original_references:
            references = f"{original_references} {original_message_id}".strip()
        else:
            references = original_message_id
        message['References'] = references

        message['Message-ID'] = f"<{uuid.uuid4()}@gmail.com>"

    body = {
        'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    }

    if thread_id:
        body['threadId'] = thread_id
    return body