from pydantic import BaseModel


class ProductInput(BaseModel):
    name: str
    space: float
    value: float
    amount: int


class ProductOutput(BaseModel):
    name: str
    space: float
    value: float
    amount: int
    total_space: float
    total_value: float
