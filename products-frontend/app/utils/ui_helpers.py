"""Helpers para interface de usuário."""

import streamlit as st
from config import BUTTON_STYLE, SESSION_SHOW_FORM, SESSION_EDIT_ID, SESSION_DELETE_CONFIRMATION

def aplicar_estilos():
    """Aplica estilos CSS."""
    st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

def inicializar_sessao():
    """Inicializa estado da sessão."""
    if SESSION_SHOW_FORM not in st.session_state:
        st.session_state[SESSION_SHOW_FORM] = False
    if SESSION_EDIT_ID not in st.session_state:
        st.session_state[SESSION_EDIT_ID] = None
    if SESSION_DELETE_CONFIRMATION not in st.session_state:
        st.session_state[SESSION_DELETE_CONFIRMATION] = None

def limpar_formulario():
    """Limpa estado do formulário."""
    st.session_state[SESSION_SHOW_FORM] = False
    st.session_state[SESSION_EDIT_ID] = None
    st.session_state[SESSION_DELETE_CONFIRMATION] = None

def mostrar_erro(mensagem: str):
    """Exibe erro."""
    st.error(mensagem)

def mostrar_sucesso(mensagem: str):
    """Exibe sucesso."""
    st.success(mensagem)

def mostrar_info(mensagem: str):
    """Exibe informação."""
    st.info(mensagem)