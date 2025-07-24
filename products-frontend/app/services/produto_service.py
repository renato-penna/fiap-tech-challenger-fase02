"""Serviço de produtos."""

import requests
from typing import List
from models.produto import Produto
from config import PRODUCTS_API_URL, REQUEST_TIMEOUT

class ProdutoService:
    """Serviço para operações com produtos."""
    
    def __init__(self):
        self.base_url = PRODUCTS_API_URL
        self.timeout = REQUEST_TIMEOUT
    
    def listar_todos(self) -> List[Produto]:
        """Lista todos os produtos."""
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            response.raise_for_status()
            produtos_data = response.json()
            return [Produto.from_dict(data) for data in produtos_data]
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Erro de conexão com o serviço de produtos.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao buscar produtos: {e}")
    
    def criar(self, nome: str, espaco: float, valor: float) -> Produto:
        """Cria um novo produto."""
        data = {"nome": nome, "espaco": espaco, "valor": valor}
        try:
            response = requests.post(self.base_url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return Produto.from_dict(response.json())
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao criar produto: {e}")
    
    def atualizar(self, produto_id: int, nome: str, espaco: float, valor: float) -> Produto:
        """Atualiza um produto."""
        data = {"nome": nome, "espaco": espaco, "valor": valor}
        try:
            response = requests.put(f"{self.base_url}/{produto_id}", json=data, timeout=self.timeout)
            response.raise_for_status()
            return Produto.from_dict(response.json())
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao atualizar produto: {e}")
    
    def excluir(self, produto_id: int):
        """Exclui um produto."""
        try:
            response = requests.delete(f"{self.base_url}/{produto_id}", timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao excluir produto: {e}")
    
    def buscar_por_id(self, produto_id: int, produtos: List[Produto]) -> Produto:
        """Busca produto por ID."""
        produto_encontrado = next((p for p in produtos if p.id == produto_id), None)
        if not produto_encontrado:
            raise ValueError(f"Produto com ID {produto_id} não encontrado")
        return produto_encontrado