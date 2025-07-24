FROM python:3.11-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos da raiz do contexto de build (products-service/)
# Certifique-se de que requirements.txt está em products-service/requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o conteúdo da subpasta 'app' (que contém o código FastAPI)
# DIRETAMENTE para o diretório de trabalho do contêiner (/app).
# Isso garante que 'app' seja o módulo raiz acessível.
COPY ./app /app

# Comando para iniciar a aplicação FastAPI
# O 'main:app' agora se refere a /app/main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
