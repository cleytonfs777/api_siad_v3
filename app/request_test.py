import requests
import time
from dotenv import load_dotenv
import os

# ✅ Carregar variáveis do arquivo .env
load_dotenv()

# ✅ Obtém o SECRET_CODE do .env
SECRET_CODE = os.getenv("SECRET_CODE")

url = 'http://localhost:8000/request/'
headers = {
    'accept': 'application/json',
    'secret-code': SECRET_CODE,
    'Content-Type': 'application/json'
}

numbers = ["123456", "124485", "768455", "899965", "465558"]
emails = ["dd@gmail.com", "ligs@gmail.com", "aba@gmail.com", "lacre@gmail.com", "joia@gmail.com"]

for number, email in zip(numbers, emails):
    data = {
        "number": number,
        "email": email
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"Requisição enviada para número: {number}, email: {email}")
    print(f"Status Code: {response.status_code}")
    print(f"Resposta: {response.text}")
    
    time.sleep(2)  # intervalo de 2 segundos
