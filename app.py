import streamlit as st
import requests
import uuid
from config import doc_map

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="RAG Chat", layout="centered")

# ---------------- Session setup ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_doc_id" not in st.session_state:
    st.session_state.selected_doc_id = None


# ---------------- HEADER (FIXED) ----------------
st.title("Company Policy Assistant")

doc_names = ["-- Select a document --"] + list(doc_map.keys())

selected_doc_name = st.selectbox(
    "Select a document",
    doc_names,
    index=0
)

# Handle document selection
if selected_doc_name == "-- Select a document --":
    st.session_state.selected_doc_id = None
    st.session_state.messages = []
else:
    new_doc_id = doc_map[selected_doc_name]

    # Reset chat if document changed
    if st.session_state.selected_doc_id != new_doc_id:
        st.session_state.selected_doc_id = new_doc_id
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())

st.divider()

# ---------------- CHAT AREA ----------------
if st.session_state.selected_doc_id is None:
    st.info("Select a document")
    st.stop()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask something about the document")

if user_input:
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.write(user_input)

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

            st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
