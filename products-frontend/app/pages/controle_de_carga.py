"""Página de controle de carga."""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.produto_service import ProdutoService
from services.otimizacao_service import OtimizacaoService
from utils.ui_helpers import (
    aplicar_estilos, mostrar_erro, mostrar_sucesso, mostrar_info
)
from config import MESSAGES, PAGE_TITLE, PAGE_LAYOUT

st.set_page_config(
    page_title=f"{PAGE_TITLE} - Controle de Carga", 
    layout=PAGE_LAYOUT,
    page_icon="🚛"
)

def main():
    """Função principal da página."""
    st.title("🚛 Controle de Carga do Caminhão")
    aplicar_estilos()
    
    produto_service = ProdutoService()
    otimizacao_service = OtimizacaoService()
    
    try:
        produtos = produto_service.listar_todos()
    except ConnectionError:
        mostrar_erro("Erro de conexão com o serviço de produtos.")
        return
    except Exception as e:
        mostrar_erro(str(e))
        return
    
    if not produtos:
        mostrar_info("Nenhum produto cadastrado. Cadastre produtos primeiro na página de Gerenciamento.")
        st.info("👈 Use o menu lateral para navegar até a página de Gerenciamento de Produtos")
        return
    
    renderizar_selecao_produtos(produtos, otimizacao_service)

def renderizar_selecao_produtos(produtos, otimizacao_service):
    """Renderiza seleção de produtos e otimização."""
    
    st.subheader("📋 Produtos Disponíveis")
    df_produtos = pd.DataFrame([p.to_dict() for p in produtos])
    st.dataframe(df_produtos[['nome', 'espaco', 'valor']], use_container_width=True)
    
    st.subheader("📦 Selecione a quantidade de cada produto:")
    
    quantidades = {}
    for produto in produtos:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{produto.nome}** - Espaço: {produto.espaco} | Valor: {produto.valor}")
        with col2:
            quantidade = st.number_input(
                "Qtd",
                min_value=0,
                value=0,
                key=f"qtd_{produto.id}",
                label_visibility="collapsed"
            )
            quantidades[produto.id] = quantidade
    
    st.subheader("⚙️ Parâmetros de Otimização")
    
    col1, col2 = st.columns(2)
    
    with col1:
        limite = st.number_input(
            "🚛 Limite de espaço do caminhão", 
            min_value=0.0, 
            value=3.0,
            help="Capacidade máxima de espaço do caminhão"
        )
        taxa_mutacao = st.number_input(
            "🧬 Taxa de mutação", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.01,
            help="Taxa de mutação do algoritmo genético (0.01 = 1%)"
        )
    
    with col2:
        numero_geracoes = st.number_input(
            "🔄 Número de gerações", 
            min_value=1, 
            value=100,
            help="Número de iterações do algoritmo genético"
        )
        tamanho_populacao = st.number_input(
            "👥 Tamanho da população", 
            min_value=1, 
            value=200,
            help="Número de indivíduos por geração"
        )
    
    st.markdown("---")
    if st.button("🚀 Otimizar Carga", key="btn_otimizar", type="primary", use_container_width=True):
        executar_otimizacao(
            produtos, quantidades, limite, taxa_mutacao, 
            numero_geracoes, tamanho_populacao, otimizacao_service
        )

def executar_otimizacao(produtos, quantidades, limite, taxa_mutacao, 
                        numero_geracoes, tamanho_populacao, otimizacao_service):
    """Executa a otimização da carga."""
    
    produtos_selecionados = []
    for produto in produtos:
        quantidade = quantidades.get(produto.id, 0)
        if quantidade > 0:
            produtos_selecionados.append({
                "nome": produto.nome,
                "espaco": produto.espaco,
                "valor": produto.valor,
                "quantidade": quantidade
            })
    
    if not produtos_selecionados:
        mostrar_erro(MESSAGES["selecione_produto"])
        return
    
    with st.spinner("🔄 Executando otimização... Aguarde!"):
        try:
            resultado = otimizacao_service.otimizar_carga(
                produtos_selecionados, limite, taxa_mutacao,
                numero_geracoes, tamanho_populacao
            )
            
            exibir_resultado(resultado)
            
        except Exception as e:
            mostrar_erro(str(e))

def exibir_resultado(resultado):
    """Exibe resultado da otimização."""
    mostrar_sucesso(MESSAGES["otimizacao_sucesso"])
    
    st.markdown("---")
    st.subheader("📊 Resultado da Otimização")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "📏 Espaço Total Utilizado", 
            f"{resultado['espaco_total']:.2f}",
            help="Total de espaço ocupado pelos produtos selecionados"
        )
    
    with col2:
        st.metric(
            "💰 Valor Total", 
            f"R$ {resultado['valor_total']:.2f}",
            help="Valor total dos produtos otimizados"
        )
    
    with col3:
        eficiencia = (resultado['valor_total'] / resultado['espaco_total']) if resultado['espaco_total'] > 0 else 0
        st.metric(
            "⚡ Eficiência", 
            f"R$ {eficiencia:.2f}/unidade",
            help="Valor por unidade de espaço"
        )
    
    st.subheader("📦 Produtos Selecionados para Carregamento")
    df_resultado = pd.DataFrame(resultado["produtos"])
    
    if not df_resultado.empty:
        df_resultado['valor_total_produto'] = df_resultado['valor'] * df_resultado['quantidade']
        df_resultado['espaco_total_produto'] = df_resultado['espaco'] * df_resultado['quantidade']
        
        colunas_ordenadas = ['nome', 'quantidade', 'espaco', 'espaco_total_produto', 'valor', 'valor_total_produto']
        df_resultado = df_resultado[colunas_ordenadas]
        
        df_resultado.columns = ['Produto', 'Quantidade', 'Espaço Unit.', 'Espaço Total', 'Valor Unit.', 'Valor Total']
        
        st.dataframe(df_resultado, use_container_width=True)
        
        st.info(f"💡 **Resumo**: {len(df_resultado)} tipos de produtos selecionados para maximizar o valor da carga!")
    else:
        st.warning("Nenhum produto foi selecionado na otimização.")

if __name__ == "__main__":
    main()