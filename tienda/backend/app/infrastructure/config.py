from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_username: str
    mongodb_password: str
    mongodb_cluster: str
    mongodb_db_name: str = "tienda"
    api_cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")

    @property
    def mongodb_uri(self) -> str:
        username = quote_plus(self.mongodb_username)
        password = quote_plus(self.mongodb_password)
        return f"mongodb+srv://{username}:{password}@{self.mongodb_cluster}/{self.mongodb_db_name}?retryWrites=true&w=majority"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.api_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
