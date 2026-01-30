from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_postgres import PGVector
from config import *
from langchain.tools import tool

@tool
def retrieve_logs(query: str,document_id: str | None = None):
    """ Use this tool to retrieve relevant parts of the uploaded document."""

    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    vector_store = PGVector(
        connection=CONNECTION_STRING,
        embeddings=embeddings,
        collection_name="Company_documents"
    )


    search_kwargs = {"k":5}

    if document_id:
        search_kwargs["filter"] = {
            "document_id": document_id
        }

    retriever = vector_store.as_retriever(search_kwargs=search_kwargs)
    response = retriever.invoke(query)
    # response = vector_store.similarity_search_with_score(query,**search_kwargs)
    
    # threshold = 0.5 # Set your desired threshold for similarity score
    # filtered_docs = [
    #     doc for doc, score in response if score >= threshold
    # ]
    print("Retreiving is done")
    return response



