import os
import redis
import json
import logging
from time import sleep
from sender_email import send_email_teste
from contextlib import contextmanager

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Conectar ao Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


def processing_key(number: str) -> str:
    """
    Gera a chave de bloqueio de processamento para o Redis.
    """
    return f"processing:{number}"


@contextmanager
def processing_lock(number: str):
    """
    Gerenciador de contexto para garantir que o bloqueio seja removido mesmo em caso de erro
    """
    try:
        yield
    finally:
        try:
            redis_client.delete(processing_key(number))
            logging.info(f"Chave de processamento removida para {number}")
        except Exception as e:
            logging.error(f"Erro ao remover chave de processamento para {number}: {e}")


def cadastrar_militar(number: str, email: str) -> bool:
    """
    Simula o cadastro de um militar.
    """
    try:
        sleep(10)  # Simula o tempo de cadastro
        logging.info(f"Militar {number} cadastrado com sucesso.")
        logging.info(f"Confirmação encaminhada para o email: {email}")
        return True
    except Exception as e:
        logging.error(f"Erro ao cadastrar militar {number}: {e}")
        return False

def send_email_with_retry(message_body: str, email_to: str, retries: int = 3) -> str:
    """
    Envia um e-mail com política de tentativas.
    """
    attempt = 0
    while attempt < retries:
        try:
            status = send_email_teste(message_body, email_to)
            if "Erro" not in status:
                return status
            logging.warning(f"Tentativa {attempt + 1} de envio falhou para {email_to}: {status}")
        except Exception as e:
            logging.error(f"Erro na tentativa {attempt + 1} de envio para {email_to}: {e}")
        attempt += 1
        if attempt < retries:
            sleep(2)  # Espera antes da nova tentativa
    return f"Erro: todas as {retries} tentativas de envio falharam."

def process_request(request_data: dict):
    """
    Processa a requisição e envia um e-mail ao usuário.
    """
    number = request_data["number"]
    email_to = request_data["email"]

    with processing_lock(number):
        # ✅ Cadastrar o militar
        resultado = cadastrar_militar(number, email_to)

        if resultado:
            message_body = """
            <html>
            <body>
                <p style="font-weight:bold; font-size:16px;">Senha do sistema PRODEMGE resetada com sucesso. Sua senha padrão será:</p>
                <p style="color:blue; font-weight:bold; font-size:22px;">SNHRCF</p>
                <p style="font-weight:bold; font-size:16px;">Para a sua segurança crie uma nova senha</p>
            </body>
            </html>
            """
        else:
            message_body = """
            <html>
            <body>
                <p style="font-weight:bold; font-size:16px;">Cadastro não localizado no sistema. Entre em contato com o administrador.</p>
            </body>
            </html>
            """

        # ✅ Enviar e-mail com retry
        email_status = send_email_with_retry(message_body, email_to)

        if "Erro" in email_status:
            logging.error(f"Erro ao enviar e-mail para {email_to}. Solicite ao usuário que entre em contato com o administrador.")
        else:
            logging.info(f"E-mail enviado com sucesso para {email_to}.")

def run_worker():
    """
    Mantém o worker escutando a fila no Redis.
    """
    logging.info("Worker iniciado, aguardando requisições...")

    while True:
        try:
            # Aguarda uma nova tarefa na fila
            task = redis_client.brpop("queue", timeout=60)
            if task:
                try:
                    request_data = json.loads(task[1])
                    logging.info(f"Processando requisição: {request_data}")
                    process_request(request_data)
                except json.JSONDecodeError as e:
                    logging.error(f"Erro ao decodificar JSON da tarefa: {e}")
                except Exception as e:
                    logging.exception(f"Erro ao processar a tarefa: {e}")
        except redis.RedisError as e:
            logging.error(f"Erro de conexão com Redis: {e}")
            sleep(5)  # Espera um pouco antes de tentar novamente
        except Exception as e:
            logging.exception(f"Erro inesperado: {e}")
            sleep(5)

if __name__ == "__main__":
    run_worker()
