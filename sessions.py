import psycopg
from config import CONNECTION_STRING



def get_all_sessions():
    print("called sessions")
    conn = psycopg.connect(CONNECTION_STRING)
    cur = conn.cursor()

    cur.execute("""
        SELECT s.session_id,(select  message FROM message_store m WHERE m.session_id = s.session_id ORDER BY id ASC LIMIT 1)
        FROM message_store s
        GROUP BY s.session_id
        ORDER BY MAX(s.id) DESC;

    """)

    sessions=[]
    labels=[]
    for row in cur.fetchall():
        sessions.append(row[0])
        if row[1]:
            labels.append(row[1]["data"]["content"][:30])
        else:
            labels.append("New Session")
        

    cur.close()
    conn.close()
    
    return {"sessions": sessions, "labels": labels}



