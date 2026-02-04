import psycopg
from config import CONNECTION_STRING

def get_messages_for_session(session_id: str):
    conn = psycopg.connect(CONNECTION_STRING)
    cur = conn.cursor()

    cur.execute("""
        SELECT message
        FROM message_store
        WHERE session_id = %s
        ORDER BY id ASC
    """, (session_id,))
    messages = []
    for row in cur.fetchall():
        msg = row[0]
        messages.append({
            "role": msg["type"],
            "content": msg["data"]["content"]
        })
        

    for msg in messages:
        if msg["role"]=="human":
            msg["role"]="user"
        elif msg["role"]=="ai":
            msg["role"]="assistant"
        
    
    cur.close()
    conn.close()

    return {"messages":messages}
