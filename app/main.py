import sys
import os
import redis
import json
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# ✅ Carregar variáveis do arquivo .env
load_dotenv()

# ✅ Inicializar FastAPI
app = FastAPI()

# ✅ Conectar ao Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# ✅ Obtém o SECRET_CODE do .env
SECRET_CODE = os.getenv("SECRET_CODE")

# ✅ Tempo de expiração da chave para evitar cliques repetidos (ex: 45 segundos)
EXPIRATION_TIME = 45  

# ✅ Modelo de requisição recebida
class RequestSchema(BaseModel):
    number: str
    email: str

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/request/")
def create_request(
    request_data: RequestSchema, 
    secret_code: str = Header(None)
):
    """
    Processa a solicitação de reset, verificando se já existe na fila.
    Se já estiver na fila, retorna uma mensagem apropriada.
    Se for uma nova requisição, adiciona à fila e retorna sucesso.
    """

    if secret_code != SECRET_CODE:
        raise HTTPException(status_code=403, detail=f"Acesso negado. SECRET_CODE inválido. Esse é o enviado: {secret_code} e esse é o do sistema: {SECRET_CODE}")

    # ✅ Verificar se o número já está sendo processado
    if redis_client.exists(f"processing:{request_data.number}"):
        return {"message": "Pedido de reset já registrado. Aguarde a liberação..."}

    # ✅ Criar um bloqueio temporário no Redis para evitar múltiplos cliques
    redis_client.setex(f"processing:{request_data.number}", EXPIRATION_TIME, "processing")

    # ✅ Se não estiver na fila, adiciona à fila no Redis
    request_id = f"req:{request_data.number}"  # Criar ID único baseado no número
    redis_client.lpush("queue", json.dumps({"id": request_id, "number": request_data.number, "email": request_data.email}))

    return {"message": "Pedido de reset enviado e confirmado com sucesso. Enviaremos um email de confirmação."}
