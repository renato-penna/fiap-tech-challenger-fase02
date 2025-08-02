"""
Optimizer Controller Module.

This module contains the business logic controller for cargo optimization
operations, providing the interface between API routes and the genetic
algorithm.
"""

from typing import List

from app.schemas.optimize import OptimizeRequest, OptimizeResponse
from app.schemas.product import ProductOutput
from .genetic_algorithm import GeneticAlgorithm


class OptimizerController:
    """
    Controller for cargo optimization operations.

    Provides business logic for genetic algorithm optimization,
    handling request processing and response formatting.
    """

    @staticmethod
    def optimize(data: OptimizeRequest) -> OptimizeResponse:
        """
        Optimize cargo loading using genetic algorithm.

        Args:
            data: Optimization request containing products and constraints

        Returns:
            OptimizeResponse: Optimization results with selected products and metrics

        Raises:
            HTTPException: If optimization fails or constraints are invalid
        """
        # Use default values for optional parameters
        population_size = data.population_size or 200
        number_generations = data.number_generations or 100
        mutation_rate = data.mutation_rate or 0.01

        ga = GeneticAlgorithm(
            data.products,
            data.limit,
            population_size,
            number_generations,
            mutation_rate=mutation_rate
        )
        result = ga.run()

        # Serialize the result into the response format
        products: List[ProductOutput] = []
        total_space: float = 0
        total_value: float = 0

        if result and hasattr(result, 'chromosome'):
            for idx, gene in enumerate(result.chromosome):
                if gene == '1':
                    product = ga.products[idx]
                    products.append(ProductOutput(
                        name=product.name,
                        space=product.space,
                        value=product.value,
                        amount=product.amount,
                        total_space=product.space * product.amount,
                        total_value=product.value * product.amount
                    ))
                    total_space += product.space * product.amount
                    total_value += product.value * product.amount

        return OptimizeResponse(
            products=products,
            total_space=total_space,
            total_value=total_value
        )

