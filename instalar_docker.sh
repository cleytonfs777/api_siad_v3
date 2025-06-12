#!/bin/bash

# Configuração do proxy
export http_proxy=http://proxymg.prodemge.gov.br:8080
export https_proxy=http://proxymg.prodemge.gov.br:8080

# Atualização inicial e instalação de dependências
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Criação do diretório para chaves GPG
sudo install -m 0755 -d /etc/apt/keyrings

# Download da chave GPG do repositório Docker via proxy
sudo curl -x http://proxymg.prodemge.gov.br:8080 -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Adição do repositório Docker (forçando codinome jammy - Ubuntu 22.04)
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu jammy stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Atualiza repositórios e instala o Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
