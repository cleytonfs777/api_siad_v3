import pexpect
import socket
import time
import re
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Carrega variaveis do sistema
usuario =  os.getenv('MYNUMBER')
senha = os.getenv('MYPASS')
# =============================
# Funções do bot
# =============================

def iniciar_c3270(host='192.168.2.1', porta=5000):
    child = pexpect.spawn(f'c3270 -scriptport {porta} {host}')
    time.sleep(1)
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
    time.sleep(0.3)
    child.sendline('exit')
    child.expect(pexpect.EOF)

# =============================
# Execução do bot
# =============================

if __name__ == "__main__":
    # 1. Abre o sistema
    terminal = iniciar_c3270()

    # 2. Digita "cbmmg"
    escrever("cbmmg")
    
    # 3. Pressiona Tab
    tecla("tab")

    # 3.1  Digita "s142924"
    escrever(usuario)
    
    # 3. Pressiona Tab
    tecla("tab")

    # 3.1  Digita "s142924"
    escrever(senha)
    
    # 3. Pressiona Tab
    tecla("Enter")
    
    time.sleep(1)
    
    escrever("losg")
    
    time.sleep(1)
    
    # 3. Pressiona Tab
    tecla("Enter")
    
    time.sleep(1)
    
    conteudo_1 = get_tela_atual()
    
    # 4. Aguarda a próxima tela carregar
    time.sleep(1)


    # 6. Fecha o terminal
    fechar_c3270(terminal)

    # 7. Mostra resultado
    print("==== CONTEÚDO DA TELA APÓS LOGIN ====")

    print(conteudo_1)
