from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import uuid # Importa uuid para gerar IDs para os produtos iniciais

# A importação de ProductModel foi movida para dentro das funções
# onde é utilizada para evitar a importação circular.
# from app.models.product_model import ProductModel # REMOVIDA ESTA LINHA

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

def create_db_tables():
    """
    Cria todas as tabelas no banco de dados.
    Esta função deve ser chamada na inicialização da aplicação.
    A importação de ProductModel é feita aqui para garantir que Base.metadata
    tenha todos os modelos registrados antes de criar as tabelas.
    """
    # Importa ProductModel aqui para evitar importação circular
    from app.models.product_model import ProductModel # ADICIONADA AQUI
    print("DEBUG: Criando tabelas do banco de dados (se não existirem)...")
    Base.metadata.create_all(bind=engine)
    print("DEBUG: Tabelas do banco de dados criadas (ou já existentes).")

def insert_initial_products(db: Session):
    """
    Insere produtos iniciais no banco de dados se a tabela estiver vazia.
    """
    # Importa ProductModel aqui para evitar importação circular
    from app.models.product_model import ProductModel # ADICIONADA AQUI
    print("DEBUG: Verificando se a tabela de produtos está vazia para inserir dados iniciais...")
    
    if db.query(ProductModel).count() == 0:
        print("DEBUG: Tabela de produtos vazia. Inserindo dados iniciais...")
        initial_products_data = [
            {"nome": "Cadeira Gamer", "espaco": 0.75, "valor": 1200.00},
            {"nome": "Mesa Escritório", "espaco": 1.5, "valor": 800.00},
            {"nome": "Monitor 27 polegadas", "espaco": 0.3, "valor": 950.00},
            {"nome": "Teclado Mecânico", "espaco": 0.1, "valor": 300.00},
            {"nome": "Mouse Gamer", "espaco": 0.05, "valor": 150.00},
            {"nome": "Headset Wireless", "espaco": 0.2, "valor": 400.00},
            {"nome": "Webcam Full HD", "espaco": 0.02, "valor": 250.00},
            {"nome": "Notebook Essencial", "espaco": 0.8, "valor": 2500.00},
            {"nome": "Impressora Multifuncional", "espaco": 0.6, "valor": 700.00},
            {"nome": "Roteador Wi-Fi 6", "espaco": 0.15, "valor": 350.00},
            {"nome": "SSD 1TB", "espaco": 0.01, "valor": 450.00},
            {"nome": "Placa de Vídeo RTX 3060", "espaco": 0.5, "valor": 2200.00},
            {"nome": "Memória RAM 16GB", "espaco": 0.03, "valor": 380.00},
            {"nome": "Fonte de Alimentação 750W", "espaco": 0.25, "valor": 500.00},
            {"nome": "Gabinete Gamer", "espaco": 0.9, "valor": 600.00}
        ]

        for product_data in initial_products_data:
            new_product = ProductModel(
                id=str(uuid.uuid4()), # Gera um ID único para cada produto
                nome=product_data["nome"],
                espaco=product_data["espaco"],
                valor=product_data["valor"]
            )
            db.add(new_product)
        
        db.commit() # Salva os produtos no banco de dados
        print("DEBUG: Dados iniciais inseridos com sucesso.")
    else:
        print("DEBUG: Tabela de produtos já contém dados. Pulando inserção inicial.")