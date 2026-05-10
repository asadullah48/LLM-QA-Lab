"""Compare different Ollama models"""

from src.core.llm_client import LLMClient

questions = [
    "What is machine learning?",
    "What is RAG?",
    "Explain Python in one sentence"
]

models = ["gemma3:4b", "gpt-oss:20b"]

for model in models:
    print(f"\n{'='*60}")
    print(f"🤖 Testing model: {model}")
    print('='*60)
    
    # Create client with specific model
    client = LLMClient()
    client.model = model
    
    for q in questions:
        print(f"\nQ: {q}")
        response = client.generate(q)
        print(f"A: {response[:200]}...")
        print("-"*40)
