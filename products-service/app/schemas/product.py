# app/schemas/product_schema.py
# Define os modelos Pydantic para validação de dados de entrada e saída.

from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    """
    Modelo base para um produto, contendo os campos comuns.
    """
    nome: str
    espaco: float
    valor: float

class ProductCreate(ProductBase):
    """
    Modelo para criação de um novo produto.
    Herda de ProductBase. O ID é gerado pelo backend.
    """
    pass

class Product(ProductBase):
    """
    Modelo completo de um produto, incluindo o ID.
    Usado para representar um produto retornado pela API.
    """
    id: str

    class Config:
        """
        Configuração para o Pydantic, permitindo que o modelo seja criado a partir de atributos de objeto.
        Útil ao converter de dicionário para modelo Pydantic.
        """
        from_attributes = True
