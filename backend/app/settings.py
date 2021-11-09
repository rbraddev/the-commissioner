import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT: str = os.getenv("PROJECT", "FastAPI")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")

    DB_URL: str = os.getenv("DB_URL", "sqlite:///database.db")


@lru_cache
def get_settings() -> BaseSettings:
    return Settings()
