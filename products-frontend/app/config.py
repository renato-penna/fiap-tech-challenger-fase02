"""
Application Configuration Module.

This module contains all configuration settings for the products management
frontend application, including API URLs, page settings, session keys,
and UI messages.
"""

import os
from typing import Dict

# API Configuration
PRODUCTS_API_URL: str = os.getenv(
    "PRODUCTS_API_URL",
    "http://fiap-tech-challenger-fase2-products-service:8000/products"
)
OPTIMIZER_API_URL: str = os.getenv(
    "OPTIMIZER_API_URL",
    "http://fiap-tech-challenger-fase2-optimizer-cargo-service:8002/optimize/"
)

# Page Configuration
PAGE_TITLE: str = "Product Management System"
PAGE_LAYOUT: str = "wide"

# Request Configuration
REQUEST_TIMEOUT: int = 60

# Session Keys
SESSION_SHOW_FORM: str = "show_form"
SESSION_EDIT_ID: str = "edit_id"
SESSION_DELETE_CONFIRMATION: str = "awaiting_delete_confirmation"

# UI Messages
MESSAGES: Dict[str, str] = {
    "produto_criado": "Product created successfully!",
    "produto_atualizado": "Product updated successfully!",
    "produto_excluido": "Product deleted successfully!",
    "otimizacao_sucesso": "Optimization completed successfully!",
    "nenhum_produto": "No products registered.",
    "selecione_produto": "Please select at least one product!"
}

# UI Styles
BUTTON_STYLE: str = """
<style>
.stButton>button {background-color: #1976d2; color: white;}
.stTextInput>div>input {border: 1px solid #1976d2;}
</style>
"""
