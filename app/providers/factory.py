from app.core.config import settings
from app.providers.local import LocalProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.azure_provider import AzureOpenAIProvider
from app.providers.bedrock_provider import BedrockProvider

def get_provider(name: str | None = None):
    p = (name or settings.llm_provider).lower()
    if p == "local": return LocalProvider()
    if p == "openai":
        if not settings.openai_api_key: raise ValueError("OPENAI_API_KEY is required")
        return OpenAIProvider(settings.openai_api_key, settings.openai_model, settings.openai_embedding_model)
    if p == "azure_openai":
        required = [settings.azure_openai_api_key, settings.azure_openai_endpoint, settings.azure_openai_deployment, settings.azure_openai_embedding_deployment]
        if not all(required): raise ValueError("Azure OpenAI settings are incomplete")
        return AzureOpenAIProvider(*required[:1], *required[1:]) if False else AzureOpenAIProvider(settings.azure_openai_api_key, settings.azure_openai_endpoint, settings.azure_openai_api_version, settings.azure_openai_deployment, settings.azure_openai_embedding_deployment)
    if p == "bedrock":
        if not settings.bedrock_model_id or not settings.bedrock_embedding_model_id: raise ValueError("Bedrock model settings are incomplete")
        return BedrockProvider(settings.aws_region, settings.bedrock_model_id, settings.bedrock_embedding_model_id)
    raise ValueError(f"Unsupported provider: {p}")
