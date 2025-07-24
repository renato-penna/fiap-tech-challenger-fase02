from sqlalchemy import Column, String, Float
from app.database import Base

class ProductModel(Base):
    """
    Modelo SQLAlchemy para a tabela 'products' no banco de dados.
    Mapeia os campos do produto para as colunas da tabela.
    """
    __tablename__ = "products" # Nome da tabela no banco de dados

    id = Column(String, primary_key=True, index=True) # ID único do produto
    nome = Column(String, index=True) # Nome do produto
    espaco = Column(Float) # Espaço que o produto ocupa (float)
    valor = Column(Float) # Valor do produto (float)
