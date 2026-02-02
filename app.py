import streamlit as st
import requests
import uuid
from config import doc_map

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="RAG Chat", layout="centered")
st.markdown("""
<style>
.user-msg {
    align-self: flex-end;
    color: black;
    padding: 10px 14px;
    border-radius: 12px;
    margin: 6px 0;
    text-align: right;
}

.bot-msg {
    align-self: flex-start;
    background-color: #F1F0F0;
    color: black;
    padding: 10px 14px;
    margin: 6px 0;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)


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
        # st.session_state.messages = []
        # st.session_state.session_id = str(uuid.uuid4())

st.divider()

# ---------------- CHAT AREA ----------------
if st.session_state.selected_doc_id is None:
    st.info("Select a document")
    st.stop()

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(
                f'<div class="user-msg">{msg["content"]}</div>',
                unsafe_allow_html=True
            )
    else:
        with st.chat_message("assistant"):
            st.markdown(
                f'<div class="bot-msg">{msg["content"]}</div>',
                unsafe_allow_html=True
            )

user_input = st.chat_input("Ask something about the document")

if user_input:
    # User message
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
