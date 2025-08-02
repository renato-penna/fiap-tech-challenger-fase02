"""
Product Management Page Module.

This module contains the Streamlit page for product management functionality,
including product listing, creation, editing, and deletion operations.
"""

import sys
import os
from typing import List

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Add the app root directory to the path
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

try:
    from services.produto_service import ProdutoService
    from utils.ui_helpers import (
        aplicar_estilos, inicializar_sessao, limpar_formulario,
        mostrar_erro, mostrar_sucesso, mostrar_info
    )
    from config import (
        SESSION_SHOW_FORM, SESSION_EDIT_ID, SESSION_DELETE_CONFIRMATION,
        MESSAGES, PAGE_TITLE, PAGE_LAYOUT
    )
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

st.set_page_config(
    page_title=f"{PAGE_TITLE} - Management",
    layout=PAGE_LAYOUT,
    page_icon="📦"
)


def main() -> None:
    """
    Main function for the product management page.

    Sets up the page, initializes session state, loads products,
    and renders the product management interface.
    """
    st.title("📦 Product Management")
    aplicar_estilos()
    inicializar_sessao()

    service = ProdutoService()

    st.session_state[SESSION_SHOW_FORM] = True
    st.session_state[SESSION_EDIT_ID] = None
    st.session_state[SESSION_DELETE_CONFIRMATION] = None

    st.markdown("---")

    try:
        with st.spinner("🔄 Loading products..."):
            produtos = service.listar_todos()

        if produtos:
            st.success(f"✅ {len(produtos)} product(s) loaded")
        else:
            st.info("ℹ️ No products found")

    except ConnectionError:
        mostrar_erro(
            "❌ Connection error with products service. "
            "Please check if the backend is running."
        )
        st.stop()
    except Exception as e:
        mostrar_erro(f"❌ Unexpected error: {str(e)}")
        st.error(f"Technical details: {e}")
        st.stop()

    renderizar_grid(produtos, service)
    renderizar_formulario(service, produtos)


def renderizar_grid(produtos: List, service: ProdutoService) -> None:
    """
    Render the products grid.

    Args:
        produtos: List of products to display
        service: Product service instance
    """
    if not produtos:
        mostrar_info(MESSAGES["nenhum_produto"])
        return

    df = pd.DataFrame([p.to_dict() for p in produtos])

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=False)
    gb.configure_column("id", hide=True)
    gb.configure_selection('single', use_checkbox=True)

    st.subheader("Product List")
    grid_response = AgGrid(
        df,
        gridOptions=gb.build(),
        enable_enterprise_modules=False,
        update_mode="MODEL_CHANGED",
        fit_columns_on_grid_load=True,
        key="produtos_grid"
    )

    processar_selecao(grid_response, produtos, service)


def processar_selecao(
    grid_response: dict, produtos: List, service: ProdutoService
) -> None:
    """
    Process grid selection.

    Args:
        grid_response: Response from the AgGrid component
        produtos: List of products
        service: Product service instance
    """
    selected = grid_response["selected_rows"]

    if tem_selecao(selected):
        produto_dict = (
            selected.iloc[0].to_dict() if isinstance(selected, pd.DataFrame)
            else selected[0]
        )
        produto = service.buscar_por_id(produto_dict['id'], produtos)

        if produto:
            st.write(f"Selected product: {produto.nome}")
    else:
        st.session_state[SESSION_DELETE_CONFIRMATION] = None


def tem_selecao(selected) -> bool:
    """
    Check if there is a valid selection.

    Args:
        selected: Selection data from grid

    Returns:
        bool: True if there is a valid selection, False otherwise
    """
    return ((isinstance(selected, pd.DataFrame) and not selected.empty) or
            (isinstance(selected, list) and selected))


def renderizar_formulario(service: ProdutoService, produtos: List) -> None:
    """
    Render the product form.

    Args:
        service: Product service instance
        produtos: List of products for reference
    """
    produto_editado = None

    if st.session_state.get(SESSION_EDIT_ID):
        try:
            produto_editado = service.buscar_por_id(
                st.session_state[SESSION_EDIT_ID], produtos
            )
        except ValueError:
            mostrar_erro("Product not found.")
            limpar_formulario()
            st.experimental_rerun()
            return

    titulo = "✏️ Edit Product" if produto_editado else "➕ New Product"
    st.subheader(titulo)

    valores = {
        "nome": produto_editado.nome if produto_editado else "",
        "espaco": float(produto_editado.espaco) if produto_editado else 0.0,
        "valor": float(produto_editado.valor) if produto_editado else 0.0
    }

    with st.form("form_produto", clear_on_submit=True):
        st.write("**Fill in the product data:**")

        nome = st.text_input("📝 Product Name", value=valores["nome"])
        espaco = st.number_input(
            "📏 Space", value=valores["espaco"], min_value=0.0, format="%.4f"
        )
        valor = st.number_input(
            "💰 Value", value=valores["valor"], min_value=0.0, format="%.2f"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            salvar_clicked = st.form_submit_button(
                "💾 Save", type="primary", use_container_width=True
            )

        with col2:
            cancelar_clicked = st.form_submit_button(
                "❌ Cancel", use_container_width=True
            )

        with col3:
            st.write("")

        if cancelar_clicked:
            limpar_formulario()
            st.success("✅ Form cancelled!")
            st.experimental_rerun()

        if salvar_clicked:

            if not nome or not nome.strip():
                mostrar_erro("Product name is required!")
                return

            if espaco < 0:
                mostrar_erro("Space must be greater than or equal to zero!")
                return

            if valor < 0:
                mostrar_erro("Value must be greater than or equal to zero!")
                return

            with st.spinner("💾 Saving product..."):
                try:
                    if produto_editado:
                        service.atualizar(
                            produto_editado.id, nome.strip(), espaco, valor
                        )
                        mostrar_sucesso(MESSAGES["produto_atualizado"])
                    else:
                        service.criar(nome.strip(), espaco, valor)
                        mostrar_sucesso(MESSAGES["produto_criado"])

                    limpar_formulario()

                except Exception as e:
                    mostrar_erro(f"Error saving product: {str(e)}")
                    st.exception(e)


if __name__ == "__main__":
    main()
