from langchain_huggingface import HuggingFaceEmbeddings
import os

def get_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},   # use CPU (works on all machines)
        encode_kwargs={"normalize_embeddings": True}
    )
    return embeddings