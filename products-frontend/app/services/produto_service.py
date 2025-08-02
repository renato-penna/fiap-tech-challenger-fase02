"""
Product Service Module.

This module provides service layer functionality for product operations,
including CRUD operations through HTTP API calls to the backend service.
"""

import requests
from typing import List, Optional

from models.produto import Produto
from config import PRODUCTS_API_URL, REQUEST_TIMEOUT


class ProdutoService:
    """
    Service class for product operations.

    Provides methods to interact with the products API backend,
    handling HTTP requests and response processing.
    """

    def __init__(self) -> None:
        """
        Initialize the product service.

        Sets up the base URL and timeout configuration for API calls.
        """
        self.base_url: str = PRODUCTS_API_URL
        self.timeout: int = REQUEST_TIMEOUT

    def listar_todos(self) -> List[Produto]:
        """
        Retrieve all products from the API.

        Returns:
            List[Produto]: List of all products

        Raises:
            ConnectionError: If connection to the products service fails
            Exception: If there's an error retrieving products
        """
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            response.raise_for_status()
            produtos_data = response.json()
            return [Produto.from_dict(data) for data in produtos_data]
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection error with products service.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error retrieving products: {e}")

    def criar(self, nome: str, espaco: float, valor: float) -> Produto:
        """
        Create a new product.

        Args:
            nome: Product name
            espaco: Product space requirement
            valor: Product value

        Returns:
            Produto: Created product instance

        Raises:
            Exception: If there's an error creating the product
        """
        data = {"nome": nome, "espaco": espaco, "valor": valor}
        try:
            response = requests.post(
                self.base_url, json=data, timeout=self.timeout
            )
            response.raise_for_status()
            return Produto.from_dict(response.json())
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error creating product: {e}")

    def atualizar(
        self, produto_id: str, nome: str, espaco: float, valor: float
    ) -> Produto:
        """
        Update an existing product.

        Args:
            produto_id: Product ID to update
            nome: New product name
            espaco: New product space requirement
            valor: New product value

        Returns:
            Produto: Updated product instance

        Raises:
            Exception: If there's an error updating the product
        """
        data = {"nome": nome, "espaco": espaco, "valor": valor}
        try:
            response = requests.put(
                f"{self.base_url}/{produto_id}",
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return Produto.from_dict(response.json())
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error updating product: {e}")

    def excluir(self, produto_id: str) -> None:
        """
        Delete a product.

        Args:
            produto_id: Product ID to delete

        Raises:
            Exception: If there's an error deleting the product
        """
        try:
            response = requests.delete(
                f"{self.base_url}/{produto_id}", timeout=self.timeout
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error deleting product: {e}")

    def buscar_por_id(
        self, produto_id: str, produtos: List[Produto]
    ) -> Optional[Produto]:
        """
        Find product by ID from a list of products.

        Args:
            produto_id: Product ID to search for
            produtos: List of products to search in

        Returns:
            Optional[Produto]: Found product or None if not found

        Raises:
            ValueError: If product with the given ID is not found
        """
        produto_encontrado = next(
            (p for p in produtos if p.id == produto_id), None
        )
        if not produto_encontrado:
            raise ValueError(f"Product with ID {produto_id} not found")
        return produto_encontrado
