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

load_dotenv()  # take environment variables from .env.

url_email = os.getenv('URL_EMAIL')

headers = {'Content-Type': 'application/json'}

SISTEMA = os.getenv('SYSTEM')


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
            
        try:

            headers = {'Content-Type': 'application/json'}

            response_body = {
            "token": secret_code,
            "email": email,
            "message":mensagem
            }

            requests.post(url_email, headers=headers,
                        data=json.dumps(response_body))
            return "Email enviado com sucesso para {}"
        except Exception as e:
            return f"Erro: {e}"
        


    def abrir_arquivo(caminho_arquivo):
        if os.path.exists(caminho_arquivo):
            subprocess.Popen(caminho_arquivo, shell=True)
            print(f"Arquivo aberto com sucesso: {caminho_arquivo}")
        else:
            print("Erro: O arquivo especificado não foi encontrado.")

    def gerar_nova_senha():
        consoantes = list("bcdfghjklmnpqrstvwxyz")
        numeros = list("123456789")
        password = "".join(random.choices(consoantes, k=4)) + "".join(random.choices(numeros, k=4))
        return password

    def digitar_dados(senha):
        sleep(1)  # Garantir que o foco esteja na aplicação correta

        # Sistema a ser acessado
        escrev("cbmmg")
        sleep(intervalo_teclas / 1000)
        keyboard.send("tab")
        sleep(intervalo_teclas / 1000)

        # Insere o usuario
        escrev(usuario)
        sleep(intervalo_teclas / 1000)
        keyboard.send("tab")
        sleep(intervalo_teclas / 1000)

        # Insere a senha
        escrev(senha)
        sleep(intervalo_teclas / 1000)
        keyboard.send("enter")
        sleep(2)

        # Loop de verificação via copiar/colar
        while True:
            keyboard.send("ctrl+a")
            sleep(0.5)
            keyboard.send("ctrl+c")
            sleep(0.5)
            keyboard.send("esc")
            mensagem1 = pyperclip.paste()

            if "Senha expirada" in mensagem1:
                print(f"A senha atual é: {senha}")

                escrev(senha)
                sleep(intervalo_teclas / 1000)
                nova_senha = gerar_nova_senha()

                # Atualiza senha e envia email
                senha = nova_senha
                msg = f"Sua senha de admin foi redefinida para {senha}"
                enviar_email(msg, email_admin)
                update_env_variable("MYPASS", senha)

                escrev(senha)
                sleep(intervalo_teclas / 1000)
                keyboard.send("enter")
                sleep(intervalo_teclas / 1000)

                escrev(senha)
                sleep(intervalo_teclas / 1000)
                keyboard.send("enter")
                sleep(intervalo_teclas / 1000)

                print(f"A nova senha é: {senha}")

            elif "Logon executado com sucesso" in mensagem1:
                escrev(sistema)
                sleep(intervalo_teclas / 1000)
                keyboard.send("enter")
                break
            else:
                keyboard.send("enter")
                sleep(intervalo_teclas / 1000)


    abrir_arquivo(caminho_pw3270)
    sleep(3)  # Aguardar para garantir que o programa esteja aberto
    digitar_dados(senha)

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

def escrev(lista, interv=0.05):
    for c in lista:
        keyboard.press(c)
        keyboard.release(c)
        sleep(interv)
        
        
def get_api_key(num_api):
    return f"s{num_api[:-1]}"


def send_key_press(keys, delay=0.1):
    escrev(keys)
    sleep(delay)

def get_screen(message, target):
    return target in message


def initialize_main():
    try:
        inicia_sistema()
        sleep(1)
        keyboard.send('enter')
        for _ in range(9):
            send_key_press("\t")
        send_key_press("X\n")
        for _ in range(2):
            send_key_press("\t")
        send_key_press("X\n")
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False


def set_user(user_target):
    send_key_press(user_target + "\n")
    sleep(0.5)
    keyboard.send('ctrl+a')
    sleep(0.5)
    keyboard.send('ctrl+c')

    sleep(0.5)
    mensagem2 = pyperclip.paste()

    if get_screen(mensagem2, "LIBERADO :"):
        return {"status": "OK", "message": "Reset de senha realizado com sucesso. Entre com a senha padrão 'snhrcf' e redefina."}
    else:
        return {"status": "ERROR", "message": "Usuário não cadastrado no sistema. Entre em contato com sua unidade"}


def new_military_registration_full(nummaster):
    if not nummaster.isdigit():
        print("Não tem número válido...")
        return

    numero = get_api_key(nummaster)
    if not initialize_main():
        return

    resultfinal = set_user(numero)
    print(f"Numero do usuario {numero}...")
    print(resultfinal["message"])

    # Fecha o sistema para evitar erros
    kill_processes_by_name("w3270")

    
    return True if resultfinal["status"] == "OK" else False



if __name__ == "__main__":

    response_mail = new_military_registration_full('1526607')
    sleep(1)
    response_mail = new_military_registration_full('0020123')
    # print("O resultado final é:")
    # print(response_mail)
    # initialize_main()