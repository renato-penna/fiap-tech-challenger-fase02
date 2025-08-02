"""
Product Controller Module.

This module contains the business logic controller for product operations,
providing an interface between the API routes and the repository layer.
"""

from typing import List, Optional

from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, Product
from app.repositories.product_repository import ProductRepository


class ProductController:
    """
    Controller for managing product business logic.

    Handles the business logic layer between API routes and the repository,
    providing a clean interface for product operations.
    """

    def __init__(self, db: Session) -> None:
        """
        Initialize the product controller.

        Args:
            db: Database session instance
        """
        self.repository = ProductRepository(db)

    def get_all_products(self) -> List[Product]:
        """
        Retrieve all products.

        Returns:
            List[Product]: List of all products
        """
        return self.repository.get_all()

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """
        Retrieve a product by its ID.

        Args:
            product_id: Product ID to search for

        Returns:
            Optional[Product]: Product if found, None otherwise
        """
        return self.repository.get_by_id(product_id)

    def create_product(self, product_data: ProductCreate) -> Product:
        """
        Create a new product.

        Args:
            product_data: Product data for creation

        Returns:
            Product: Created product instance
        """
        return self.repository.create(product_data)

    def update_product(
        self, product_id: str, product_data: ProductCreate
    ) -> Optional[Product]:
        """
        Update an existing product.

        Args:
            product_id: Product ID to update
            product_data: New product data

        Returns:
            Optional[Product]: Updated product if found, None otherwise
        """
        return self.repository.update(product_id, product_data)

    def delete_product(self, product_id: str) -> bool:
        """
        Delete a product.

        Args:
            product_id: Product ID to delete

        Returns:
            bool: True if product was deleted, False otherwise
        """
        return self.repository.delete(product_id)
