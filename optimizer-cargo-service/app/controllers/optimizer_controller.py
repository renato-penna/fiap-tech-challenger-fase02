from fastapi import HTTPException
from app.schemas.optimize import OptimizeRequest, OptimizeResponse
from app.schemas.product import ProductOutput
from .genetic_algorithm import GeneticAlgorithm

class OptimizerController:
    
    @staticmethod
    def optimize(data: OptimizeRequest) -> OptimizeResponse:
        ga = GeneticAlgorithm(
            data.products, 
            data.limit, 
            data.population_size, 
            data.number_generations, 
            mutation_rate=data.mutation_rate
        )
        result = ga.run()
        print(result)
        # Serialize the result into the response format
        products = []
        total_space = 0
        total_value = 0
        for idx, gene in enumerate(result.chromosome):
            if gene == '1':
                product = ga.products[idx]
                print(f"Product {product.name} R$ {product.value} x {product.amount}")
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

