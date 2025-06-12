# Usa Python como base
FROM python:3.10-slim

# Define os argumentos para o proxy
ARG http_proxy
ARG https_proxy

# Aplica como variáveis de ambiente dentro do container
ENV http_proxy=${http_proxy}
ENV https_proxy=${https_proxy}

# Instala pacotes do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    gcc

# Define o diretório da aplicação
WORKDIR /app

# Copia os arquivos
COPY . /app

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
