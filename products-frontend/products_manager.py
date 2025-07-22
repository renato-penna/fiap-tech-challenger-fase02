import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_option_menu import option_menu
import requests
import pandas as pd

# Define a URL base para o serviço de produtos.
# Se estiver rodando em Docker Compose, use o nome do serviço: "http://products-service:8000/products".
# Se estiver rodando localmente (sem Docker), use: "http://localhost:8000/products".
API_URL = "http://products-service:8000/products" # ALTERADO PARA USAR O NOME DO SERVIÇO DOCKER

# Configurações iniciais da página Streamlit.
st.set_page_config(page_title="Gerenciamento de Produtos", layout="wide")

# Menu lateral de navegação.
# Adicionado 'key="main_menu"' para evitar StreamlitDuplicateElementId.
menu = option_menu(
    "Menu", ["Gerenciamento de Produtos", "Controle de Carga"],
    icons=["list", "truck"],
    menu_icon="cast", default_index=0, orientation="vertical",
    key="main_menu" # Adicionado um key único aqui
)

# --- Seção de Gerenciamento de Produtos ---
if menu == "Gerenciamento de Produtos":
    st.title("Gerenciamento de Produtos")
    st.markdown("""
    <style>
    .stButton>button {background-color: #1976d2; color: white;}
    .stTextInput>div>input {border: 1px solid #1976d2;}
    </style>
    """, unsafe_allow_html=True)

    # Inicializa variáveis de sessão se não existirem.
    # st.session_state é usado para manter o estado entre as reruns do Streamlit.
    if "show_form" not in st.session_state:
        st.session_state["show_form"] = False
    if "edit_id" not in st.session_state:
        st.session_state["edit_id"] = None

    # Botão "Novo Produto".
    # Adicionado 'key="btn_novo_produto"' para evitar duplicação de ID.
    if st.button("Novo Produto", key="btn_novo_produto"):
        st.session_state["show_form"] = True
        st.session_state["edit_id"] = None

    # Requisição GET para obter a lista de produtos do backend.
    try:
        response = requests.get(API_URL)
        response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        produtos = response.json()
    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão com o serviço de produtos. Certifique-se de que o backend está rodando em http://products-service:8000 (se usando Docker Compose) ou http://localhost:8000 (se localmente).")
        produtos = []
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar produtos: {e}")
        produtos = []

    # Configuração e exibição da tabela AgGrid.
    # O DataFrame é criado a partir da lista de produtos.
    df_produtos = pd.DataFrame(produtos)
    if df_produtos.empty:
        st.info("Nenhum produto cadastrado. Clique em 'Novo Produto' para adicionar um.")
    else:
        gb = GridOptionsBuilder.from_dataframe(df_produtos)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_default_column(editable=False)
        gb.configure_column("id", hide=True) # Esconde a coluna 'id'
        # A coluna "Ações" está configurada com cellRenderer, mas não é diretamente usada na seleção.
        # gb.configure_column("Ações", cellRenderer="agGroupCellRenderer")
        grid_options = gb.build()

        st.subheader("Lista de Produtos")
        grid_response = AgGrid(
            df_produtos,
            gridOptions=grid_options,
            enable_enterprise_modules=False,
            update_mode="NO_UPDATE",
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True, # Necessário para cellRenderer personalizado, se usado
            # Adicionado 'key' para a AgGrid, embora geralmente não seja a causa do erro de duplicação
            key="produtos_grid"
        )

        # Lógica para botões de edição e exclusão de produtos selecionados na tabela.
        selected = grid_response["selected_rows"]
        if selected:
            produto = selected[0] # Pega o primeiro produto selecionado
            col1, col2 = st.columns(2) # Cria duas colunas para os botões

            # Botão "Editar". Usa o ID do produto como parte da chave.
            if col1.button("Editar", key=f"edit_btn_{produto['id']}"):
                st.session_state["show_form"] = True
                st.session_state["edit_id"] = produto["id"]
                st.rerun() # Recarrega a página para mostrar o formulário de edição

            # Botão "Excluir". Usa o ID do produto como parte da chave.
            if col2.button("Excluir", key=f"delete_btn_{produto['id']}"):
                # Substituído st.warning com um modal de confirmação ou lógica direta,
                # pois st.warning não é uma função de bloqueio para confirmação.
                # Para uma confirmação real, você precisaria de um componente personalizado ou um workaround.
                # Aqui, vamos assumir que o clique já significa intenção de excluir para simplificar.
                # Em um app real, você pode adicionar um st.checkbox "Confirmar exclusão" antes do botão.
                
                # Exemplo de um modal de confirmação simples (não bloqueante como alert/confirm)
                if st.session_state.get(f"confirm_delete_{produto['id']}", False):
                    # Se já confirmou, procede com a exclusão
                    try:
                        delete_response = requests.delete(f"{API_URL}/{produto['id']}")
                        delete_response.raise_for_status()
                        st.success("Produto excluído com sucesso!")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro ao excluir produto: {e}")
                    st.session_state["show_form"] = False
                    st.session_state["edit_id"] = None
                    # Limpa o estado de confirmação
                    st.session_state[f"confirm_delete_{produto['id']}"] = False
                    st.rerun()
                else:
                    # Primeira vez que clica em "Excluir", mostra a mensagem de aviso e um botão de confirmação
                    st.warning("Tem certeza que deseja excluir este produto? Clique em 'Confirmar Exclusão' abaixo.")
                    if st.button("Confirmar Exclusão", key=f"confirm_delete_action_{produto['id']}"):
                        st.session_state[f"confirm_delete_{produto['id']}"] = True
                        st.rerun() # Rerun para processar a confirmação


    # Formulário de cadastro/edição de produto.
    if st.session_state.get("show_form", False):
        if st.session_state.get("edit_id"):
            # Busca o produto a ser editado na lista de produtos carregada
            produto_para_editar = next((p for p in produtos if p["id"] == st.session_state["edit_id"]), None)
            if produto_para_editar:
                st.subheader("Editar Produto")
            else:
                st.error(f"Produto com ID {st.session_state['edit_id']} não encontrado para edição.")
                st.session_state["show_form"] = False
                st.session_state["edit_id"] = None
                st.rerun()
                produto_para_editar = {"nome": "", "espaco": 0.0, "valor": 0.0} # Fallback
        else:
            produto_para_editar = {"nome": "", "espaco": 0.0, "valor": 0.0}
            st.subheader("Novo Produto")

        # O formulário é criado com um key único.
        # REMOVIDO O PRIMEIRO ARGUMENTO POSICIONAL "produto_form"
        with st.form(key="produto_cadastro_form"):
            nome = st.text_input("Nome", value=produto_para_editar["nome"], key="form_nome")
            espaco = st.number_input("Espaço", value=float(produto_para_editar["espaco"]), min_value=0.0, key="form_espaco")
            valor = st.number_input("Valor", value=float(produto_para_editar["valor"]), min_value=0.0, key="form_valor")
            
            # Botão de submissão do formulário.
            submitted = st.form_submit_button("Salvar")
            
            if submitted:
                data = {"nome": nome, "espaco": espaco, "valor": valor}
                try:
                    if st.session_state.get("edit_id"):
                        # Requisição PUT para atualizar um produto existente
                        put_response = requests.put(f"{API_URL}/{produto_para_editar['id']}", json=data)
                        put_response.raise_for_status()
                        st.success("Produto atualizado com sucesso!")
                    else:
                        # Requisição POST para criar um novo produto
                        post_response = requests.post(API_URL, json=data)
                        post_response.raise_for_status()
                        st.success("Produto criado com sucesso!")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro ao salvar produto: {e}")
                
                st.session_state["show_form"] = False
                st.session_state["edit_id"] = None
                st.rerun() # Recarrega a página para atualizar a lista de produtos

