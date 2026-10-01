from abc import ABC, abstractmethod

class AIProvider(ABC):
    name: str
    @abstractmethod
    def embed(self, text: str) -> list[float]: ...
    @abstractmethod
    def generate(self, prompt: str) -> str: ...
