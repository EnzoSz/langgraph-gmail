from google_auth_oauthlib.flow import InstalledAppFlow # Esta clase permite manejar el flujo de autenticación OAuth 2.0 para aplicaciones instaladas.
from google.oauth2.credentials import Credentials # Esta clase representa las credenciales de un usuario autenticado.
from google.auth.transport.requests import Request # Esta clase permite realizar solicitudes HTTP para obtener tokens de acceso.
from googleapiclient.discovery import build # Esta función permite construir un cliente para interactuar con la API de Gmail.
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
        body=body
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
