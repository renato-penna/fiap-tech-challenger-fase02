"""
Database Configuration Module.

This module contains database configuration and utility functions for
the products service, including connection setup, session management,
and initial data insertion.
"""

import os
import uuid
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://app_user:mysecretpassword@fiap-tech-challenger-fase2-db:5432/products_db"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Utility function to get a database session.

    Used as a FastAPI dependency to manage the session.
    Ensures the session is closed after use.

    Yields:
        Session: Database session instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db_tables() -> None:
    """
    Create all tables in the database.

    This function should be called during application initialization.
    ProductModel import is done here to ensure Base.metadata
    has all models registered before creating tables.
    """
    from app.models.product_model import ProductModel
    Base.metadata.create_all(bind=engine)


def insert_initial_products(db: Session) -> None:
    """
    Insert initial products into the database if the table is empty.

    Args:
        db: Database session instance
    """
    from app.models.product_model import ProductModel

    if db.query(ProductModel).count() == 0:
        initial_products_data = [
            {"nome": "Gaming Chair", "espaco": 0.75, "valor": 1200.00},
            {"nome": "Office Desk", "espaco": 1.5, "valor": 800.00},
            {"nome": "27-inch Monitor", "espaco": 0.3, "valor": 950.00},
            {"nome": "Mechanical Keyboard", "espaco": 0.1, "valor": 300.00},
            {"nome": "Gaming Mouse", "espaco": 0.05, "valor": 150.00},
            {"nome": "Wireless Headset", "espaco": 0.2, "valor": 400.00},
            {"nome": "Full HD Webcam", "espaco": 0.02, "valor": 250.00},
            {"nome": "Essential Laptop", "espaco": 0.8, "valor": 2500.00},
            {"nome": "Multifunction Printer", "espaco": 0.6, "valor": 700.00},
            {"nome": "Wi-Fi 6 Router", "espaco": 0.15, "valor": 350.00},
            {"nome": "1TB SSD", "espaco": 0.01, "valor": 450.00},
            {"nome": "RTX 3060 Graphics Card", "espaco": 0.5, "valor": 2200.00},
            {"nome": "16GB RAM", "espaco": 0.03, "valor": 380.00},
            {"nome": "750W Power Supply", "espaco": 0.25, "valor": 500.00},
            {"nome": "Gaming Case", "espaco": 0.9, "valor": 600.00}
        ]

        for product_data in initial_products_data:
            new_product = ProductModel(
                id=str(uuid.uuid4()),
                nome=product_data["nome"],
                espaco=product_data["espaco"],
                valor=product_data["valor"]
            )
            db.add(new_product)

        db.commit()
