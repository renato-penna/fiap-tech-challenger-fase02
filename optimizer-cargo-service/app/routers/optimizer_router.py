from fastapi import APIRouter
from app.schemas.optimize import OptimizeRequest, OptimizeResponse
from app.controllers.optimizer_controller import OptimizerController

router = APIRouter(prefix="/optimize", tags=["optimize"])

@router.post("/", response_model=OptimizeResponse)
def optimize(data: OptimizeRequest):
    return OptimizerController.optimize(data)
