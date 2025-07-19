from pydantic import BaseModel
from typing import List, Optional

class ProdutoInput(BaseModel):
    nome: str
    espaco: float
    valor: float
    quantidade: int

class OptimizeRequest(BaseModel):
    produtos: List[ProdutoInput]
    limite: float
    taxa_mutacao: Optional[float] = 0.01
    numero_geracoes: Optional[int] = 100
    tamanho_populacao: Optional[int] = 200

class ProdutoOutput(BaseModel):
    nome: str
    espaco: float
    valor: float
    quantidade: int
    total_espaco: float
    total_valor: float

class OptimizeResponse(BaseModel):
    produtos: List[ProdutoOutput]
    espaco_total: float
    valor_total: float
