# app/services/llm/llm_service.py

import os
from app.services.llm.ollama_llm import OllamaLLM
from app.services.llm.openai_llm import OpenAILLM


class LLMService:

    @staticmethod
    def get_llm():

        ENV = os.getenv("ENV", "local")

        if ENV == "local":
            return OllamaLLM(model="llama3")

        return OpenAILLM()

    @staticmethod
    def generate(prompt: str):

        llm = LLMService.get_llm()
        return llm.generate(prompt)