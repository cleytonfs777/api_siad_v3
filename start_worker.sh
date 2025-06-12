#!/bin/bash

# Ativar virtualenv
source /home/ad1429240/api_siad_v3/venv/bin/activate

# Ir para pasta onde está o worker
cd /home/ad1429240/api_siad_v3/app

# Executar worker e redirecionar logs (caso queira duplo log também aqui)
python worker.py
