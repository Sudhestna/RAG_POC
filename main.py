from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda


from retrieve import retrieve_logs
from memory import get_pg_chat_history

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatOllama(model="llama3.1", temperature=0.8)

# ---------------- PROMPT (ACTUALLY USED) ----------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant.\n"
        "Use the provided context if relevant.\n"
        "Do not give irrelevant information even it is in context.\n"
        "If the answer is not in the document or context is empty or history is also empty, you must say: 'Sorry, I do not have enough information to answer that.'\n\n"
        "Context:\n{context}"
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

# ---------------- RAG LOGIC ----------------
def rag_inputs(inputs: dict):
    question = inputs["question"]
    history=inputs.get("history")
    document_id=inputs.get("document_id")

    docs = retrieve_logs(question,document_id)
    context = "\n\n".join(d.page_content for d in docs)

    return {
        "question": question,
        "context": context,
        "history":history
    
    }

rag_chain= (rag_inputs|prompt | llm)


chain_with_memory = RunnableWithMessageHistory(
    rag_chain,
    get_pg_chat_history,
    input_messages_key="question",
    history_messages_key="history",
)

# ---------------- API ----------------
@app.post("/chat")
async def chat(
    query: str = Form(...),
    document_id=Form(...),
    session_id: str = Form(...)
):
    response = chain_with_memory.invoke(
        {"question": query,
        "document_id":document_id},
        config={"configurable": {"session_id": session_id}},
    )
    return {"answer": response.content}
