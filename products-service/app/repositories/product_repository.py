"""
Product Repository Module.

This module contains the repository layer for product data access,
providing CRUD operations using SQLAlchemy ORM.
"""

import uuid
from typing import List, Optional

from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, Product
from app.models.product_model import ProductModel


class ProductRepository:
    """
    Repository for product CRUD operations using SQLAlchemy.

    Provides data access layer functionality for product operations,
    handling database queries and model conversions.
    """

    def __init__(self, db: Session) -> None:
        """
        Initialize the product repository.

        Args:
            db: Database session instance
        """
        self.db = db

    def get_all(self) -> List[Product]:
        """
        Retrieve all products from the database.

        Returns:
            List[Product]: List of all products
        """
        products = self.db.query(ProductModel).all()
        return [Product.model_validate(p) for p in products]

    def get_by_id(self, product_id: str) -> Optional[Product]:
        """
        Retrieve a product by its ID from the database.

        Args:
            product_id: Product ID to search for

        Returns:
            Optional[Product]: Product if found, None otherwise
        """
        product = self.db.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        if product:
            return Product.model_validate(product)
        return None

    def create(self, product_create: ProductCreate) -> Product:
        """
        Create a new product and add it to the database.

        Generates a unique ID for the product.

        Args:
            product_create: Product data for creation

        Returns:
            Product: Created product instance
        """
        product_id = str(uuid.uuid4())
        new_product_model = ProductModel(
            id=product_id,
            nome=product_create.nome,
            espaco=product_create.espaco,
            valor=product_create.valor
        )
        self.db.add(new_product_model)
        self.db.commit()
        self.db.refresh(new_product_model)
        return Product.model_validate(new_product_model)

    def update(
        self, product_id: str, product_update: ProductCreate
    ) -> Optional[Product]:
        """
        Update an existing product in the database.

        Args:
            product_id: Product ID to update
            product_update: New product data

        Returns:
            Optional[Product]: Updated product if found, None otherwise
        """
        product_model = self.db.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        if not product_model:
            return None

        product_model.nome = product_update.nome
        product_model.espaco = product_update.espaco
        product_model.valor = product_update.valor

        self.db.commit()
        self.db.refresh(product_model)
        return Product.model_validate(product_model)

    def delete(self, product_id: str) -> bool:
        """
        Delete a product from the database.

        Args:
            product_id: Product ID to delete

        Returns:
            bool: True if product was deleted, False otherwise
        """
        product_model = self.db.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        if not product_model:
            return False

        self.db.delete(product_model)
        self.db.commit()
        return True
