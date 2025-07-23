# app/repositories/product_repository.py
import uuid
from typing import List, Dict, Optional
from app.db import get_db
from app.schemas.product import ProductCreate, Product

class ProductRepository:
    """
    Repositório para operações CRUD em produtos.
    Interage com a "base de dados" em memória.
    """
    def __init__(self):
        self.db = get_db() # Obtém a instância da base de dados em memória

    def get_all(self) -> List[Product]:
        """
        Retorna todos os produtos armazenados.
        """
        return [Product(**data) for data in self.db.values()]

    def get_by_id(self, product_id: str) -> Optional[Product]:
        """
        Retorna um produto pelo seu ID.
        Retorna None se o produto não for encontrado.
        """
        product_data = self.db.get(product_id)
        if product_data:
            return Product(**product_data)
        return None

    def create(self, product_create: ProductCreate) -> Product:
        """
        Cria um novo produto e o adiciona à base de dados.
        Gera um ID único para o produto.
        """
        product_id = str(uuid.uuid4())
        new_product_data = product_create.model_dump()
        new_product_data["id"] = product_id
        self.db[product_id] = new_product_data
        return Product(**new_product_data)

    def update(self, product_id: str, product_update: ProductCreate) -> Optional[Product]:
        """
        Atualiza um produto existente.
        Retorna o produto atualizado ou None se o produto não for encontrado.
        """
        if product_id not in self.db:
            return None
        updated_product_data = product_update.model_dump()
        updated_product_data["id"] = product_id # Garante que o ID seja mantido
        self.db[product_id] = updated_product_data
        return Product(**updated_product_data)

    def delete(self, product_id: str) -> bool:
        """
        Deleta um produto da base de dados.
        Retorna True se o produto foi deletado, False caso contrário.
        """
        print(f"DEBUG: Tentando deletar produto com ID: {product_id}") # Linha de depuração
        if product_id in self.db:
            del self.db[product_id]
            print(f"DEBUG: Produto com ID: {product_id} DELETADO com sucesso do DB em memória.") # Linha de depuração
            return True
        print(f"DEBUG: Produto com ID: {product_id} NÃO ENCONTRADO no DB em memória.") # Linha de depuração
        return False

