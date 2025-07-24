# products-service/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Variáveis de ambiente para conexão com o banco de dados
# O 'db' é o nome do serviço do PostgreSQL no docker-compose.yml
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app_user:mysecretpassword@db:5432/products_db")

# Cria o motor SQLAlchemy
# echo=True para ver as queries SQL no console (útil para depuração)
engine = create_engine(DATABASE_URL, echo=True)

# Cria uma SessionLocal class
# Cada instância de SessionLocal será uma sessão de banco de dados
# autocommit=False: não faz commit automaticamente
# autoflush=False: não faz flush automaticamente
# bind=engine: liga a sessão ao motor que criamos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos SQLAlchemy
Base = declarative_base()

def get_db():
    """
    Função de utilidade para obter uma sessão de banco de dados.
    Usada como uma dependência no FastAPI para gerenciar a sessão.
    Garante que a sessão seja fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para criar todas as tabelas definidas nos modelos Base
def create_db_tables():
    """
    Cria todas as tabelas no banco de dados.
    Esta função deve ser chamada na inicialização da aplicação.
    Em um ambiente de produção, você usaria ferramentas de migração como Alembic.
    """
    Base.metadata.create_all(bind=engine)
