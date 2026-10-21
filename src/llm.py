import os

from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM


def _ensure_local_model_exists(model_name: str):
    """Validate that the configured Ollama model is actually installed and available."""
    try:
        import ollama
    except ImportError as exc:
        raise RuntimeError("The 'ollama' Python package is required for local model validation.") from exc

    try:
        installed_models = ollama.list()
    except Exception as exc:
        raise RuntimeError(
            "Ollama is not running or is unavailable. Start it with 'ollama serve' "
            "and make sure the model is installed."
        ) from exc

    available = set()
    for model in installed_models.get("models", []):
        name = model.get("name") or model.get("model")
        if name:
            available.add(name)

    if model_name not in available:
        raise RuntimeError(
            f"Local Ollama model '{model_name}' is not installed. "
            f"Run: 'ollama pull {model_name}'"
        )


def get_llm(max_tokens: int = 1024):
    """
    Smart LLM selector — Ollama locally, Groq on cloud.
    """
    deployment = os.getenv("DEPLOYMENT", "local")
    if deployment == "cloud":
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is required when DEPLOYMENT=cloud.")

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=max_tokens,
            api_key=groq_api_key,
        )
        return llm

    model_name = os.getenv("OLLAMA_MODEL", "gemma:2b")
    _ensure_local_model_exists(model_name)

    llm = OllamaLLM(
        model=model_name,
        temperature=0.7,
        num_predict=max_tokens,
    )
    return llm