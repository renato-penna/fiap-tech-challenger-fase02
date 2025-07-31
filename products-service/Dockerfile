# products-service/Dockerfile
FROM python:3.11-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
# Certifique-se de que requirements.txt está em products-service/requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia a pasta 'app' (que contém o código FastAPI) para dentro do WORKDIR /app.
# Isso resultará em /app/app dentro do contêiner.
COPY app/ ./app/

# Não definimos CMD aqui, pois o docker-compose.yml irá substituí-lo
# para permitir o live reload com volumes montados.
