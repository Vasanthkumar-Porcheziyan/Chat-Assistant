import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import random

load_dotenv(".env.local")

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

# Function to display user messages with rounded rectangle borders
def user_message(message):
    st.markdown(f'<div class="user-message" style="display: flex; justify-content: flex-end; width: 100%; padding: 5px; gap: 8px;">'
                f'<div data-testid="stChatMessageAvatarAssistant" class="st-emotion-cache-jmw8un"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-file-person" viewBox="0 0 16 16"><path d="M12 1a1 1 0 0 1 1 1v10.755S12 11 8 11s-5 1.755-5 1.755V2a1 1 0 0 1 1-1zM4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z"></path><path d="M8 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6"></path></svg></div>'
                f'<div style="background-color: #63196b; color: white; padding: 10px; border-radius: 10px; font-size:18px; margin-bottom:10px; max-width: 70%; word-wrap: break-word; overflow-wrap: break-word;">{message}</div>'
                f'</div>', unsafe_allow_html=True)

# Function to display bot messages with rounded rectangle borders
def bot_message(message):
    st.markdown(f'<div class="bot-message" style="display: flex; width: 100%; padding: 5px; gap: 8px;">'
                f'<div data-testid="stChatMessageAvatarAssistant" class="st-emotion-cache-jmw8un"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp53 st-emotion-cache-1b2ybts ex0cdmw0"><rect width="24" height="24" fill="none"></rect><path d="M20 9V7c0-1.1-.9-2-2-2h-3c0-1.66-1.34-3-3-3S9 3.34 9 5H6c-1.1 0-2 .9-2 2v2c-1.66 0-3 1.34-3 3s1.34 3 3 3v4c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-4c1.66 0 3-1.34 3-3s-1.34-3-3-3zm-2 10H6V7h12v12zm-9-6c-.83 0-1.5-.67-1.5-1.5S8.17 10 9 10s1.5.67 1.5 1.5S9.83 13 9 13zm7.5-1.5c0 .83-.67 1.5-1.5 1.5s-1.5-.67-1.5-1.5.67-1.5 1.5-1.5 1.5.67 1.5 1.5zM8 15h8v2H8v-2z"></path></svg></div>'
                f'<div style="background-color: #074c85; color: white; padding: 10px; border-radius: 10px; font-size:18px; margin-bottom:10px; max-width: 70%; word-wrap: break-word; overflow-wrap: break-word;">{message}</div>'
                f'</div>', unsafe_allow_html=True)

def generate_bot_response(messages):
    # Placeholder for bot response generation logic
    # You can replace this with actual logic to generate a response based on the user's message
    client = OpenAI(
    base_url = os.getenv("NVIDIA_BASE_URL"),
    api_key = os.getenv("NVIDIA_API_KEY")
    )

    completion = client.chat.completions.create(
    model="google/gemma-2-2b-it",
    messages=messages,
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=True
    )

    bot_response = ""
    for chunk in completion:
        if chunk.choices and chunk.choices[0].delta.content is not None:
            bot_response += chunk.choices[0].delta.content
    return bot_response

# Define the main Streamlit app
def main(i):
    st.set_page_config(page_title="Personal ChatBot", page_icon="🤖", layout="wide")
    st.title("Personal Chat Assistant")
    # Initialize chat history using session state
    if "chat_history" not in st.session_state:
        message = "Let's start chatting! 👇"
        bot_message(message)
        st.session_state.chat_history = [(message, True)]  # List of tuples (message, is_bot_response)

    # JavaScript to scroll to the bottom
    scroll_script = """
    <script>
    setTimeout(() => {
    const container = window.parent.document.querySelector('section.main');
    if (container) {
    container.scrollTop = container.scrollHeight || 999999;
    }
    }, 200);
    </script>
    <style>
    .st-emotion-cache-jmw8un { 
        display: flex;
        width: 2rem;
        height: 2rem;
        flex-shrink: 0;
        border-radius: 0.5rem;
        -webkit-box-align: center;
        -webkit-box-pack: center;
        justify-content: center;
        background-color: rgb(255, 189, 69);
        color: rgb(14, 17, 23);
        align-items: center;
    }
    </style>
    """
    
    st.markdown(scroll_script, unsafe_allow_html=True)

    # Input field for user to enter a message
    user_input = st.chat_input("Your Message:")
    # Button to send the user's message
    if user_input:
        # Display previous chat messages
        for message, is_bot_response in st.session_state.chat_history:
            if is_bot_response:
                bot_message(message)
            else:
                user_message(message)
        # Add the user's message to the chat history
        st.session_state.chat_history.append((user_input, False))

        # Display the user's message
        user_message(user_input)

        # Prepare the messages for the API call by extracting only the text from the chat history
        messages = [{"role": "user", "content": msg} if not is_bot else {"role": "assistant", "content": msg} for msg, is_bot in st.session_state.chat_history]

        # Show loading indicator with random message while generating response
        random_message = random.choice(PROCESSING_MESSAGES)
        with st.spinner(random_message):
            bot_response = generate_bot_response(messages)

        # Add the bot's response to the chat history
        st.session_state.chat_history.append((bot_response, True))
        
        # Display the bot's response
        bot_message(bot_response)
    
# Run the app
if __name__ == "__main__":
    main(0)