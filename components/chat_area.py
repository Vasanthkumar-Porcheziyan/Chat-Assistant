import streamlit as st

def user_message(message):
    """Display user message using Streamlit's native chat message"""
    with st.chat_message("user", avatar="👤"):
        st.markdown(message)

def bot_message(message):
    """Display bot message using Streamlit's native chat message"""
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(message)

def render_chat_history(chat_history):
    """Render the entire chat history"""
    for message, is_bot_response in chat_history:
        if is_bot_response:
            bot_message(message)
        else:
            user_message(message)
