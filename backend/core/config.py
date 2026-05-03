from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # == FASTAPI APP CONFIG ==
    debug: bool
    title: str
    description: str
    version: str

    # == FRONTEND CONFIG ==
    templates_path: str
    assets_url: str
    assets_path: str
    assets_app_name: str

    # == MONGODB CONFIG ==
    cluster: str
    username: str
    password: str

    # This tells Pydantic to read from the .env file
    model_config = SettingsConfigDict(env_file=".env")


# Singleton (cached instance)
@lru_cache
def get_settings() -> Settings:
    return Settings()




