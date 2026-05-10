import streamlit as st

def render_header():
    """Render the application header with title"""
    html = """
    <div id="custom-fixed-header">
        <h3 style='margin:0; padding:0; font-weight: 600; font-size: 1.25rem; background: linear-gradient(90deg, #58a6ff, #b392f0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🤖 Personal Chat Assistant
        </h3>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)