#!/bin/bash

# Verificar se o worker já está rodando e matar o processo
echo "Verificando se o worker já está rodando..."
WORKER_PID=$(pgrep -f "worker.py")

if [ ! -z "$WORKER_PID" ]; then
    echo "Worker encontrado com PID: $WORKER_PID. Parando o processo..."
    kill -TERM $WORKER_PID
    sleep 2
    
    # Verificar se o processo ainda está rodando e forçar a parada se necessário
    if pgrep -f "worker.py" > /dev/null; then
        echo "Processo ainda rodando. Forçando parada..."
        pkill -9 -f "worker.py"
        sleep 1
    fi
    echo "Worker anterior parado com sucesso."
else
    echo "Nenhum worker rodando."
fi

# Ativar o ambiente virtual
source /home/ad1429240/api_siad_v3/venv/bin/activate

# Mudar para o diretório da aplicação
cd /home/ad1429240/api_siad_v3/app

# Iniciar o novo worker
echo "Iniciando novo worker..."
nohup /home/ad1429240/api_siad_v3/venv/bin/python /home/ad1429240/api_siad_v3/app/worker.py > /home/ad1429240/api_siad_v3/worker.error.log 2> /home/ad1429240/api_siad_v3/worker.log &

# Obter o PID do novo processo
NEW_PID=$!
echo "Worker iniciado com PID: $NEW_PID"

# Verificar se o processo foi iniciado com sucesso
sleep 2
if pgrep -f "worker.py" > /dev/null; then
    echo "Worker iniciado com sucesso!"
else
    echo "Erro ao iniciar o worker. Verifique os logs em:"
    echo "  - /home/ad1429240/api_siad_v3/worker.error.log"
    echo "  - /home/ad1429240/api_siad_v3/worker.log"
fi
