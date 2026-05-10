import streamlit as st

@st.dialog("⚙️ Advanced Settings")
def render_settings_modal():
    """Render the settings modal for advanced LLM parameters"""
    # Initialize settings in session state if not present
    if "llm_settings" not in st.session_state:
        st.session_state.llm_settings = {
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1024,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
    
    # Settings form
    with st.form("settings_form"):
        # Temperature
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=st.session_state.llm_settings["temperature"],
            step=0.1,
            help="Controls randomness in generation. Lower values make the model more deterministic, higher values make it more creative."
        )
        
        # Top-p
        top_p = st.slider(
            "Top-P (Nucleus Sampling)",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.llm_settings["top_p"],
            step=0.05,
            help="Controls diversity via nucleus sampling. Lower values focus on more probable tokens, higher values consider more tokens."
        )
        
        # Max tokens
        max_tokens = st.selectbox(
            "Max Tokens",
            options=[128, 256, 512, 1024, 2048, 4096],
            index=[128, 256, 512, 1024, 2048, 4096].index(st.session_state.llm_settings["max_tokens"]) if st.session_state.llm_settings["max_tokens"] in [128, 256, 512, 1024, 2048, 4096] else 3,
            help="Maximum number of tokens to generate in the response."
        )
        
        # Frequency penalty
        frequency_penalty = st.slider(
            "Frequency Penalty",
            min_value=-2.0,
            max_value=2.0,
            value=st.session_state.llm_settings["frequency_penalty"],
            step=0.1,
            help="Penalizes repeated tokens. Lower values encourage repetition, higher values discourage it."
        )
        
        # Presence penalty
        presence_penalty = st.slider(
            "Presence Penalty",
            min_value=-2.0,
            max_value=2.0,
            value=st.session_state.llm_settings["presence_penalty"],
            step=0.1,
            help="Penalizes tokens based on whether they appear in the text so far. Encourages model to talk about new topics."
        )
        
        # Form buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            submitted = st.form_submit_button("💾 Save Settings", use_container_width=True)
        with col2:
            reset = st.form_submit_button("🔄 Reset to Defaults", use_container_width=True)
        
        # Handle form submissions
        if submitted:
            st.session_state.llm_settings = {
                "temperature": temperature,
                "top_p": top_p,
                "max_tokens": max_tokens,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty
            }
            st.rerun()
        
        if reset:
            st.session_state.llm_settings = {
                "temperature": 0.2,
                "top_p": 0.7,
                "max_tokens": 1024,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
            st.rerun()