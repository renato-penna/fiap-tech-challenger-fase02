from pydantic import BaseModel
from typing import List, Optional
from .product import ProductInput, ProductOutput


class OptimizeRequest(BaseModel):
    products: List[ProductInput]
    limit: float
    mutation_rate: Optional[float] = 0.01
    number_generations: Optional[int] = 100
    population_size: Optional[int] = 200


class OptimizeResponse(BaseModel):
    products: List[ProductOutput]
    total_space: float
    total_value: float
