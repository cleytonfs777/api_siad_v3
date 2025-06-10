import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

def gmail_authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        print("Token carregado com sucesso.")
    else:
        print("Nenhum token encontrado, iniciando autenticação...")

    try:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Token expirado, renovando automaticamente...")
                creds.refresh(Request())
            else:
                print("Iniciando novo fluxo de autenticação...")
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            # Salva o token atualizado ou novo
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
                print("Token salvo com sucesso.")
    except Exception as e:
        print(f"Erro na autenticação: {e}")
        raise e

    return build('gmail', 'v1', credentials=creds)

def send_email(service, to, subject, body):
    message = EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['From'] = os.getenv("EMAILAPP")
    message['Subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }

    try:
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f"Email enviado! ID da mensagem: {send_message['id']}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        
def send_email_full(email, type="success"):
    service = gmail_authenticate()
    msg_success = """
        <html>
        <body>
            <p style="font-weight:bold; font-size:16px;">Senha do sistema PRODEMGE resetada com sucesso. Sua senha padrão será:</p>
            <p style="color:blue; font-weight:bold; font-size:22px;">SNHRCF</p>
            <p style="font-weight:bold; font-size:16px;">Para a sua segurança crie uma nova senha</p>
        </body>
        </html>
        """
    msg_error = """
        <html>
        <body>
            <p style="font-weight:bold; font-size:16px;">Cadastro não localizado no sistema. Entre em contato com o administrador.</p>
        </body>
        </html>
        """
    send_email()


def send_email_teste(msg_body, e_to):
    return True

if __name__ == '__main__':
    service = gmail_authenticate()
    email_to = input('Digite o email do destinatário: ')
    subject = input('Digite o assunto: ')
    message_body = input('Digite a mensagem: ')

    send_email(service, email_to, subject, message_body)
