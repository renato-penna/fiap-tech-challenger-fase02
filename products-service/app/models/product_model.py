"""
Product Model Module.

This module contains the SQLAlchemy model for the Product entity,
defining the database table structure and field mappings.
"""

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ProductModel(Base):
    """
    SQLAlchemy model for the 'products' table in the database.

    Maps product fields to database table columns with appropriate
    data types and constraints.

    Attributes:
        id: Unique product identifier (primary key)
        nome: Product name (indexed for faster queries)
        espaco: Space occupied by the product (float)
        valor: Product value (float)
    """

    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, index=True)
    espaco: Mapped[float] = mapped_column(Float)
    valor: Mapped[float] = mapped_column(Float)
