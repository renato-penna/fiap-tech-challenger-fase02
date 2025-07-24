from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.routers import product_router # Importa o roteador de produtos
from app.database import create_db_tables, get_db # Importa funções de banco de dados
from app.repositories.product_repository import ProductRepository # Importa o repositório

# Cria a instância da aplicação FastAPI
app = FastAPI(title="Gerenciamento de Produtos Backend")

# Evento de inicialização: cria as tabelas no banco de dados
@app.on_event("startup")
async def startup_event():
    """
    Função executada na inicialização da aplicação.
    Cria as tabelas no banco de dados se elas não existirem.
    """
    print("DEBUG: Criando tabelas do banco de dados...")
    create_db_tables()
    print("DEBUG: Tabelas do banco de dados criadas (ou já existentes).")

# Inclui o roteador de produtos na aplicação
# Agora, o roteador usará a dependência de sessão do banco de dados
app.include_router(product_router.router, prefix="/products", tags=["products"])

@app.get("/")
async def root():
    """
    Endpoint raiz para verificar se o serviço está funcionando.
    """
    return {"message": "Serviço de Gerenciamento de Produtos está online!"}

# Para rodar este serviço:
# 1. Certifique-se de que todas as dependências estão instaladas (incluindo sqlalchemy e psycopg2-binary).
# 2. Certifique-se de que seu docker-compose.yml está configurado para o serviço 'db' e 'products-service'.
# 3. Navegue até o diretório 'fiap-tech-challenger-fase02' no seu terminal.
# 4. Execute: docker-compose up --build