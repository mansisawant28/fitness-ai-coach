import os

from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM


def is_cloud() -> bool:
    return os.getenv("DEPLOYMENT", "cloud").strip().lower() == "cloud"


def _get_groq_api_key() -> str | None:
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return api_key

    try:
        import streamlit as st

        return st.secrets.get("GROQ_API_KEY")
    except Exception:
        return None


def get_llm(max_tokens: int = 2500):
    """Groq on cloud, Ollama locally."""
    if is_cloud():
        api_key = _get_groq_api_key()
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set in the deployment secrets.")
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=max_tokens,
            api_key=api_key,
        )
    return OllamaLLM(
        model=os.getenv("OLLAMA_MODEL", "gemma:2b"),
        temperature=0.7,
        num_predict=max_tokens,
    )