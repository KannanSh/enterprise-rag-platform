import json
import boto3
from app.providers.base import AIProvider

class BedrockProvider(AIProvider):
    name = "bedrock"
    def __init__(self, region: str, model_id: str, embedding_model_id: str):
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = model_id
        self.embedding_model_id = embedding_model_id
    def embed(self, text: str) -> list[float]:
        body = json.dumps({"inputText": text})
        r = self.client.invoke_model(modelId=self.embedding_model_id, body=body)
        return json.loads(r["body"].read())["embedding"]
    def generate(self, prompt: str) -> str:
        body = json.dumps({"inputText": prompt})
        r = self.client.invoke_model(modelId=self.model_id, body=body)
        data = json.loads(r["body"].read())
        return data.get("results", [{}])[0].get("outputText", "")
