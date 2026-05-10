import yaml
from pathlib import Path
from typing import Dict, Any
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    llm_default_provider: str = "ollama"
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "gemma3:4b"
    openai_model: str = "gpt-4o-mini"
    anthropic_model: str = "claude-3-haiku-20240307"
    groq_model: str = "llama3-70b-8192"
    
    class Config:
        env_file = ".env"
        env_prefix = "QA_LAB_"

class ConfigLoader:
    """Load and manage configuration"""
    
    def __init__(self, config_path: str = "config/default.yaml"):
        self.config_path = Path(config_path)
        self.settings = Settings()
        self.config = self._load_yaml()
        
    def _load_yaml(self) -> Dict[str, Any]:
        """Load YAML configuration"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                print(f"Error loading config: {e}")
                return {}
        return {}
    
    def get(self, key: str, default=None):
        """Get configuration value with environment override"""
        # Check environment first
        parts = key.split('.')
        
        # Convert to environment variable format
        env_key = f"QA_LAB_{key.upper().replace('.', '_')}"
        env_value = getattr(self.settings, env_key.lower(), None)
        
        if env_value is not None:
            return env_value
            
        # Fall back to YAML
        value = self.config
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part, default)
            else:
                return default
        return value

# Global config instance
config = ConfigLoader()
