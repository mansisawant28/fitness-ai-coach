from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.embeddings import get_embeddings
import os

# Path where we store the FAISS index
VECTORSTORE_PATH = "data/processed/faiss_index"
RAW_DATA_PATH = "data/raw"

def load_documents():
    loader = DirectoryLoader(
        RAW_DATA_PATH,
        glob="**/*.txt",          # load all .txt files
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} documents")
    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Split into {len(chunks)} chunks")
    return chunks

def build_vectorstore():
    print("🔨 Building vector store...")

    # Step 1 and 2
    documents = load_documents()
    chunks = split_documents(documents)

    # Step 3 and 4
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Step 5 — save to disk
    os.makedirs("data/processed", exist_ok=True)
    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"✅ Vector store saved to {VECTORSTORE_PATH}")

    return vectorstore

def load_vectorstore():
    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("✅ Vector store loaded from disk")
    return vectorstore

def get_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        return load_vectorstore()
    else:
        return build_vectorstore()