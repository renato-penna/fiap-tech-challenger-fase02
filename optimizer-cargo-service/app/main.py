from fastapi import FastAPI
from app.routers.optimizer_router import router as optimizer_router

app = FastAPI(title="Optimizer Cargo Service")
app.include_router(optimizer_router)
