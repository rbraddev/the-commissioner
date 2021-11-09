import os
import ast
import secrets
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT: str = os.getenv("PROJECT", "FastAPI")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")

    AUTH_KEY: str = os.environ.get("AUTH_SECRET_KEY", secrets.token_urlsafe(32))
    AUTH_TOKEN_EXPIRY: int = os.environ.get("AUTH_TOKEN_EXPIRY", 30)
    TOKEN_ALGORITHM: str = os.environ.get("TOKEN_ALGORITHM", "HS256")
    AUTH_MODE: str = os.environ.get("AUTH_MODE")

    DB_URL: str = os.getenv("DB_URL", "sqlite:///database.db")

    TACACS_SVR: str = os.environ.get("TACACS_HOST", "localhost")
    TACACS_KEY: str = os.environ.get("TACACS_PLUS_KEY")

    USER_LVLS: dict = {"admin": 10, "engineer": 5, "servicedesk": 1, "readonly": 0}


@lru_cache
def get_settings() -> BaseSettings:
    return Settings()
