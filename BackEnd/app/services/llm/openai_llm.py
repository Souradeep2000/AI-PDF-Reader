# app/services/llm/openai_llm.py

from openai import OpenAI
from app.services.llm.base import BaseLLM
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAILLM(BaseLLM):

    def generate(self, prompt: str) -> str:

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return res.choices[0].message.content