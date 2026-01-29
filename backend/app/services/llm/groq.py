from groq import Groq
from app.services.llm.base import BaseLLM

class GroqLLM(BaseLLM):
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def generate(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
