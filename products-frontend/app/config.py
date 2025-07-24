"""Configurações da aplicação."""

import os

PRODUCTS_API_URL = os.getenv("PRODUCTS_API_URL", "http://products-service:8000/products")
OPTIMIZER_API_URL = os.getenv("OPTIMIZER_API_URL", "http://optimizer-service:8002/optimize/")

PAGE_TITLE = "Gerenciamento de Produtos"
PAGE_LAYOUT = "wide"

REQUEST_TIMEOUT = 60

SESSION_SHOW_FORM = "show_form"
SESSION_EDIT_ID = "edit_id"
SESSION_DELETE_CONFIRMATION = "awaiting_delete_confirmation"

MESSAGES = {
    "produto_criado": "Produto criado com sucesso!",
    "produto_atualizado": "Produto atualizado com sucesso!",
    "produto_excluido": "Produto excluído com sucesso!",
    "otimizacao_sucesso": "Otimização realizada com sucesso!",
    "nenhum_produto": "Nenhum produto cadastrado.",
    "selecione_produto": "Selecione ao menos um produto!"
}

BUTTON_STYLE = """
<style>
.stButton>button {background-color: #1976d2; color: white;}
.stTextInput>div>input {border: 1px solid #1976d2;}
</style>
"""