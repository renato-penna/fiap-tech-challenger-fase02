# products-service/app/routers/product_router.py
from fastapi import APIRouter, HTTPException, status, Depends # Importa Depends
from typing import List
from sqlalchemy.orm import Session # Importa Session
from app.schemas.product import Product, ProductCreate # Importa de product.py
from app.controllers.product_controller import ProductController
from app.database import get_db # Importa a função get_db

# Cria uma instância do APIRouter
router = APIRouter()

# Função de dependência para obter o controlador de produto
# Isso permite que a sessão do banco de dados seja injetada automaticamente
def get_product_controller(db: Session = Depends(get_db)) -> ProductController:
    """
    Dependência FastAPI que fornece uma instância de ProductController
    com uma sessão de banco de dados injetada.
    """
    return ProductController(db)

@router.get("/", response_model=List[Product])
async def get_all_products_route(
    controller: ProductController = Depends(get_product_controller) # Injeta o controlador
):
    """
    Retorna uma lista de todos os produtos.
    """
    return controller.get_all_products()

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product_route(
    product: ProductCreate,
    controller: ProductController = Depends(get_product_controller) # Injeta o controlador
):
    """
    Cria um novo produto.
    """
    return controller.create_product(product)

@router.get("/{product_id}", response_model=Product)
async def get_product_route(
    product_id: str,
    controller: ProductController = Depends(get_product_controller) # Injeta o controlador
):
    """
    Retorna um produto específico pelo seu ID.
    """
    product = controller.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product_route(
    product_id: str,
    product: ProductCreate,
    controller: ProductController = Depends(get_product_controller) # Injeta o controlador
):
    """
    Atualiza um produto existente pelo seu ID.
    """
    updated_product = controller.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_route(
    product_id: str,
    controller: ProductController = Depends(get_product_controller) # Injeta o controlador
):
    """
    Deleta um produto pelo seu ID.
    """
    if not controller.delete_product(product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso"}
