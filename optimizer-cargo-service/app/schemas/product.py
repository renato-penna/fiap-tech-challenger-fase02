"""
Product Schema Module.

This module contains Pydantic models for product data structures
used in the optimization process.
"""

from pydantic import BaseModel


class ProductInput(BaseModel):
    """
    Input model for product data in optimization requests.

    Represents a product with its basic attributes needed for
    the genetic algorithm optimization.

    Attributes:
        name: Product name
        space: Space occupied by the product
        value: Product value
        amount: Quantity of the product
    """

    name: str
    space: float
    value: float
    amount: int


class ProductOutput(BaseModel):
    """
    Output model for product data in optimization responses.

    Represents a selected product with calculated totals
    from the optimization process.

    Attributes:
        name: Product name
        space: Space occupied by the product
        value: Product value
        amount: Quantity of the product
        total_space: Total space for this product (space * amount)
        total_value: Total value for this product (value * amount)
    """

    name: str
    space: float
    value: float
    amount: int
    total_space: float
    total_value: float
