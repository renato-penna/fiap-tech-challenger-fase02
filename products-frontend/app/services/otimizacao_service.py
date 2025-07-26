"""Serviço de otimização."""

import requests
from typing import List, Dict
from config import OPTIMIZER_API_URL, REQUEST_TIMEOUT

class OtimizacaoService:
    """Serviço para otimização de carga."""
    
    def __init__(self):
        self.base_url = OPTIMIZER_API_URL
        self.timeout = REQUEST_TIMEOUT
    
    def otimizar_carga(self, produtos_selecionados: List[Dict], limite: float, 
                      taxa_mutacao: float = 0.01, numero_geracoes: int = 100, 
                      tamanho_populacao: int = 200) -> Dict:
        """Executa otimização da carga."""
        payload = {
            "produtos": produtos_selecionados,
            "limite": limite,
            "taxa_mutacao": taxa_mutacao,
            "numero_geracoes": numero_geracoes,
            "tamanho_populacao": tamanho_populacao
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Erro de conexão com o serviço de otimização.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao otimizar: {e}")