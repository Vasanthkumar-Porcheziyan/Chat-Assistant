import streamlit as st
import uuid
from sqlalchemy import text
from services.connect_postgresdb import get_db_connection

def get_all_sessions():
    """Fetch all chat sessions from the database ordered by newest first."""
    conn = get_db_connection()
    if conn is None:
        return []
    
    try:
        # Cache query results to reduce DB load
        df = conn.query(
            "SELECT session_id, title FROM chat_sessions ORDER BY created_at DESC", 
            ttl="2s"
        )
        return df.to_dict('records')
    except Exception as e:
        # Avoid showing errors if tables are just not created yet
        # st.error(f"Error fetching sessions: {e}")
        return []

def initialize_chat_state():
    """Initialize session state variables related to chat management."""
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None

def get_current_history():
    """Retrieve the current active chat history from the database."""
    if not st.session_state.current_chat_id:
        return []
        
    conn = get_db_connection()
    if conn is None:
        return []
        
    try:
        # The ttl="1s" ensures we don't cache stale data right after sending a message
        df = conn.query(
            "SELECT role, message FROM chat_messages WHERE session_id = :session_id ORDER BY created_at ASC",
            params={"session_id": st.session_state.current_chat_id},
            ttl="1s"
        )
        
        # return list of tuples (message, is_bot)
        history = []
        for row in df.itertuples():
            is_bot = (row.role == "assistant")
            history.append((row.message, is_bot))
        return history
    except Exception as e:
        return []

def create_new_chat(first_message):
    """Create a new conversation session based on the first message."""
    session_id = str(uuid.uuid4())
    title = first_message[:30] + "..." if len(first_message) > 30 else first_message
    
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn.session as s:
                s.execute(text(
                    "INSERT INTO chat_sessions (session_id, title) VALUES (:session_id, :title)"
                ), {"session_id": session_id, "title": title})
                s.commit()
            st.session_state.current_chat_id = session_id
            # Bust the cached session list so the sidebar refreshes immediately
            st.cache_data.clear()
        except Exception as e:
            st.error(f"Error creating new chat: {e}")
            
    return session_id

def add_message(message_content, is_bot=False):
    """Add a message to the current active chat history in database."""
    if not st.session_state.current_chat_id:
        return
        
    role = "assistant" if is_bot else "user"
    conn = get_db_connection()
    
    if conn is not None:
        try:
            with conn.session as s:
                s.execute(text(
                    """
                    INSERT INTO chat_messages (session_id, role, message) 
                    VALUES (:session_id, :role, :message)
                    """
                ), {
                    "session_id": st.session_state.current_chat_id, 
                    "role": role, 
                    "message": message_content
                })
                
                # Also update the chat_session updated_at timestamp
                s.execute(text(
                    """
                    UPDATE chat_sessions 
                    SET updated_at = NOW() 
                    WHERE session_id = :session_id
                    """
                ), {
                    "session_id": st.session_state.current_chat_id
                })
                s.commit()
        except Exception as e:
            st.error(f"Error adding message: {e}")

def prepare_messages_for_llm():
    """Format history for the LLM API call."""
    history = get_current_history()
    return [{"role": "user", "content": msg} if not is_bot else {"role": "assistant", "content": msg} 
            for msg, is_bot in history]
