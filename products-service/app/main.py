"""
Products Service Main Application Module.

This module contains the main FastAPI application for the products management
service. It handles database initialization, startup events, and route
registration.
"""

import time
from typing import Dict

from fastapi import FastAPI

from app.database import create_db_tables, get_db, insert_initial_products
from app.routers import product_router


app = FastAPI(title="Products Management Backend")


@app.on_event("startup")
async def startup_event() -> None:
    """
    Application startup event handler.

    Creates database tables if they don't exist and inserts initial products
    if the products table is empty. Includes retry logic to wait for the
    database to be ready.

    Raises:
        Exception: If database connection fails after maximum retries.
    """
    max_retries = 10
    retry_delay = 5

    for i in range(max_retries):
        try:
            create_db_tables()

            db = next(get_db())
            try:
                insert_initial_products(db)
            finally:
                db.close()

            return
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise


app.include_router(product_router.router, prefix="/products", tags=["products"])


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint to verify if the service is working.

    Returns:
        Dict[str, str]: A message indicating the service is online.
    """
    return {"message": "Products Management Service is online!"}
