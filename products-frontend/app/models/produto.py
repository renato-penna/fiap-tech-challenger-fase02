"""
Product Model Module.

This module contains the Product data model used throughout the frontend
application for representing product data structures.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Produto:
    """
    Product data model.

    Represents a product with its basic attributes including name,
    space requirement, value, and optional ID and quantity.

    Attributes:
        nome: Product name
        espaco: Space occupied by the product (float)
        valor: Product value (float)
        id: Optional product ID
        quantidade: Optional product quantity
    """

    nome: str
    espaco: float
    valor: float
    id: Optional[str] = None
    quantidade: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert product to dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing product data
        """
        data: Dict[str, Any] = {
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
    def from_dict(cls, data: Dict[str, Any]) -> "Produto":
        """
        Create product instance from dictionary.

        Args:
            data: Dictionary containing product data

        Returns:
            Produto: New product instance

        Raises:
            KeyError: If required fields are missing from data
        """
        return cls(
            id=data.get("id"),
            nome=data["nome"],
            espaco=data["espaco"],
            valor=data["valor"],
            quantidade=data.get("quantidade")
        )
