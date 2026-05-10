import streamlit as st
from components.settings_modal import render_settings_modal

def render_header():
    """Render the application header with title and settings button"""
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("🤖 Personal Chat Assistant")
    with col2:
        if st.button("⚙️ Settings", key="settings_button"):
            render_settings_modal()