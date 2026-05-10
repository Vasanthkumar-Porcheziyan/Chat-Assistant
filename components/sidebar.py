import streamlit as st
from services.chat_manager import get_all_sessions

def render_sidebar():
    """Render the sidebar with navigation and settings"""
    with st.sidebar:
        # New Chat Button
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            st.session_state.current_chat_id = None
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Conversation History
        st.markdown("<p style='font-size: 0.85rem; color: #b392f0; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>Recent Chats</p>", unsafe_allow_html=True)
        
        sessions = get_all_sessions()
        if sessions:
            for session in sessions:
                chat_id = session['session_id']
                title = session.get("title", "New Chat")
                # Highlight the active chat differently via CSS or text styling
                prefix = "💬" if str(chat_id) != str(st.session_state.current_chat_id) else "🔹"
                if st.button(f"{prefix} {title}", key=f"chat_{chat_id}", use_container_width=True):
                    st.session_state.current_chat_id = str(chat_id)
                    st.rerun()
        else:
            st.caption("No recent chats.")
            
        st.divider()
        
        st.markdown("<p style='font-size: 0.85rem; color: #b392f0; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>Settings</p>", unsafe_allow_html=True)
        
        # Model selection
        available_models = [
            "google/gemma-2-2b-it",
            "nvidia/nemotron-3-super-120b-a12b:free",
            "meta/llama-3.1-8b-instruct",
            "microsoft/phi-3-mini-128k-instruct",
            "anthropic/claude-3-haiku"
        ]
        
        # Initialize selected model in session state if not present
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = available_models[0]
        
        selected_model = st.selectbox(
            "Language Model",
            options=available_models,
            index=available_models.index(st.session_state.selected_model) if st.session_state.selected_model in available_models else 0,
            key="model_selectbox",
            help="Select the AI model to power the chat."
        )
        
        # Update session state if model changed
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            st.rerun()
        
        st.divider()
        
        # Quick settings expander
        with st.expander("Generation Parameters", expanded=False):
            if "llm_settings" not in st.session_state:
                st.session_state.llm_settings = {
                    "temperature": 0.2,
                    "top_p": 0.7,
                    "max_tokens": 1024
                }
            
            # Temperature slider
            temp = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.llm_settings["temperature"],
                step=0.1,
                help="Controls randomness: Lower = more deterministic, Higher = more creative"
            )
            
            # Top-p slider
            top_p = st.slider(
                "Top-P",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.llm_settings["top_p"],
                step=0.05,
                help="Nucleus sampling: Lower = more conservative, Higher = more diverse"
            )
            
            # Max tokens selector
            max_tokens = st.selectbox(
                "Max Tokens",
                options=[256, 512, 1024, 2048, 4096],
                index=[256, 512, 1024, 2048, 4096].index(st.session_state.llm_settings["max_tokens"]) if st.session_state.llm_settings["max_tokens"] in [256, 512, 1024, 2048, 4096] else 2,
                help="Maximum length of generated response"
            )
            
            # Update settings if changed
            if (temp != st.session_state.llm_settings["temperature"] or 
                top_p != st.session_state.llm_settings["top_p"] or 
                max_tokens != st.session_state.llm_settings["max_tokens"]):
                st.session_state.llm_settings = {
                    "temperature": temp,
                    "top_p": top_p,
                    "max_tokens": max_tokens
                }
                st.rerun()
        
        # Add some spacing
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # App info
        st.caption("Personal Chat Assistant v1.1")
        st.caption("UI Theme: Dark Mode")