# products-service/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.routers import product_router # Importa o roteador de produtos
# Importa as novas funções de banco de dados
from app.database import create_db_tables, get_db, insert_initial_products
from app.repositories.product_repository import ProductRepository # Importa o repositório
import time # Importa a biblioteca time para usar sleep

# Cria a instância da aplicação FastAPI
app = FastAPI(title="Gerenciamento de Produtos Backend")

# Evento de inicialização: cria as tabelas e insere dados iniciais
@app.on_event("startup")
async def startup_event():
    """
    Função executada na inicialização da aplicação.
    Cria as tabelas no banco de dados se elas não existirem
    e insere dados iniciais se a tabela de produtos estiver vazia.
    Inclui lógica de retry para esperar o DB estar pronto.
    """
    print("DEBUG: Iniciando evento de startup da aplicação...")
    
    # --- Lógica de Retry para Conexão com o Banco de Dados ---
    max_retries = 10
    retry_delay = 5 # segundos
    
    for i in range(max_retries):
        try:
            print(f"DEBUG: Tentativa {i+1}/{max_retries} de conectar e criar tabelas no DB...")
            create_db_tables() # Tenta criar as tabelas
            print("DEBUG: Tabelas do banco de dados criadas (ou já existentes).")
            
            # Se a criação de tabelas for bem-sucedida, a conexão funcionou.
            # Agora, insere os dados iniciais.
            db = next(get_db()) 
            try:
                insert_initial_products(db) 
            finally:
                db.close()
            
            print("DEBUG: Evento de startup da aplicação concluído com sucesso.")
            return # Sai da função se tudo deu certo
        except Exception as e:
            print(f"DEBUG: Erro de conexão com o DB na inicialização: {e}")
            if i < max_retries - 1:
                print(f"DEBUG: Tentando novamente em {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                print("DEBUG: Número máximo de tentativas de conexão com o DB atingido. Falha na inicialização.")
                # Em um ambiente de produção, você pode querer levantar a exceção
                # ou ter um mecanismo de alerta aqui.
                raise # Re-levanta a exceção se todas as tentativas falharem
    # --- Fim da Lógica de Retry ---


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
