import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_option_menu import option_menu
import requests
import pandas as pd

API_URL = "http://localhost:8000/products"
st.set_page_config(page_title="Gerenciamento de Produtos", layout="wide")

# Menu lateral
menu = option_menu(
    "Menu", ["Gerenciamento de Produtos", "Controle de Carga"],
    icons=["list", "truck"],
    menu_icon="cast", default_index=0, orientation="vertical"
)

if menu == "Gerenciamento de Produtos":
    st.title("Gerenciamento de Produtos")
    st.markdown("""
    <style>
    .stButton>button {background-color: #1976d2; color: white;}
    .stTextInput>div>input {border: 1px solid #1976d2;}
    </style>
    """, unsafe_allow_html=True)

    # Inicializa variáveis de sessão
    if "show_form" not in st.session_state:
        st.session_state["show_form"] = False
    if "edit_id" not in st.session_state:
        st.session_state["edit_id"] = None

    # Botão Novo Produto
    if st.button("Novo Produto"):
        st.session_state["show_form"] = True
        st.session_state["edit_id"] = None

    # Listagem de produtos
    response = requests.get(API_URL)
    produtos = response.json() if response.status_code == 200 else []

    gb = GridOptionsBuilder.from_dataframe(
        pd.DataFrame(produtos)
    )
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=False)
    gb.configure_column("id", hide=True)
    gb.configure_column("Ações", cellRenderer="agGroupCellRenderer")
    grid_options = gb.build()

    st.subheader("Lista de Produtos")
    grid_response = AgGrid(
        pd.DataFrame(produtos),
        gridOptions=grid_options,
        enable_enterprise_modules=False,
        update_mode="NO_UPDATE",
        fit_columns_on_grid_load=True
    )

    # Botões de edição e exclusão
    selected = grid_response["selected_rows"]
    if selected:
        produto = selected[0]
        col1, col2 = st.columns(2)
        if col1.button("Editar", key=f"edit_{produto['id']}"):
            st.session_state["show_form"] = True
            st.session_state["edit_id"] = produto["id"]
        if col2.button("Excluir", key=f"delete_{produto['id']}"):
            if st.warning("Tem certeza que deseja excluir este produto?", icon="⚠️"):
                requests.delete(f"{API_URL}/{produto['id']}")
                st.session_state["show_form"] = False
                st.session_state["edit_id"] = None
                st.experimental_rerun()

    # Formulário de cadastro/edição
    if st.session_state.get("show_form", False):
        if st.session_state.get("edit_id"):
            produto = next((p for p in produtos if p["id"] == st.session_state["edit_id"]), None)
            st.subheader("Editar Produto")
        else:
            produto = {"nome": "", "espaco": 0.0, "valor": 0.0}
            st.subheader("Novo Produto")
        with st.form("produto_form"):
            nome = st.text_input("Nome", value=produto["nome"])
            espaco = st.number_input("Espaço", value=float(produto["espaco"]), min_value=0.0)
            valor = st.number_input("Valor", value=float(produto["valor"]), min_value=0.0)
            submitted = st.form_submit_button("Salvar")
            if submitted:
                data = {"nome": nome, "espaco": espaco, "valor": valor}
                if st.session_state.get("edit_id"):
                    requests.put(f"{API_URL}/{produto['id']}", json=data)
                else:
                    requests.post(API_URL, json=data)
                st.session_state["show_form"] = False
                st.experimental_rerun()

