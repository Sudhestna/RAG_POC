import psycopg
from config import CONNECTION_STRING



def get_all_sessions():
    print("called sessions")
    conn = psycopg.connect(CONNECTION_STRING)
    cur = conn.cursor()

    cur.execute("""
        SELECT session_id
        FROM message_store
        GROUP BY session_id
        ORDER BY MAX(id) DESC;

    """)

    sessions = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return sessions

