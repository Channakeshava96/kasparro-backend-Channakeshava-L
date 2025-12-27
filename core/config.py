from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    database_url: str
    coinpaprika_api_key: str = "your_default_api_key_here"

    model_config = ConfigDict()

@lru_cache
def get_settings() -> Settings:
    return Settings()

