import google.generativeai as genai
from app.services.llm.base import BaseLLM

class GeminiLLM(BaseLLM):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
