
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from pdf_loader import load_documents
import os

PERSIST_DIR = "faiss_index"
PDF_PATH = "data/usp_addressSearch_guide.pdf"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def store_documents(docs, persist_dir=PERSIST_DIR):
    
    db = FAISS.from_documents(docs,embeddings,allow_dangerous_deserialization=True)
    db.save_local(persist_dir)
    return db

def load_vector_store(persist_dir=PERSIST_DIR):
    return FAISS.load_local(persist_dir,embeddings,allow_dangerous_deserialization=True)

def get_or_create_vector_store():
    if not os.path.exists(PERSIST_DIR):
        docs = load_documents(PDF_PATH)
        return store_documents(docs)
    return load_vector_store()