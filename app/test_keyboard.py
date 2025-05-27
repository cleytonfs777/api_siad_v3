import subprocess
import time
import keyboard

# Passo 1: Abrir o Bloco de Notas
subprocess.Popen('notepad.exe')

# Passo 2: Aguardar o Bloco de Notas abrir
time.sleep(2)

# Passo 3: Escrever um texto
keyboard.write("Olá! Isso é uma automação usando a biblioteca keyboard.\n")
keyboard.write("Funciona sem precisar de interface gráfica complexa.\n")

# Passo 4: Enviar uma combinação de teclas (opcional)
keyboard.send('ctrl+s')  # Simula o comando de salvar
