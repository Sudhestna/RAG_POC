from langchain.agents import create_agent
from langchain_ollama import ChatOllama
# from langchain.prompts import ChatPromptTemplate
from fastapi import *
from retrieve import retrieve_logs
from ingest_logs import ingestion
import tempfile

llm = ChatOllama(model="llama3.1", temperature=0)


# agent = create_agent(
#     llm=llm,
#     tools=[retrieve_logs],
#     system_prompt="You are a log analyzer. You must use atleast one tool.Identify the issue and provide me the solution for the issue to be resolved."
# )

# response=agent.invoke({"messages":[{"role":"user","content":"Why does my application crash?"}]})
# print(response["messages"][-1].content)


app=FastAPI()

@app.post("/chat")
async def main(query: str = Form(...),file: UploadFile | None = None):
    document_id=None
    if file:
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        
        # content = (await file.read()).decode("utf-8")
       
        document_id=ingestion(tmp_path)
        
    response=retrieve_logs(query,document_id)
    context = "\n\n".join(d.page_content for d in response)
    
    prompt=f"""
            Answer the question strictly using the document below.
            If the answer is not present, say so clearly.

            Document:
            {context}

            Question:
            {query}
            """
    result=llm.invoke(prompt).content
    # result=llm.invoke({"messages":[{"role":"user","content":"What is a game give a brief description"}]})
    return result
        
        
        
        
    
    




