import streamlit as st
from sqlalchemy import text

def get_db_connection():
    """
    Initialize and return a connection to the PostgreSQL database
    using Streamlit's st.connection abstraction.
    """
    try:
        # Uses credentials defined in .streamlit/secrets.toml
        conn = st.connection("postgresql", type="sql")
        return conn
    except Exception as e:
        st.error(f"Failed to connect to the database: {e}")
        return None

def init_db(conn):
    """
    Initialize tables if they do not exist.
    """
    if conn is None:
        return
    
    with conn.session as s:
        s.execute(text(
            '''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id UUID PRIMARY KEY,
                user_id UUID,
                building_id UUID,
                title TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
            '''
        ))
        s.execute(text(
            '''
            CREATE TABLE IF NOT EXISTS chat_messages (
                message_id BIGSERIAL PRIMARY KEY,
                session_id UUID REFERENCES chat_sessions(session_id),
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                metadata JSONB,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            '''
        ))
        s.commit()
