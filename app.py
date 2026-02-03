import streamlit as st
import requests
import uuid
from config import doc_map

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Company Policy Assistant")

# ---------- SESSION ----------
if "view" not in st.session_state:
    st.session_state.view = "main"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "selected_doc_id" not in st.session_state:
    st.session_state.selected_doc_id = None
    
if "upload_session_id" not in st.session_state:
    st.session_state.upload_session_id=str(uuid.uuid4())

# ---------- HEADER ----------
col1, col2 = st.columns([6, 1])
with col1:
    st.title("Company Policy Assistant")
with col2:
    if st.button("Upload PDF"):
        st.session_state.view = "upload"
        
        st.rerun()

# ---------------- Sidebar ----------------
st.sidebar.title("Chats")

sessions_res = requests.get(f"{API_BASE}/sessions")
sessions = sessions_res.json().get("sessions")


if st.sidebar.button("New Chat"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []

st.sidebar.divider()


for sess_id in sessions:
    label = sess_id[:8] 
    if st.sidebar.button(label, key=sess_id):
        st.session_state.session_id = sess_id

        
        res = requests.get(f"{API_BASE}/sessions/{sess_id}")
        st.session_state.messages = res.json().get("messages")

# ================= MAIN CHAT =================
if st.session_state.view == "main":

    doc_names = ["-- Select a document --"] + list(doc_map.keys())
    selected = st.selectbox("Select a document", doc_names)

    if selected == "-- Select a document --":
        st.info("Select a document")
        st.stop()

    document_id = doc_map[selected]
    if st.session_state.selected_doc_id != document_id:
        st.session_state.selected_doc_id = document_id
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask about the document")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(
                f'<div class="user-msg">{user_input}</div>',
                unsafe_allow_html=True
            )

    # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(
                        f"{API_BASE}/chat",
                        data={
                            "query": user_input,
                            "document_id": st.session_state.selected_doc_id,
                            "session_id": st.session_state.session_id,
                        },
                    )
                    answer = res.json().get("answer", "No answer returned")

                except Exception as e:
                    answer = f"Error: {e}"

                st.markdown(
                f'<div class="bot-msg">{answer}</div>',
                unsafe_allow_html=True
                )   

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )


# ================= UPLOAD CHAT =================
if st.session_state.view == "upload":

    if st.button("<-Back"):
        st.session_state.view = "main"
        st.rerun()

    uploaded = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded:
        if "upload_doc_id" not in st.session_state:
            with st.spinner("Processing document..."):
                res = requests.post(
                    f"{API_BASE}/upload",
                    files={"file": uploaded}
                )
                st.session_state.upload_doc_id = res.json()["document_id"]
                st.session_state.upload_messages = []

        for msg in st.session_state.upload_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_input = st.chat_input("Ask about uploaded document")

        if user_input:
            st.session_state.upload_messages.append(
                {"role": "user", "content": user_input}
            )

            with st.chat_message("user"):
                st.markdown(
                f'<div class="user-msg">{user_input}</div>',
                unsafe_allow_html=True
            )

    # Assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        res = requests.post(
                            f"{API_BASE}/chat",
                            data={
                                "query": user_input,
                                "document_id": st.session_state.upload_doc_id,
                                "session_id": st.session_state.upload_session_id,
                            },
                        )
                        answer = res.json().get("answer", "No answer returned")

                    except Exception as e:
                        answer = f"Error: {e}"

                    st.markdown(
                    f'<div class="bot-msg">{answer}</div>',
                    unsafe_allow_html=True
                    )   

            st.session_state.upload_messages.append(
                {"role": "assistant", "content": answer}
            )
