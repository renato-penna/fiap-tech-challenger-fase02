"""Modelo Produto."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Produto:
    """Modelo que representa um produto."""
    
    nome: str
    espaco: float
    valor: float
    id: Optional[int] = None
    quantidade: Optional[int] = None
    
    def to_dict(self):
        """Converte para dicionário."""
        data = {
            "nome": self.nome,
            "espaco": self.espaco,
            "valor": self.valor
        }
        if self.id is not None:
            data["id"] = self.id
        if self.quantidade is not None:
            data["quantidade"] = self.quantidade
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        """Cria produto a partir de dicionário."""
        return cls(
            id=data.get("id"),
            nome=data["nome"],
            espaco=data["espaco"],
            valor=data["valor"],
            quantidade=data.get("quantidade")
        )