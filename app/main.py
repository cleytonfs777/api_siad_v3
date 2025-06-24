import os
import redis
import json
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# ✅ Carregar variáveis do .env
load_dotenv()

# ✅ Inicializar FastAPI sem docs/redoc
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# ✅ Permitir somente a origem da intranet para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://intranet.bombeiros.mg.gov.br"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ✅ Middleware para bloquear ferramentas como curl, Postman etc.
@app.middleware("http")
async def block_non_browser_clients(request: Request, call_next):
    user_agent = request.headers.get("user-agent", "").lower()
    bloqueados = ["curl", "httpie", "wget", "postman", "python", "java", "go-http-client"]
    
    if any(b in user_agent for b in bloqueados):
        return JSONResponse(
            status_code=403,
            content={"detail": "Acesso bloqueado: apenas navegadores são permitidos."}
        )

    return await call_next(request)

# ✅ Conectar ao Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# ✅ Configurações
SECRET_CODE = os.getenv("SECRET_CODE")
EXPIRATION_TIME = 45  # segundos

# ✅ Schema da requisição
class RequestSchema(BaseModel):
    number: str
    email: str

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/request/")
def create_request(request_data: RequestSchema, secret_code: str = Header(None)):
    if secret_code != SECRET_CODE:
        raise HTTPException(status_code=403, detail="Acesso negado. SECRET_CODE inválido.")

    if redis_client.exists(f"processing:{request_data.number}"):
        return {"message": "Pedido de reset já registrado. Aguarde a liberação..."}

    redis_client.setex(f"processing:{request_data.number}", EXPIRATION_TIME, "processing")

    request_id = f"req:{request_data.number}"
    redis_client.lpush("queue", json.dumps({
        "id": request_id,
        "number": request_data.number,
        "email": request_data.email
    }))

    return {"message": "Pedido de reset enviado e confirmado com sucesso. Enviaremos um email de confirmação."}
