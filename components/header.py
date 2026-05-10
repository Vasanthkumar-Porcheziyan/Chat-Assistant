import streamlit as st

def render_header():
    """Render the application header with title"""
    html = """
    <div id="custom-fixed-header">
        <h3 style='margin:0; padding:0; color:#c9d1d9;'>🤖 Personal Chat Assistant</h3>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)