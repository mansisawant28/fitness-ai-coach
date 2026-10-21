import os

from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM


def get_llm(max_tokens: int = 1024):
    """
    Smart LLM selector — Ollama locally, Groq on cloud.
    """
    deployment = os.getenv("DEPLOYMENT", "local")
    if deployment == "cloud":
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=max_tokens,
            api_key=os.getenv("GROQ_API_KEY"),
        )
    else:
        llm = OllamaLLM(
            model=os.getenv("OLLAMA_MODEL", "gemma:2b"),
            temperature=0.7,
            num_predict=max_tokens,
        )
    return llm