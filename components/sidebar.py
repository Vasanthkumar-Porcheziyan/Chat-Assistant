import streamlit as st

def render_sidebar():
    """Render the sidebar with model selection and info"""
    with st.sidebar:
        st.header("🤖 Model Settings")
        
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
            "Select Model",
            options=available_models,
            index=available_models.index(st.session_state.selected_model) if st.session_state.selected_model in available_models else 0,
            key="model_selectbox"
        )
        
        # Update session state if model changed
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            st.rerun()
        
        # Display current model info
        st.info(f"**Current Model:** {st.session_state.selected_model}")
        
        # Quick settings expander
        with st.expander("⚙️ Quick Settings", expanded=False):
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
        st.divider()
        
        # App info
        st.caption("Personal Chat Assistant v1.0")
        st.caption("Built with Streamlit")