import re
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_postgres import PGVector
from config import *
from langchain_community.document_loaders import PyMuPDFLoader
import os



def ingestion(file):
    print("entered")
    document_id = str(uuid.uuid4())
    texts=[]
    metadatas=[]
    loader=PyMuPDFLoader(file)
    print("loader completed")
    documents=loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    for doc in chunks:
        doc.metadata["document_id"]=document_id

    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    try:
        vector_store = PGVector(
            connection=CONNECTION_STRING,
            embeddings=embeddings,
            collection_name="Company_documents"
        )
    except Exception as e:
        return e

    vector_store.add_documents(chunks)

    print("Document ingestion completed")
    return document_id

