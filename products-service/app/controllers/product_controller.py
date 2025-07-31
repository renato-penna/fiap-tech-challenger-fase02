# products-service/app/controllers/product_controller.py
from typing import List, Optional
from sqlalchemy.orm import Session # Importa a Session
from app.schemas.product import ProductCreate, Product # Importa de product.py
from app.repositories.product_repository import ProductRepository

class ProductController:
    """
    Controlador para gerenciar a lógica de negócios dos produtos.
    """
    # O construtor agora recebe a sessão do banco de dados
    def __init__(self, db: Session):
        self.repository = ProductRepository(db) # Passa a sessão para o repositório

    def get_all_products(self) -> List[Product]:
        """
        Obtém todos os produtos.
        """
        return self.repository.get_all()

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """
        Obtém um produto pelo seu ID.
        """
        return self.repository.get_by_id(product_id)

    def create_product(self, product_data: ProductCreate) -> Product:
        """
        Cria um novo produto.
        """
        return self.repository.create(product_data)

    def update_product(self, product_id: str, product_data: ProductCreate) -> Optional[Product]:
        """
        Atualiza um produto existente.
        """
        return self.repository.update(product_id, product_data)

    def delete_product(self, product_id: str) -> bool:
        """
        Deleta um produto.
        """
        return self.repository.delete(product_id)
