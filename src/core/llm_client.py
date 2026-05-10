import json
import urllib.request
import urllib.error
from typing import Optional

class LLMClient:
    """Multi-provider LLM client with real Ollama support"""
    
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or "ollama"
        self.host = "http://127.0.0.1:11434"
        self.model = "gemma3:4b"
        self.use_mock = False
        
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from LLM"""
        if not self.use_mock and self.provider == "ollama":
            response = self._call_ollama(prompt)
            if response and not response.startswith("[ERROR]"):
                return response
        
        # Fallback to mock
        return self._mock_llm(prompt)
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API"""
        url = f"{self.host}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9
            }
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            print(f"[OLLAMA] Calling with model: {self.model}...")
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('response', '')
        except urllib.error.URLError as e:
            print(f"[WARNING] Ollama not reachable: {e}")
            print("   Make sure Ollama is running: 'ollama serve'")
            self.use_mock = True
            return ""
        except Exception as e:
            print(f"[WARNING] Ollama error: {e}")
            return ""
    
    def _mock_llm(self, prompt: str) -> str:
        """Mock LLM for testing without real API"""
        print("[MOCK] Using mock LLM (install Ollama for real responses)")
        
        # Smart mock responses
        if "machine learning" in prompt.lower():
            return "Machine learning enables systems to learn from data."
        elif "what is rag" in prompt.lower() or "rag?" in prompt.lower():
            return "RAG is Retrieval-Augmented Generation for enhanced LLM responses."
        elif "python" in prompt.lower():
            return "Python is a high-level programming language."
        else:
            return f"[Mock] Response to: {prompt[:100]}..."

# Global client instance
llm_client = LLMClient()
