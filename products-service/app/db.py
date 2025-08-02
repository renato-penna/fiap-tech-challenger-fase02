"""
In-Memory Database Module.

This module provides an in-memory database implementation for storing products.
Used as a fallback or for testing purposes when a real database is not available.
"""

from typing import Dict


products_db: Dict[str, Dict] = {}


def get_db() -> Dict[str, Dict]:
    """
    Return the in-memory "database" instance.

    In a real database scenario, this function could return a database session.

    Returns:
        Dict[str, Dict]: In-memory database dictionary
    """
    return products_db
