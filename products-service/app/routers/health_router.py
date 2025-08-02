"""
Health Check Router Module.

This module contains the health check endpoint for the products service.
It provides a simple endpoint to verify if the service is running correctly.
"""

from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/health/")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Dict[str, str]: Health status
    """
    return {"status": "healthy", "service": "products-service"}
