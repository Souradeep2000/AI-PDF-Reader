# app/services/llm/ollama_llm.py

import requests
from app.services.llm.base import BaseLLM

class OllamaLLM(BaseLLM):

    def __init__(self, model: str = "llama3"):
        self.url = "http://ollama:11434/api/chat"
        self.model = model

    def generate(self, prompt: str) -> str:

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }

        res = requests.post(self.url, json=payload, timeout=120)
        res.raise_for_status()
        
        data = res.json()
        return data.get(
            "message",
            {}
        ).get(
            "content",
            "No response generated."
        )