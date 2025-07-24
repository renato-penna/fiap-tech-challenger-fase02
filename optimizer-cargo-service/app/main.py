from fastapi import FastAPI
from .routers.optimizer_router import router as optimizer_router

app = FastAPI()
app.include_router(optimizer_router)
