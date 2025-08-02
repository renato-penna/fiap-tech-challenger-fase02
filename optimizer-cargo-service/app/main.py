"""
Optimizer Service Main Application Module.

This module contains the main FastAPI application for the cargo optimization
service. It handles route registration for the genetic algorithm optimizer
and provides endpoints for cargo optimization using genetic algorithms.
"""

from fastapi import FastAPI

from .routers.optimizer_router import router as optimizer_router


app = FastAPI(
    title="Cargo Optimization Service",
    description="Service for optimizing cargo loading using genetic algorithms",
    version="1.0.0"
)
app.include_router(optimizer_router)
