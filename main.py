import streamlit as st
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv(".env.local")

# Import components
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_area import render_chat_history

# Import services
from services.llm_service import generate_bot_response
from services.chat_manager import (
    initialize_chat_state, 
    get_current_history, 
    create_new_chat, 
    add_message, 
    prepare_messages_for_llm
)
from services.connect_postgresdb import get_db_connection, init_db

# Random processing messages for the spinner
PROCESSING_MESSAGES = [
    "🤖 Processing your message...",
    "⏳ Analyzing your input...",
    "🧠 Thinking deeply...",
    "⚡ Running inference...",
    "📊 Generating response...",
    "🔄 Processing request...",
    "💭 Crafting a response...",
    "🚀 Computing answer...",
    "📡 Contacting AI engine...",
    "⌛ Working on that...",
]

# Define the main Streamlit app
def main():
    st.set_page_config(page_title="Personal Chat Assistant", page_icon="🤖", layout="wide")
    
    # Load custom CSS with error handling
    try:
        with open("styles/dark_theme.css") as f:
            css_content = f.read()
            # Only apply CSS if file is not empty
            if css_content.strip():
                st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Silently continue if CSS file not found
    except Exception:
        pass  # Silently continue on any other error
    
    # Initialize Database
    conn = get_db_connection()
    init_db(conn)
    
    # Initialize chat session state variables
    initialize_chat_state()
    
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "google/gemma-2-2b-it"
    
    if "llm_settings" not in st.session_state:
        st.session_state.llm_settings = {
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1024,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Display chat history
    current_history = get_current_history()
    render_chat_history(current_history)
    
    # Input field for user to enter a message
    user_input = st.chat_input("Your Message:")
    
    # Handle suggestion input if clicked
    if "suggestion_input" in st.session_state and st.session_state.suggestion_input:
        user_input = st.session_state.suggestion_input
        st.session_state.suggestion_input = ""  # Clear after taking
        
    # Handle user input
    if user_input:
        if not st.session_state.current_chat_id:
            # Create a new conversation
            create_new_chat(user_input)
            
        # Add user message to chat history
        add_message(user_input, is_bot=False)
        
        # Prepare messages for API call
        messages = prepare_messages_for_llm()
        
        # Show loading indicator with random message while generating response
        random_message = random.choice(PROCESSING_MESSAGES)
        with st.spinner(random_message):
            bot_response = generate_bot_response(
                messages, 
                st.session_state.selected_model, 
                st.session_state.llm_settings
            )
        
        # Add bot response to chat history
        add_message(bot_response, is_bot=True)
        
        # Rerun to update the chat display
        st.rerun()

# Run the app
if __name__ == "__main__":
    main()