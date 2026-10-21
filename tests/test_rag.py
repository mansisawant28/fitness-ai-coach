import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm import get_llm
from chains.fitness_nutrition_chain import NUTRITION_PROMPT, WORKOUT_PROMPT, _build_prompt_chain


def test_get_llm_returns_model_instance(monkeypatch):
    monkeypatch.setenv("DEPLOYMENT", "local")
    llm = get_llm()

    assert llm is not None
    assert hasattr(llm, "invoke")


def test_cloud_mode_requires_api_key(monkeypatch):
    monkeypatch.setenv("DEPLOYMENT", "cloud")
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    try:
        get_llm()
        assert False, "Expected ValueError when GROQ_API_KEY is missing in cloud mode"
    except ValueError as exc:
        assert "GROQ_API_KEY" in str(exc)


def test_local_mode_raises_clear_error_when_model_missing(monkeypatch):
    monkeypatch.setenv("DEPLOYMENT", "local")
    monkeypatch.setenv("OLLAMA_MODEL", "definitely-missing-model:latest")

    try:
        get_llm()
        assert False, "Expected RuntimeError when Ollama model cannot be initialized"
    except RuntimeError as exc:
        assert "ollama pull" in str(exc)


def test_prompt_chains_are_constructed_correctly():
    workout_chain = _build_prompt_chain(WORKOUT_PROMPT)
    nutrition_chain = _build_prompt_chain(NUTRITION_PROMPT)

    assert hasattr(workout_chain, "invoke")
    assert hasattr(nutrition_chain, "invoke")
    assert "relevant_knowledge" in WORKOUT_PROMPT.input_variables
    assert "relevant_knowledge" in NUTRITION_PROMPT.input_variables
