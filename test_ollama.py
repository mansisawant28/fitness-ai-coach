from langchain_ollama import OllamaLLM

# Connect to your local Ollama model
llm = OllamaLLM(model="gemma:2b")

# Send a test prompt
response = llm.invoke("Give me a 3 day beginner workout plan for fat loss. Be concise.")

print("=" * 50)
print("✅ Ollama connected successfully!")
print("=" * 50)
print(response)