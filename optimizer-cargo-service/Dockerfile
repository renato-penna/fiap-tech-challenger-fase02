FROM python:3.11-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
# O requirements.txt está diretamente na pasta optimizer-cargo-service,
# então o caminho é relativo ao WORKDIR /app, que é onde o Dockerfile está sendo executado.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da pasta 'app' do seu host para '/app/app' no contêiner
# Isso incluirá main.py, controllers, routers, schemas, services, etc.
COPY ./app /app/app

# Comando para iniciar a aplicação FastAPI
# Ajuste 'app.main:app' se o seu ponto de entrada principal for diferente,
# por exemplo, se o seu arquivo principal for 'optimizer_service.py' e estiver em 'app/',
# o comando seria 'uvicorn app.optimizer_service:app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
