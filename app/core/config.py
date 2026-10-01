from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "postgresql+psycopg://rag:rag@localhost:5432/rag"
    llm_provider: str = "local"
    embedding_provider: str = "local"
    top_k: int = 4
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.1"
    openai_embedding_model: str = "text-embedding-3-small"
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_deployment: str | None = None
    azure_openai_embedding_deployment: str | None = None
    aws_region: str = "eu-central-1"
    bedrock_model_id: str | None = None
    bedrock_embedding_model_id: str | None = None

settings = Settings()
