"""Aplicação principal - Página Home."""

import streamlit as st
from config import PAGE_TITLE, PAGE_LAYOUT

def main():
    """Página principal da aplicação."""
    
    # Configuração da página
    st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT)
    
    st.title("Sistema de Gerenciamento de Produtos")
    
    st.markdown("""
    ## Bem-vindo ao Sistema de Gerenciamento de Produtos
    
    Este sistema permite:
    
    ### 📦 Gerenciamento de Produtos
    - Cadastrar novos produtos
    - Editar produtos existentes
    - Excluir produtos
    - Visualizar lista completa de produtos
    
    ### 🚛 Controle de Carga
    - Selecionar produtos para otimização
    - Configurar parâmetros de otimização
    - Executar algoritmo genético para maximizar valor da carga
    - Visualizar resultados da otimização
    
    ---
    
    ### Como usar:
    1. **Navegue** usando o menu lateral
    2. **Gerencie** seus produtos na seção correspondente
    3. **Otimize** a carga do caminhão conforme necessário
    
    """)

if __name__ == "__main__":
    main()