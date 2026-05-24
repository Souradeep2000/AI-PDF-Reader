# app/services/llm/llm_service.py

import os
from app.services.llm.ollama_llm import OllamaLLM
from app.services.llm.gemini_llm import GeminiLLM


class LLMService:

    @staticmethod
    def get_llm():

        ENV = os.getenv("ENV", "local")

        if ENV == "local":
            return OllamaLLM(model="qwen2.5:3b")

        return GeminiLLM()

    @staticmethod
    def generate(prompt: str):

        llm = LLMService.get_llm()
        return llm.generate(prompt)
    
    @staticmethod
    def stream_generate(prompt: str):

        llm = LLMService.get_llm()

        return llm.stream_generate(prompt)