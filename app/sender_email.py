import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_email(message_body, email_to, assunto='Sua solicitação de Recuperação foi processada!!'):
    email = os.getenv("EMAILAPP")
    password = os.getenv("SENHAAPP")

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = email
    msg['To'] = email_to
    msg.set_content("Seu e-mail não suporta HTML. Por favor, habilite a exibição de conteúdo HTML.")  # Backup para clientes sem HTML
    msg.add_alternative(message_body, subtype="html")  # ✅ Agora o e-mail suporta HTML

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
            return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

def send_email_full(email, type="success"):
    
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
    if type == 'success':
        send_email(msg_success, email)
    else:
        send_email(msg_error, email)


def send_email_teste(msg_body, e_to):
    return True

if __name__ == '__main__':
    # send_email_full("cleyton.fs777@gmail.com")
    send_email("Teste de Body para a aplicação", "cleytoncbmmg@gmail.com", "Novo assunto para realização de teste")