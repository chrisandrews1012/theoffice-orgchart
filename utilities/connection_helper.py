import streamlit as st
from handler.cursor import Connection

def get_db_connection() -> Connection:
    """Get or create database connection in session state"""
    if "my_client" not in st.session_state:
        st.session_state.my_client = Connection()
    return st.session_state.my_client