# --- Seção de Controle de Carga ---
elif menu == "Controle de Carga":
    st.title("Controle de Carga do Caminhão")
    st.markdown("""
    <style>
    .stButton>button {background-color: #1976d2; color: white;}
    .stTextInput>div>input {border: 1px solid #1976d2;}
    </style>
    """, unsafe_allow_html=True)

    # Requisição GET para obter a lista de produtos para o controle de carga.
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        produtos = response.json()
    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão com o serviço de produtos. Certifique-se de que o backend está rodando em http://products-service:8000 (se usando Docker Compose) ou http://localhost:8000 (se localmente).")
        produtos = []
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar produtos para controle de carga: {e}")
        produtos = []

    df = pd.DataFrame(produtos)
    if not df.empty:
        st.subheader("Selecione a quantidade de cada produto para o caminhão:")
        quantidade = {}
        for idx, row in df.iterrows():
            # Adicionado 'key' único para cada st.number_input de quantidade.
            quantidade[row["id"]] = st.number_input(
                f"{row['nome']} (Espaço: {row['espaco']}, Valor: {row['valor']})",
                min_value=0, value=0, key=f"qtd_{row['id']}"
            )
        
        # Adicionado 'key' único para os campos de entrada de otimização.
        limite = st.number_input("Limite de espaço do caminhão", min_value=0.0, value=3.0, key="limite_espaco")
        taxa_mutacao = st.number_input("Taxa de mutação (opcional)", min_value=0.0, max_value=1.0, value=0.01, key="taxa_mutacao")
        numero_geracoes = st.number_input("Número de gerações (opcional)", min_value=1, value=100, key="num_geracoes")
        tamanho_populacao = st.number_input("Tamanho da população (opcional)", min_value=1, value=200, key="tam_populacao")
        
        # Botão para enviar a seleção para otimização.
        # Adicionado 'key' único.
        if st.button("Enviar seleção para otimização", key="enviar_otimizacao_btn"):
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
                # URL para o serviço de otimização.
                # Se estiver rodando em Docker Compose, use o nome do serviço: "http://optimizer-service:8002/optimize/".
                # Se estiver rodando localmente, use: "http://localhost:8002/optimize/".
                optimizer_url = "http://optimizer-service:8002/optimize/"
                payload = {
                    "produtos": produtos_selecionados,
                    "limite": limite,
                    "taxa_mutacao": taxa_mutacao,
                    "numero_geracoes": numero_geracoes,
                    "tamanho_populacao": tamanho_populacao
                }
                try:
                    # Requisição POST para o serviço de otimização.
                    resp = requests.post(optimizer_url, json=payload, timeout=60)
                    resp.raise_for_status() # Levanta um erro para códigos de status HTTP ruins
                    if resp.status_code == 200:
                        resultado = resp.json()
                        st.success("Otimização realizada com sucesso!")
                        st.write(f"Espaço total: {resultado['espaco_total']:.2f}") # Formata para 2 casas decimais
                        st.write(f"Valor total: {resultado['valor_total']:.2f}")   # Formata para 2 casas decimais
                        st.subheader("Produtos selecionados:")
                        # Exibe os produtos otimizados em uma tabela.
                        st.table(pd.DataFrame(resultado["produtos"]))
                    else:
                        st.error(f"Erro ao otimizar: {resp.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com o serviço de otimização. Certifique-se de que o backend de otimização está rodando em http://localhost:8002.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro ao otimizar: {e}")
    else:
        st.info("Nenhum produto cadastrado. Cadastre produtos na seção 'Gerenciamento de Produtos' para usar o controle de carga.")
