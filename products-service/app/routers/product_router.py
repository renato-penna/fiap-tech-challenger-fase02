from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.product import Product, ProductCreate
from app.controllers.product_controller import ProductController

# Cria uma instância do APIRouter
router = APIRouter()

# Instancia o controlador de produtos
product_controller = ProductController()

@router.get("/", response_model=List[Product])
async def get_all_products_route():
    """
    Retorna uma lista de todos os produtos.
    """
    return product_controller.get_all_products()

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product_route(product: ProductCreate):
    """
    Cria um novo produto.
    """
    return product_controller.create_product(product)

@router.get("/{product_id}", response_model=Product)
async def get_product_route(product_id: str):
    """
    Retorna um produto específico pelo seu ID.
    """
    product = product_controller.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product_route(product_id: str, product: ProductCreate):
    """
    Atualiza um produto existente pelo seu ID.
    """
    updated_product = product_controller.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_route(product_id: str):
    """
    Deleta um produto pelo seu ID.
    """
    if not product_controller.delete_product(product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso"}