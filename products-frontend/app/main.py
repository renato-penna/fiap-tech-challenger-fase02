"""
Main Application - Home Page.

This module contains the main Streamlit application for the products management
system. It provides the home page with navigation and system overview.
"""

import streamlit as st

from config import PAGE_TITLE, PAGE_LAYOUT


def main() -> None:
    """
    Main application page.
    
    Sets up the page configuration and displays the home page with
    system overview and navigation instructions.
    """
    st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT)
    
    st.title("Products Management System")
    
    st.markdown("""
    ## Welcome to the Products Management System
    
    This system allows:
    
    ### 📦 Product Management
    - Register new products
    - Edit existing products
    - Delete products
    - View complete product list
    
    ### 🚛 Cargo Control
    - Select products for optimization
    - Configure optimization parameters
    - Execute genetic algorithm to maximize cargo value
    - View optimization results
    
    ---
    
    ### How to use:
    1. **Navigate** using the sidebar menu
    2. **Manage** your products in the corresponding section
    3. **Optimize** the truck cargo as needed
    
    """)


if __name__ == "__main__":
    main()