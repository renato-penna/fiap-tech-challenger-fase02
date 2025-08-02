"""
Cargo Control Page Module.

This module contains the Streamlit page for cargo optimization functionality,
including product selection, optimization parameters, and genetic algorithm execution.
"""

import sys
import os
from typing import List, Dict, Any

import streamlit as st
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.produto_service import ProdutoService
from services.otimizacao_service import OtimizacaoService
from utils.ui_helpers import (
    aplicar_estilos, mostrar_erro, mostrar_sucesso, mostrar_info
)
from config import MESSAGES, PAGE_TITLE, PAGE_LAYOUT

st.set_page_config(
    page_title=f"{PAGE_TITLE} - Cargo Control",
    layout=PAGE_LAYOUT,
    page_icon="🚛"
)


def main() -> None:
    """
    Main function for the cargo control page.

    Sets up the page, loads products, and renders the cargo optimization interface.
    """
    st.title("🚛 Truck Cargo Control")
    aplicar_estilos()

    produto_service = ProdutoService()
    otimizacao_service = OtimizacaoService()

    try:
        produtos = produto_service.listar_todos()
    except ConnectionError:
        mostrar_erro("Connection error with products service.")
        return
    except Exception as e:
        mostrar_erro(str(e))
        return

    if not produtos:
        mostrar_info("No products registered. Register products first in the Management page.")
        st.info("👈 Use the sidebar menu to navigate to the Product Management page")
        return

    renderizar_selecao_produtos(produtos, otimizacao_service)


def renderizar_selecao_produtos(
    produtos: List, otimizacao_service: OtimizacaoService
) -> None:
    """
    Render product selection and optimization interface.

    Args:
        produtos: List of available products
        otimizacao_service: Optimization service instance
    """

    st.subheader("📋 Available Products")
    df_produtos = pd.DataFrame([p.to_dict() for p in produtos])
    st.dataframe(df_produtos[['nome', 'espaco', 'valor']], use_container_width=True)

    st.subheader("📦 Select the quantity of each product:")

    quantidades: Dict[str, int] = {}
    for produto in produtos:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{produto.nome}** - Space: {produto.espaco} | Value: {produto.valor}")
        with col2:
            quantidade = st.number_input(
                "Qty",
                min_value=0,
                value=0,
                key=f"qtd_{produto.id}",
                label_visibility="collapsed"
            )
            quantidades[produto.id] = quantidade

    st.subheader("⚙️ Optimization Parameters")

    col1, col2 = st.columns(2)

    with col1:
        limite = st.number_input(
            "🚛 Truck space limit",
            min_value=0.0,
            value=3.0,
            help="Maximum space capacity of the truck"
        )
        taxa_mutacao = st.number_input(
            "🧬 Mutation rate",
            min_value=0.0,
            max_value=1.0,
            value=0.01,
            help="Genetic algorithm mutation rate (0.01 = 1%)"
        )

    with col2:
        numero_geracoes = st.number_input(
            "🔄 Number of generations",
            min_value=1,
            value=100,
            help="Number of genetic algorithm iterations"
        )
        tamanho_populacao = st.number_input(
            "👥 Population size",
            min_value=1,
            value=200,
            help="Size of the genetic algorithm population"
        )

    if st.button("🚀 Execute Optimization", type="primary"):
        if sum(quantidades.values()) == 0:
            mostrar_erro("Please select at least one product!")
            return

        with st.spinner("🧬 Executing genetic algorithm..."):
            resultado = executar_otimizacao(
                produtos, quantidades, limite, taxa_mutacao,
                numero_geracoes, tamanho_populacao, otimizacao_service
            )

        if resultado:
            exibir_resultado(resultado)


def executar_otimizacao(
    produtos: List, quantidades: Dict[str, int], limite: float,
    taxa_mutacao: float, numero_geracoes: int, tamanho_populacao: int,
    otimizacao_service: OtimizacaoService
) -> Dict[str, Any]:
    """
    Execute cargo optimization using genetic algorithm.

    Args:
        produtos: List of available products
        quantidades: Dictionary of product quantities
        limite: Space limit for the truck
        taxa_mutacao: Mutation rate for genetic algorithm
        numero_geracoes: Number of generations
        tamanho_populacao: Population size
        otimizacao_service: Optimization service instance

    Returns:
        Dict[str, Any]: Optimization result or None if failed
    """
    try:
        resultado = otimizacao_service.otimizar(
            produtos, quantidades, limite, taxa_mutacao,
            numero_geracoes, tamanho_populacao
        )
        mostrar_sucesso("Optimization completed successfully!")
        return resultado
    except Exception as e:
        mostrar_erro(f"Error during optimization: {str(e)}")
        return None


def exibir_resultado(resultado: Dict[str, Any]) -> None:
    """
    Display optimization results.

    Args:
        resultado: Optimization result dictionary
    """
    st.subheader("📊 Optimization Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Value", f"${resultado['valor_total']:.2f}")

    with col2:
        st.metric("Space Used", f"{resultado['espaco_usado']:.2f}")

    with col3:
        st.metric("Space Efficiency", f"{(resultado['espaco_usado']/resultado['limite'])*100:.1f}%")

    st.subheader("📦 Selected Products")

    if resultado['produtos_selecionados']:
        df_resultado = pd.DataFrame(resultado['produtos_selecionados'])
        st.dataframe(df_resultado, use_container_width=True)
    else:
        st.info("No products were selected in the optimal solution.")


if __name__ == "__main__":
    main()
