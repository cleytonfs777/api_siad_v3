import subprocess
import time
import keyboard
import os
from time import sleep

def escrev(lista):
    for c in lista:
        keyboard.press(c)
        keyboard.release(c)
        sleep(0.05)

def abrir_arquivo(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        subprocess.Popen(caminho_arquivo, shell=True)
        print(f"Arquivo aberto com sucesso: {caminho_arquivo}")
    else:
        print("Erro: O arquivo especificado não foi encontrado.")

caminho_pw3270 = "C:\\Program Files (x86)\\pw3270\\pw3270.exe"
abrir_arquivo(caminho_pw3270)

sleep(1)
escrev("cbmmg")
sleep(0.2)
keyboard.send('tab')
sleep(0.2)
escrev("s142924")
sleep(0.2)
keyboard.send('tab')
sleep(0.2)
escrev("zxcv2025")
sleep(0.2)
keyboard.send('enter')
sleep(0.2)
escrev("losg")
sleep(0.2)
keyboard.send('enter')