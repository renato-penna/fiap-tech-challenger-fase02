"""
Optimization Schema Module.

This module contains Pydantic models for optimization request and response
data structures used in the genetic algorithm optimization process.
"""

from typing import List, Optional

from pydantic import BaseModel

from .product import ProductInput, ProductOutput


class OptimizeRequest(BaseModel):
    """
    Request model for cargo optimization.

    Contains the products to optimize, space limit, and genetic algorithm
    parameters for the optimization process.

    Attributes:
        products: List of products to optimize
        limit: Maximum space limit for the cargo
        mutation_rate: Genetic algorithm mutation rate (default: 0.01)
        number_generations: Number of generations to run (default: 100)
        population_size: Size of the population (default: 200)
    """

    products: List[ProductInput]
    limit: float
    mutation_rate: Optional[float] = 0.01
    number_generations: Optional[int] = 100
    population_size: Optional[int] = 200


class OptimizeResponse(BaseModel):
    """
    Response model for cargo optimization results.

    Contains the optimized product selection and calculated metrics
    from the genetic algorithm optimization.

    Attributes:
        products: List of selected products with quantities
        total_space: Total space used by selected products
        total_value: Total value of selected products
    """

    products: List[ProductOutput]
    total_space: float
    total_value: float
