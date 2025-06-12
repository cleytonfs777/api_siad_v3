import os
import json
import asyncio
import requests
import keyboard
import pyperclip
import subprocess
from time import sleep
from dotenv import load_dotenv
import psutil
from sender_email import send_email
# Adicionando Importação de Recursos para Implementar na Tela
import pexpect
import socket
import re


load_dotenv()  # take environment variables from .env.

url_email = os.getenv('URL_EMAIL')

headers = {'Content-Type': 'application/json'}

usuario =  os.getenv('MYNUMBER')
senha = os.getenv('MYPASS')
caminho_pw3270 = os.getenv('CAMINHO_ARQ')
intervalo_teclas = os.getenv('ITV_TECLAS')
intervalo_teclas = int(intervalo_teclas)
sistema = os.getenv('SYSTEM')
secret_code = os.getenv('SECRETCODE')
url_email = os.getenv('URL_EMAIL')
email_admin = os.getenv('EMAIL_USER_ADMIN')

# Ferramentas de Interação com Terminal Prodemge

# =============================
# Funções do bot
# =============================

def liberar_porta(porta):
    try:
        # Verifica se há algum processo usando a porta
        result = subprocess.run(
            ["lsof", "-t", f"-i:{porta}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        pids = result.stdout.strip().split("\n")

        for pid in pids:
            if pid.strip().isdigit():
                subprocess.run(["kill", "-9", pid.strip()])
                print(f"✔ Processo {pid} finalizado na porta {porta}")

    except Exception as e:
        print(f"Erro ao liberar porta {porta}: {e}")

def iniciar_c3270(host='192.168.2.1', porta=5000):
    liberar_porta(porta)  # 🔪 Libera a porta antes de iniciar
    child = pexpect.spawn(f'c3270 -scriptport {porta} {host}')
    sleep(1)
    return child

def send_command(command, porta=5000):
    with socket.create_connection(('localhost', porta)) as sock:
        sock.sendall((command + '\n').encode())
        result = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            result += data
            if b'ok' in data or b'error' in data:
                break
        return result.decode(errors="ignore")

def get_tela_atual():
    raw = send_command('ReadBuffer(Ascii)')
    hex_data = []
    for line in raw.splitlines():
        if line.startswith("data:"):
            hex_data.extend(re.findall(r'\b[0-9A-Fa-f]{2}\b', line))

    chars = []
    for h in hex_data:
        if h == "00":
            chars.append(" ")
        else:
            char = chr(int(h, 16))
            if 32 <= ord(char) <= 126:
                chars.append(char)
            else:
                chars.append(" ")

    texto = ''.join(chars)
    linhas = [texto[i:i+80].rstrip() for i in range(0, len(texto), 80)]
    return '\n'.join(linhas).strip()

def escrever(texto):
    send_command(f'String("{texto}")')

def tecla(tecla_nome):
    send_command(tecla_nome)

def fechar_c3270(child):
    child.send('\x1b')
    sleep(0.3)
    child.sendline('exit')
    child.expect(pexpect.EOF)

# Fim das Ferramentas de Interação com Terminal Prodemge

def inicia_sistema():

    # Carrega variaveis do sistema
    usuario =  os.getenv('MYNUMBER')
    senha = os.getenv('MYPASS')
    caminho_pw3270 = os.getenv('CAMINHO_ARQ')
    intervalo_teclas = os.getenv('ITV_TECLAS')
    intervalo_teclas = int(intervalo_teclas)
    sistema = os.getenv('SYSTEM')
    secret_code = os.getenv('SECRETCODE')
    url_email = os.getenv('URL_EMAIL')
    email_admin = os.getenv('EMAIL_USER_ADMIN')


    def update_env_variable(key, value, env_file=".env"):
        """Atualiza ou adiciona uma variável no arquivo .env"""
        lines = []
        key_found = False

        # Ler o arquivo .env e modificar a linha correspondente
        if os.path.exists(env_file):
            with open(env_file, "r") as file:
                for line in file:
                    if line.startswith(f"{key}="):  # Se a variável já existe, modifica ela
                        lines.append(f"{key}={value}\n")
                        key_found = True
                    else:
                        lines.append(line)

        # Se a variável não for encontrada, adiciona ao final do arquivo
        if not key_found:
            lines.append(f"{key}={value}\n")

        # Escreve as alterações de volta no .env
        with open(env_file, "w") as file:
            file.writelines(lines)

        # Recarrega as variáveis do .env
        load_dotenv(override=True)

    def enviar_email(mensagem, email):
        assunto = "A senha do useradmin foi resetada com sucesso"
            
        try:
            send_email(mensagem, email, assunto)
            return "Email enviado com sucesso ao useradmin"
            
        except Exception as e:
            return f"Erro: {e}"
        
    def gerar_nova_senha():
        consoantes = list("bcdfghjklmnpqrstvwxyz")
        numeros = list("123456789")
        password = "".join(random.choices(consoantes, k=4)) + "".join(random.choices(numeros, k=4))
        return password

    def digitar_dados(senha):
        sleep(1)  # Garantir que o foco esteja na aplicação correta

        # Sistema a ser acessado
        escrever("cbmmg")
        sleep(intervalo_teclas / 1000)
        tecla("tab")
        sleep(intervalo_teclas / 1000)

        # Insere o usuario
        escrever(usuario)
        sleep(intervalo_teclas / 1000)
        tecla("tab")
        sleep(intervalo_teclas / 1000)

        # Insere a senha
        escrever(senha)
        sleep(intervalo_teclas / 1000)
        tecla("enter")
        sleep(2)

        # Loop de verificação via copiar/colar
        while True:
            # Verifica o conteudo atual da tela
            mensagem1 = get_tela_atual()

            if "Senha expirada" in mensagem1:

                escrever(senha)
                sleep(intervalo_teclas / 1000)
                nova_senha = gerar_nova_senha()

                # Atualiza senha e envia email
                senha = nova_senha
                msg = f"Sua senha de admin foi redefinida para {senha}"
                enviar_email(msg, email_admin)
                update_env_variable("MYPASS", senha)
                
                tecla("Tab")

                escrever(senha)
                sleep(intervalo_teclas / 1000)
                tecla("enter")
                sleep(intervalo_teclas / 1000)

                escrever(senha)
                sleep(intervalo_teclas / 1000)
                tecla("enter")
                sleep(intervalo_teclas / 1000)


            elif "Logon executado com sucesso" in mensagem1:
                print("'Logon executado com sucesso'...foi encontrado na frase selecionada")
                sleep(intervalo_teclas / 1000)
                escrever(sistema)
                sleep(intervalo_teclas / 1000)
                tecla("enter")
                return
            else:
                tecla("enter")
                sleep(intervalo_teclas / 1000)

    # 1. Abre o sistema
    terminal = iniciar_c3270()
    sleep(1)  # Aguardar para garantir que o programa esteja aberto
    digitar_dados(senha)
    print("Finalizada a etapa de iniciar o sistema...")
    return terminal  # ✅ Retorna o terminal vivo

def kill_processes_by_name(keyword):
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            process_name = process.info['name']
            process_pid = process.info['pid']
            if keyword.lower() in process_name.lower():
                print(f"Encerrando processo: {process_name} (PID: {process_pid})")
                psutil.Process(process_pid).terminate()  # Encerra o processo
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Envia email atraves da API        
        
def get_api_key(num_api):
    return f"s{num_api[:-1]}"

def send_key_press(keys, delay=0.1):
    escrever(keys)
    sleep(delay)

def get_screen(message, target):
    return target in message

def initialize_main():

    terminal = inicia_sistema()
    if not terminal:
        print("Falha ao iniciar terminal.")
        return False

    sleep(1)

    # Etapa 2: Enter
    tecla("Enter")
    
    # Etapa 3: 9 TABs
    for _ in range(9):
        tecla("Tab")

    # Etapa 4: escreve "X" e pressiona Enter
    escrever("X")
    
    sleep(intervalo_teclas / 1000)
    
    tecla("Enter")
 
    # Etapa 5: 2 TABs
    for _ in range(2):
        tecla("Tab")

    # Etapa 6: escreve "X" e pressiona Enter
    escrever("X")

    sleep(intervalo_teclas / 1000)
    
    tecla("Enter")

    return terminal

def set_user(user_target):
    print("Iniciando o set de usuario...")
    send_key_press(user_target)
    sleep(0.5)
    tecla("Enter")
    sleep(0.5)
    
    mensagem2 = get_tela_atual()

    if get_screen(mensagem2, "LIBERADO :"):
        return {"status": "OK", "message": "Reset de senha realizado com sucesso. Entre com a senha padrão 'snhrcf' e redefina."}
    else:
        return {"status": "ERROR", "message": "Usuário não cadastrado no sistema. Entre em contato com sua unidade"}

def new_military_registration_full(nummaster):
    
    print(f"Iniciando o reset de senha para o nº: {nummaster}")
    if not nummaster.isdigit():
        print("Não tem número válido...")
        return

    numero = get_api_key(nummaster)
    terminal = initialize_main()
    if not terminal:
        return

    resultfinal = set_user(numero)
    print(f"Numero do usuario {numero}...")
    print(resultfinal["message"])

    # Fecha o sistema para evitar erros
    kill_processes_by_name("w3270")

    
    return True if resultfinal["status"] == "OK" else False


if __name__ == "__main__":

    response_mail = new_military_registration_full('1526607')
    # sleep(1)
    # response_mail = new_military_registration_full('0020123')
    # print("O resultado final é:")
    # print(response_mail)
    # initialize_main()