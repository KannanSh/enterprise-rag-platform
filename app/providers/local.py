import hashlib, math, re
from app.providers.base import AIProvider

class LocalProvider(AIProvider):
    name = "local"
    dims = 1536
    def embed(self, text: str) -> list[float]:
        # Deterministic demo embedding: enables a zero-key local environment.
        vec = [0.0] * self.dims
        for token in re.findall(r"[a-z0-9]+", text.lower()):
            idx = int(hashlib.sha256(token.encode()).hexdigest(), 16) % self.dims
            vec[idx] += 1.0
        norm = math.sqrt(sum(x*x for x in vec)) or 1.0
        return [x / norm for x in vec]
    def generate(self, prompt: str) -> str:
        return "Local demo mode: based on the retrieved context, " + prompt.split("Question:", 1)[-1].strip()