elif menu == "Controle de Carga":
    st.title("Controle de Carga do Caminhão")
    st.markdown("""
    <style>
    .stButton>button {background-color: #1976d2; color: white;}
    .stTextInput>div>input {border: 1px solid #1976d2;}
    </style>
    """, unsafe_allow_html=True)

    response = requests.get(API_URL)
    produtos = response.json() if response.status_code == 200 else []
    df = pd.DataFrame(produtos)
    if not df.empty:
        st.subheader("Selecione a quantidade de cada produto para o caminhão:")
        quantidade = {}
        for idx, row in df.iterrows():
            quantidade[row["id"]] = st.number_input(f"{row['nome']} (Espaço: {row['espaco']}, Valor: {row['valor']})", min_value=0, value=0, key=f"qtd_{row['id']}")
        limite = st.number_input("Limite de espaço do caminhão", min_value=0.0, value=3.0)
        taxa_mutacao = st.number_input("Taxa de mutação (opcional)", min_value=0.0, max_value=1.0, value=0.01)
        numero_geracoes = st.number_input("Número de gerações (opcional)", min_value=1, value=100)
        tamanho_populacao = st.number_input("Tamanho da população (opcional)", min_value=1, value=200)
        if st.button("Enviar seleção para otimização"):
            produtos_selecionados = []
            for idx, row in df.iterrows():
                qtd = quantidade[row["id"]]
                if qtd > 0:
                    produtos_selecionados.append({
                        "nome": row["nome"],
                        "espaco": row["espaco"],
                        "valor": row["valor"],
                        "quantidade": int(qtd)
                    })
            if not produtos_selecionados:
                st.warning("Selecione ao menos um produto!")
            else:
                optimizer_url = "http://localhost:8002/optimize/"
                payload = {
                    "produtos": produtos_selecionados,
                    "limite": limite,
                    "taxa_mutacao": taxa_mutacao,
                    "numero_geracoes": numero_geracoes,
                    "tamanho_populacao": tamanho_populacao
                }
                try:
                    resp = requests.post(optimizer_url, json=payload, timeout=60)
                    if resp.status_code == 200:
                        resultado = resp.json()
                        st.success("Otimização realizada com sucesso!")
                        st.write(f"Espaço total: {resultado['espaco_total']}")
                        st.write(f"Valor total: {resultado['valor_total']}")
                        st.subheader("Produtos selecionados:")
                        st.table(pd.DataFrame(resultado["produtos"]))
                    else:
                        st.error(f"Erro ao otimizar: {resp.text}")
                except Exception as e:
                    st.error(f"Erro de conexão com o serviço de otimização: {e}")
    else:
        st.info("Nenhum produto cadastrado.")
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_option_menu import option_menu
import requests

API_URL = "http://localhost:8000/products"

st.set_page_config(page_title="Gerenciamento de Produtos", layout="wide")

# Menu lateral
menu = option_menu(
    "Menu", ["Gerenciamento de Produtos", "Controle de Carga"],
    icons=["list", "truck"],
    menu_icon="cast", default_index=0, orientation="vertical"
)

if menu == "Gerenciamento de Produtos":
    st.title("Gerenciamento de Produtos")
    st.markdown("""
    <style>
    .stButton>button {background-color: #1976d2; color: white;}
    .stTextInput>div>input {border: 1px solid #1976d2;}
    </style>
    """, unsafe_allow_html=True)

    # Botão Novo Produto
    if st.button("Novo Produto"):
        st.session_state["show_form"] = True
        st.session_state["edit_id"] = None

    # Listagem de produtos
    response = requests.get(API_URL)
    produtos = response.json() if response.status_code == 200 else []

    gb = GridOptionsBuilder.from_dataframe(
        pd.DataFrame(produtos)
    )
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=False)
    gb.configure_column("id", hide=True)
    gb.configure_column("Ações", cellRenderer="agGroupCellRenderer")
    grid_options = gb.build()

    st.subheader("Lista de Produtos")
    grid_response = AgGrid(
        pd.DataFrame(produtos),
        gridOptions=grid_options,
        enable_enterprise_modules=False,
        update_mode="NO_UPDATE",
        fit_columns_on_grid_load=True
    )

    # Botões de edição e exclusão
    selected = grid_response["selected_rows"]
    if selected:
        produto = selected[0]
        col1, col2 = st.columns(2)
        if col1.button("Editar", key=f"edit_{produto['id']}"):
            st.session_state["show_form"] = True
            st.session_state["edit_id"] = produto["id"]
        if col2.button("Excluir", key=f"delete_{produto['id']}"):
            if st.confirm("Tem certeza que deseja excluir este produto?"):
                requests.delete(f"{API_URL}/{produto['id']}")
                st.experimental_rerun()

    # Formulário de cadastro/edição
    if st.session_state.get("show_form", False):
        if st.session_state.get("edit_id"):
            produto = next((p for p in produtos if p["id"] == st.session_state["edit_id"]), None)
            st.subheader("Editar Produto")
        else:
            produto = {"nome": "", "espaco": 0.0, "valor": 0.0}
            st.subheader("Novo Produto")
        with st.form("produto_form"):
            nome = st.text_input("Nome", value=produto["nome"])
            espaco = st.number_input("Espaço", value=float(produto["espaco"]), min_value=0.0)
            valor = st.number_input("Valor", value=float(produto["valor"]), min_value=0.0)
            submitted = st.form_submit_button("Salvar")
            if submitted:
                data = {"nome": nome, "espaco": espaco, "valor": valor}
                if st.session_state.get("edit_id"):
                    requests.put(f"{API_URL}/{produto['id']}", json=data)
                else:
                    requests.post(API_URL, json=data)
                st.session_state["show_form"] = False
                st.experimental_rerun()

elif menu == "Controle de Carga":
    st.title("Controle de Carga do Caminhão")
    st.info("Em breve...")
