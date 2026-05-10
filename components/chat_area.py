import streamlit as st

def render_welcome_screen():
    """Render a Copilot-style welcome screen when chat is empty"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #c9d1d9;'>Hi, I'm your Personal Assistant</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8b949e;'>I can answer questions, help you learn, and write code.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Suggestion chips
        st.button("Explain quantum computing in simple terms", use_container_width=True, on_click=lambda: set_user_input("Explain quantum computing in simple terms"))
        st.button("Write a Python script to automate file organization", use_container_width=True, on_click=lambda: set_user_input("Write a Python script to automate file organization"))
        st.button("How do I use Streamlit session state?", use_container_width=True, on_click=lambda: set_user_input("How do I use Streamlit session state?"))

def set_user_input(text):
    # This stores the suggestion to be processed
    st.session_state.suggestion_input = text

def user_message(message):
    """Display user message using Streamlit's native chat message"""
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(message)

def bot_message(message):
    """Display bot message using Streamlit's native chat message"""
    with st.chat_message("assistant", avatar="✨"):
        st.markdown(message)

def render_chat_history(chat_history):
    """Render the entire chat history or the welcome screen"""
    if not chat_history:
        render_welcome_screen()
    else:
        for message, is_bot_response in chat_history:
            if is_bot_response:
                bot_message(message)
            else:
                user_message(message)
