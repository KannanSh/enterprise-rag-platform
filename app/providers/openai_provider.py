from openai import OpenAI
from app.providers.base import AIProvider

class OpenAIProvider(AIProvider):
    name = "openai"
    def __init__(self, api_key: str, model: str, embedding_model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.embedding_model = embedding_model
    def embed(self, text: str) -> list[float]:
        return self.client.embeddings.create(model=self.embedding_model, input=text).data[0].embedding
    def generate(self, prompt: str) -> str:
        r = self.client.responses.create(model=self.model, input=prompt)
        return r.output_text
