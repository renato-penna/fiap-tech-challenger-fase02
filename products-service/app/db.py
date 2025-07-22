from typing import Dict

# Dicionário em memória para armazenar os produtos.
# A chave é o ID do produto (string) e o valor é um dicionário com os dados do produto.
products_db: Dict[str, Dict] = {}

def get_db():
    """
    Retorna a instância da "base de dados" em memória.
    Em um cenário de banco de dados real, esta função poderia retornar uma sessão de banco de dados.
    """
    return products_db
