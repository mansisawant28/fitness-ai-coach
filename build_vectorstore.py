import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from rag.vectorstore import build_vectorstore

if __name__ == "__main__":
    print("🚀 Building fitness knowledge vector store...")
    vectorstore = build_vectorstore()
    print("✅ Done! Vector store is ready.")
    print("📁 Saved to: data/processed/faiss_index")