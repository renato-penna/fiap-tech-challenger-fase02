"""Página de gerenciamento de produtos."""

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import sys
import os

# Adiciona o diretório raiz da app ao path
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
    st.error(f"Erro ao importar módulos: {e}")
    st.stop()

st.set_page_config(
    page_title=f"{PAGE_TITLE} - Gerenciamento", 
    layout=PAGE_LAYOUT,
    page_icon="📦"
)

def main():
    """Função principal da página."""
    st.title("📦 Gerenciamento de Produtos")
    aplicar_estilos()
    inicializar_sessao()
    
    service = ProdutoService()

    st.session_state[SESSION_SHOW_FORM] = True
    st.session_state[SESSION_EDIT_ID] = None
    st.session_state[SESSION_DELETE_CONFIRMATION] = None

    st.markdown("---")
    
    try:
        with st.spinner("🔄 Carregando produtos..."):
            produtos = service.listar_todos()
        
        if produtos:
            st.success(f"✅ {len(produtos)} produto(s) carregado(s)")
        else:
            st.info("ℹ️ Nenhum produto encontrado")
            
    except ConnectionError:
        mostrar_erro("❌ Erro de conexão com o serviço de produtos. Verifique se o backend está rodando.")
        st.stop()
    except Exception as e:
        mostrar_erro(f"❌ Erro inesperado: {str(e)}")
        st.error(f"Detalhes técnicos: {e}")
        st.stop()
    
    renderizar_grid(produtos, service)
    
    renderizar_formulario(service, produtos)
    
def renderizar_grid(produtos, service):
    """Renderiza a grid de produtos."""
    if not produtos:
        mostrar_info(MESSAGES["nenhum_produto"])
        return
    
    df = pd.DataFrame([p.to_dict() for p in produtos])
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=False)
    gb.configure_column("id", hide=True)
    gb.configure_selection('single', use_checkbox=True)
    
    st.subheader("Lista de Produtos")
    grid_response = AgGrid(
        df,
        gridOptions=gb.build(),
        enable_enterprise_modules=False,
        update_mode="MODEL_CHANGED",
        fit_columns_on_grid_load=True,
        key="produtos_grid"
    )
    
    processar_selecao(grid_response, produtos, service)

def processar_selecao(grid_response, produtos, service):
    """Processa seleção na grid."""
    selected = grid_response["selected_rows"]
    
    if tem_selecao(selected):
        produto_dict = selected.iloc[0].to_dict() if isinstance(selected, pd.DataFrame) else selected[0]
        produto = service.buscar_por_id(produto_dict['id'], produtos)
        
        if produto:
            st.write(f"Produto selecionado: {produto.nome}")
    else:
        st.session_state[SESSION_DELETE_CONFIRMATION] = None

def tem_selecao(selected):
    """Verifica se há seleção válida."""
    return ((isinstance(selected, pd.DataFrame) and not selected.empty) or 
            (isinstance(selected, list) and selected))

def renderizar_formulario(service, produtos):
    """Renderiza formulário de produto."""

    produto_editado = None
    
    if st.session_state.get(SESSION_EDIT_ID):
        try:
            produto_editado = service.buscar_por_id(st.session_state[SESSION_EDIT_ID], produtos)
        except ValueError:
            mostrar_erro("Produto não encontrado.")
            limpar_formulario()
            st.experimental_rerun()
            return
    
    titulo = "✏️ Editar Produto" if produto_editado else "➕ Novo Produto"
    st.subheader(titulo)
    
    valores = {
        "nome": produto_editado.nome if produto_editado else "",
        "espaco": float(produto_editado.espaco) if produto_editado else 0.0,
        "valor": float(produto_editado.valor) if produto_editado else 0.0
    }
    
    with st.form("form_produto", clear_on_submit=True):
        st.write("**Preencha os dados do produto:**")
        
        nome = st.text_input("📝 Nome do Produto", value=valores["nome"])
        espaco = st.number_input("📏 Espaço", value=valores["espaco"], min_value=0.0, format="%.4f")
        valor = st.number_input("💰 Valor", value=valores["valor"], min_value=0.0, format="%.2f")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            salvar_clicked = st.form_submit_button("💾 Salvar", type="primary", use_container_width=True)
        
        with col2:
            cancelar_clicked = st.form_submit_button("❌ Cancelar", use_container_width=True)
        
        with col3:
            st.write("") 
        
        if cancelar_clicked:
            limpar_formulario()
            st.success("✅ Formulário cancelado!")
            st.experimental_rerun()
        
        if salvar_clicked:
            
            if not nome or not nome.strip():
                mostrar_erro("Nome do produto é obrigatório!")
                return
            
            if espaco < 0:
                mostrar_erro("Espaço deve ser maior ou igual a zero!")
                return
                
            if valor < 0:
                mostrar_erro("Valor deve ser maior ou igual a zero!")
                return
            
            with st.spinner("💾 Salvando produto..."):
                try:
                    if produto_editado:
                        resultado = service.atualizar(produto_editado.id, nome.strip(), espaco, valor)
                        mostrar_sucesso(MESSAGES["produto_atualizado"])
                    else:
                        resultado = service.criar(nome.strip(), espaco, valor)
                        mostrar_sucesso(MESSAGES["produto_criado"])
                    
                    limpar_formulario()
                    
                except Exception as e:
                    mostrar_erro(f"Erro ao salvar produto: {str(e)}")
                    st.exception(e)

if __name__ == "__main__":
    main()