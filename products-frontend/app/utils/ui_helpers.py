"""
UI Helpers Module.

This module provides utility functions for Streamlit UI components,
including session management, styling, and message display functions.
"""

import streamlit as st
from config import (
    BUTTON_STYLE,
    SESSION_SHOW_FORM,
    SESSION_EDIT_ID,
    SESSION_DELETE_CONFIRMATION
)


def aplicar_estilos() -> None:
    """
    Apply CSS styles to the Streamlit application.

    Injects custom CSS styles defined in BUTTON_STYLE into the page.
    """
    st.markdown(BUTTON_STYLE, unsafe_allow_html=True)


def inicializar_sessao() -> None:
    """
    Initialize session state variables.

    Sets up default values for session state variables used
    throughout the application for form management.
    """
    if SESSION_SHOW_FORM not in st.session_state:
        st.session_state[SESSION_SHOW_FORM] = False
    if SESSION_EDIT_ID not in st.session_state:
        st.session_state[SESSION_EDIT_ID] = None
    if SESSION_DELETE_CONFIRMATION not in st.session_state:
        st.session_state[SESSION_DELETE_CONFIRMATION] = None


def limpar_formulario() -> None:
    """
    Clear form state variables.

    Resets all form-related session state variables to their
    default values, effectively clearing the form.
    """
    st.session_state[SESSION_SHOW_FORM] = False
    st.session_state[SESSION_EDIT_ID] = None
    st.session_state[SESSION_DELETE_CONFIRMATION] = None


def mostrar_erro(mensagem: str) -> None:
    """
    Display error message.

    Args:
        mensagem: Error message to display
    """
    st.error(mensagem)


def mostrar_sucesso(mensagem: str) -> None:
    """
    Display success message.

    Args:
        mensagem: Success message to display
    """
    st.success(mensagem)


def mostrar_info(mensagem: str) -> None:
    """
    Display info message.

    Args:
        mensagem: Info message to display
    """
    st.info(mensagem)
