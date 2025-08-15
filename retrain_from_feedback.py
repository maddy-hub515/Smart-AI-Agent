from memory_store import load_memory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os

def retrain_from_feedback():
    all_data = load_memory()
    positive_only = [item for item in all_data if item.get("feedback") == "👍"]
    print(f"🔁 Rebuilding memory with {len(positive_only)} positive examples...")
    if not positive_only:
        print("⚠️ No 👍 examples yet.")
        return
    
    # Prepare texts
    texts = [f"Issue: {d['issue']}\nSolution: {d['solution']}" for d in positive_only]

    # Embed
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    new_vector_store = FAISS.from_texts(texts, embeddings)

    # Save it
    new_vector_store.save_local("vector_store")

    print("✅ Memory retrained successfully!")

    
    
if __name__ == "__main__":
    retrain_from_feedback()