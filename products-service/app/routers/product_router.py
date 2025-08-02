"""
Product Router Module.

This module contains the FastAPI router for product-related endpoints.
It provides CRUD operations for products with dependency injection.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.controllers.product_controller import ProductController
from app.database import get_db
from app.schemas.product import Product, ProductCreate


router = APIRouter()


def get_product_controller(db: Session = Depends(get_db)) -> ProductController:
    """
    FastAPI dependency that provides a ProductController instance
    with an injected database session.

    Args:
        db: Database session dependency.

    Returns:
        ProductController: Controller instance with database session.
    """
    return ProductController(db)


@router.get("/", response_model=List[Product])
async def get_all_products_route(
    controller: ProductController = Depends(get_product_controller)
) -> List[Product]:
    """
    Get all products.

    Args:
        controller: Product controller dependency.

    Returns:
        List[Product]: List of all products.
    """
    return controller.get_all_products()


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product_route(
    product: ProductCreate,
    controller: ProductController = Depends(get_product_controller)
) -> Product:
    """
    Create a new product.

    Args:
        product: Product data to create.
        controller: Product controller dependency.

    Returns:
        Product: Created product.
    """
    return controller.create_product(product)


@router.get("/{product_id}", response_model=Product)
async def get_product_route(
    product_id: str,
    controller: ProductController = Depends(get_product_controller)
) -> Product:
    """
    Get a specific product by ID.

    Args:
        product_id: Product ID.
        controller: Product controller dependency.

    Returns:
        Product: Product with the specified ID.

    Raises:
        HTTPException: If product is not found.
    """
    product = controller.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.put("/{product_id}", response_model=Product)
async def update_product_route(
    product_id: str,
    product: ProductCreate,
    controller: ProductController = Depends(get_product_controller)
) -> Product:
    """
    Update an existing product by ID.

    Args:
        product_id: Product ID to update.
        product: New product data.
        controller: Product controller dependency.

    Returns:
        Product: Updated product.

    Raises:
        HTTPException: If product is not found.
    """
    updated_product = controller.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_route(
    product_id: str,
    controller: ProductController = Depends(get_product_controller)
) -> None:
    """
    Delete a product by ID.

    Args:
        product_id: Product ID to delete.
        controller: Product controller dependency.

    Raises:
        HTTPException: If product is not found.
    """
    if not controller.delete_product(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
