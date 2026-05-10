import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv(".env.local")

# Import components
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_area import render_chat_history

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

def generate_bot_response(messages, model, settings):
    """Generate bot response using selected model and settings"""
    client = OpenAI(
        base_url=os.getenv("NVIDIA_BASE_URL"),
        api_key=os.getenv("NVIDIA_API_KEY")
    )

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=settings["temperature"],
        top_p=settings["top_p"],
        max_tokens=settings["max_tokens"],
        stream=True
    )

    bot_response = ""
    for chunk in completion:
        if chunk.choices and chunk.choices[0].delta.content is not None:
            bot_response += chunk.choices[0].delta.content
    return bot_response

# Define the main Streamlit app
def main():
    st.set_page_config(page_title="Personal ChatBot", page_icon="🤖", layout="wide")
    
    # Load custom CSS with error handling
    try:
        with open("styles/copilot_theme.css") as f:
            css_content = f.read()
            # Only apply CSS if file is not empty
            if css_content.strip():
                st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Silently continue if CSS file not found
    except Exception:
        pass  # Silently continue on any other error
    
    # Initialize session state
    if "chat_history" not in st.session_state:
        message = "Let's start chatting! 👇"
        st.session_state.chat_history = [(message, True)]  # List of tuples (message, is_bot_response)
    
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
    render_chat_history(st.session_state.chat_history)
    
    # Input field for user to enter a message
    user_input = st.chat_input("Your Message:")
    
    # Handle user input
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append((user_input, False))
        
        # Prepare messages for API call
        messages = [{"role": "user", "content": msg} if not is_bot else {"role": "assistant", "content": msg} 
                   for msg, is_bot in st.session_state.chat_history]
        
        # Show loading indicator with random message while generating response
        random_message = random.choice(PROCESSING_MESSAGES)
        with st.spinner(random_message):
            bot_response = generate_bot_response(
                messages, 
                st.session_state.selected_model, 
                st.session_state.llm_settings
            )
        
        # Add bot response to chat history
        st.session_state.chat_history.append((bot_response, True))
        
        # Rerun to update the chat display
        st.rerun()

# Run the app
if __name__ == "__main__":
    main()