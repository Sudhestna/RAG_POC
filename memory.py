from langchain_postgres import PostgresChatMessageHistory
from config import CONNECTION_STRING
import psycopg
MAX_HISTORY_MESSAGES = 7

def get_pg_chat_history(session_id: str):
    conn = psycopg.connect(CONNECTION_STRING)
    history =  PostgresChatMessageHistory(
        "message_store",
        session_id,
        sync_connection=conn
    )
    
    messages = history.messages
    if len(messages) > MAX_HISTORY_MESSAGES:
        history.messages = messages[-MAX_HISTORY_MESSAGES:]

    return history
