# products-service/app/repositories/product_repository.py
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, Product # Importa de product.py
from app.models.product_model import ProductModel # Importa o modelo SQLAlchemy

class ProductRepository:
    """
    Repositório para operações CRUD em produtos usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db # A sessão do banco de dados é injetada no construtor

    def get_all(self) -> List[Product]:
        """
        Retorna todos os produtos armazenados no banco de dados.
        """
        # Consulta todos os produtos na tabela ProductModel
        products = self.db.query(ProductModel).all()
        # Converte os modelos SQLAlchemy para schemas Pydantic
        return [Product.model_validate(p) for p in products]

    def get_by_id(self, product_id: str) -> Optional[Product]:
        """
        Retorna um produto pelo seu ID do banco de dados.
        Retorna None se o produto não for encontrado.
        """
        # Consulta um produto pelo ID
        product = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product:
            return Product.model_validate(product)
        return None

    def create(self, product_create: ProductCreate) -> Product:
        """
        Cria um novo produto e o adiciona ao banco de dados.
        Gera um ID único para o produto.
        """
        product_id = str(uuid.uuid4())
        # Cria uma nova instância do modelo SQLAlchemy
        new_product_model = ProductModel(
            id=product_id,
            nome=product_create.nome,
            espaco=product_create.espaco,
            valor=product_create.valor
        )
        # Adiciona o novo produto à sessão
        self.db.add(new_product_model)
        # Faz o commit da transação para salvar no banco de dados
        self.db.commit()
        # Atualiza a instância para garantir que o ID gerado (se fosse autoincrement) esteja disponível
        self.db.refresh(new_product_model)
        return Product.model_validate(new_product_model)

    def update(self, product_id: str, product_update: ProductCreate) -> Optional[Product]:
        """
        Atualiza um produto existente no banco de dados.
        Retorna o produto atualizado ou None se o produto não for encontrado.
        """
        # Busca o produto pelo ID
        product_model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not product_model:
            return None
        
        # Atualiza os atributos do modelo
        product_model.nome = product_update.nome
        product_model.espaco = product_update.espaco
        product_model.valor = product_update.valor
        
        # Faz o commit da transação
        self.db.commit()
        self.db.refresh(product_model) # Atualiza a instância após o commit
        return Product.model_validate(product_model)

    def delete(self, product_id: str) -> bool:
        """
        Deleta um produto do banco de dados.
        Retorna True se o produto foi deletado, False caso contrário.
        """
        print(f"DEBUG: Tentando deletar produto com ID: {product_id}") # Linha de depuração
        # Busca o produto pelo ID
        product_model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not product_model:
            print(f"DEBUG: Produto com ID: {product_id} NÃO ENCONTRADO no DB.") # Linha de depuração
            return False
        
        # Deleta o produto da sessão
        self.db.delete(product_model)
        # Faz o commit da transação
        self.db.commit()
        print(f"DEBUG: Produto com ID: {product_id} DELETADO com sucesso do DB.") # Linha de depuração
        return True
