from openai import AzureOpenAI
from app.providers.base import AIProvider

class AzureOpenAIProvider(AIProvider):
    name = "azure_openai"
    def __init__(self, api_key: str, endpoint: str, api_version: str, deployment: str, embedding_deployment: str):
        self.client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)
        self.deployment = deployment
        self.embedding_deployment = embedding_deployment
    def embed(self, text: str) -> list[float]:
        return self.client.embeddings.create(model=self.embedding_deployment, input=text).data[0].embedding
    def generate(self, prompt: str) -> str:
        r = self.client.chat.completions.create(model=self.deployment, messages=[{"role":"user","content":prompt}])
        return r.choices[0].message.content or ""
