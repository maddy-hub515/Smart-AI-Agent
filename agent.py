from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama
from vector_store import get_or_create_vector_store
from langchain.embeddings import HuggingFaceEmbeddings
from memory_store import search_memory, save_to_memory
from langchain.vectorstores import FAISS
import requests
import os

# Load Mistral via Ollama
def load_local_llm():
    return Ollama(model="mistral")

def smart_agent(query):

    # 1. Search memory for relevant answers
    memory_hits = search_memory(query)
    if memory_hits:
        return {"source": "memory", "results": memory_hits}
    
    # 2. Try retrained FAISS vector store (👍-only memory)
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        if os.path.exists("vector_store"):
            vector_store = FAISS.load_local("vector_store", embeddings)
            results = vector_store.similarity_search(query, k=3)
            if results:
                parsed = [parse_result(doc.page_content) for doc in results]
                return {"source": "vector_store", "results": parsed}
    except Exception as e:
        print(f"⚠️ FAISS load error: {e}")
    
    # Call Ollama's local model
    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",  # or "mistral"
            "prompt": f"Answer this issue briefly:\n{query}",
            "stream": False
        }
    )
    result_text = ollama_response.json()["response"]
    return {
        "source": "AI",
        "results": [{
            "issue": query,
            "solution": result_text
        }]
    }

# Parse FAISS document content
def parse_result(text):
    parts = text.split("\n")
    issue = parts[0].replace("Issue: ", "").strip() if len(parts) > 0 else ""
    solution = parts[1].replace("Solution: ", "").strip() if len(parts) > 1 else ""
    return {"issue": issue, "solution": solution}
