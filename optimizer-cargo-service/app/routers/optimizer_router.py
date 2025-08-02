"""
Optimizer Router Module.

This module contains the FastAPI router for optimization endpoints.
It provides the main optimization endpoint using genetic algorithms.
"""

from fastapi import APIRouter

from app.controllers.optimizer_controller import OptimizerController
from app.schemas.optimize import OptimizeRequest, OptimizeResponse


router = APIRouter(prefix="/optimize", tags=["optimize"])


@router.post("/", response_model=OptimizeResponse)
async def optimize(data: OptimizeRequest) -> OptimizeResponse:
    """
    Optimize cargo loading using genetic algorithm.

    This endpoint receives a list of products with quantities and space
    constraints, then uses a genetic algorithm to find the optimal
    combination that maximizes value while respecting space limits.

    Args:
        data: Optimization request containing products and constraints.

    Returns:
        OptimizeResponse: Optimization results with selected products and
        metrics including total value, space used, and optimization details.

    Raises:
        HTTPException: If optimization fails or invalid data is provided.
    """
    return OptimizerController.optimize(data)
