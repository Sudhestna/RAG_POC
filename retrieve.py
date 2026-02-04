from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_postgres import PGVector
from config import *
from langchain.tools import tool


def retrieve_logs(query: str,document_id: str | None = None):
    print("document_name",document_id)
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    vector_store = PGVector(
        connection=CONNECTION_STRING,
        embeddings=embeddings,
        collection_name="Company_documents"
    )


    search_kwargs = {"k":6}

    if document_id.strip():
        search_kwargs["filter"] = {
            "document_id": document_id
        }

    # retriever = vector_store.as_retriever(search_kwargs=search_kwargs)
    # response = retriever.invoke(query)
    response = vector_store.similarity_search_with_score(query,**search_kwargs)
    
    threshold = 0.4# Set your desired threshold for similarity score
    filtered_docs = [
        doc for doc, score in response if score <= threshold
    ]
    print("Retreiving is done")
    print("Filtered Docs:",filtered_docs)
    return filtered_docs



