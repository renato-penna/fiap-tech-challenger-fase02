"""
Optimization Service Module.

This module provides service layer functionality for cargo optimization,
including genetic algorithm execution through HTTP API calls to the
optimizer service.
"""

import requests
from typing import List, Dict, Any

from config import OPTIMIZER_API_URL, REQUEST_TIMEOUT


class OtimizacaoService:
    """
    Service class for cargo optimization operations.

    Provides methods to interact with the optimization API backend,
    handling HTTP requests and response processing for genetic
    algorithm execution.
    """

    def __init__(self) -> None:
        """
        Initialize the optimization service.

        Sets up the base URL and timeout configuration for API calls.
        """
        self.base_url: str = OPTIMIZER_API_URL
        self.timeout: int = REQUEST_TIMEOUT

    def otimizar_carga(
        self, produtos_selecionados: List[Dict], limite: float,
        taxa_mutacao: float = 0.01, numero_geracoes: int = 100,
        tamanho_populacao: int = 200
    ) -> Dict[str, Any]:
        """
        Execute cargo optimization using genetic algorithm.

        Args:
            produtos_selecionados: List of selected products with quantities
            limite: Space limit for the truck
            taxa_mutacao: Mutation rate for genetic algorithm (default: 0.01)
            numero_geracoes: Number of generations (default: 100)
            tamanho_populacao: Population size (default: 200)

        Returns:
            Dict[str, Any]: Optimization result from the genetic algorithm

        Raises:
            ConnectionError: If connection to the optimization service fails
            Exception: If there's an error during optimization
        """
        payload = {
            "products": produtos_selecionados,
            "limit": limite,
            "mutation_rate": taxa_mutacao,
            "number_generations": numero_geracoes,
            "population_size": tamanho_populacao
        }

        try:
            print(f"Debug: Tentando conectar com {self.base_url}")
            print(f"Debug: Payload = {payload}")
            response = requests.post(
                self.base_url, json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            print(f"Debug: ConnectionError = {e}")
            raise ConnectionError("Connection error with optimization service.")
        except requests.exceptions.RequestException as e:
            print(f"Debug: RequestException = {e}")
            raise Exception(f"Error during optimization: {e}")

    def otimizar(
        self, produtos: List, quantidades: Dict[str, int], limite: float,
        taxa_mutacao: float = 0.01, numero_geracoes: int = 100,
        tamanho_populacao: int = 200
    ) -> Dict[str, Any]:
        """
        Execute cargo optimization with product list and quantities.

        Args:
            produtos: List of available products
            quantidades: Dictionary of product quantities
            limite: Space limit for the truck
            taxa_mutacao: Mutation rate for genetic algorithm (default: 0.01)
            numero_geracoes: Number of generations (default: 100)
            tamanho_populacao: Population size (default: 200)

        Returns:
            Dict[str, Any]: Optimization result from the genetic algorithm
        """
        produtos_selecionados = []
        for produto in produtos:
            quantidade = quantidades.get(produto.id, 0)
            if quantidade > 0:
                produtos_selecionados.append({
                    "name": produto.nome,
                    "space": produto.espaco,
                    "value": produto.valor,
                    "amount": quantidade
                })

        return self.otimizar_carga(
            produtos_selecionados, limite, taxa_mutacao,
            numero_geracoes, tamanho_populacao
        )
