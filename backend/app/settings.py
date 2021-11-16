from typing import *
from ast import literal_eval
import os
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
    SYNC_DB_URL: str = os.getenv("SYNC_DB_URL", "sqlite:///database.db")

    TACACS_SVR: str = os.environ.get("TACACS_HOST", "localhost")
    TACACS_KEY: str = os.environ.get("TACACS_PLUS_KEY")

    API_USER: str = os.environ.get("API_USER")
    API_PASSWORD: str = os.environ.get("API_PASSWORD")

    USER_LVLS: Dict[str, int] = os.environ.get("USER_LVLS")

    REDIS_SERVER: str = os.environ.get("REDIS_SERVER")

    TEMPLATE_DIR: str = os.environ.get("TEMPLATE_DIR", "./app/templates")

    SITE_VLANS: List[int] = literal_eval(os.environ.get("SITE_VLANS"))

    DATA_VLAN: int = os.environ.get("DATA_VLAN")

    TASK_DEACTIVATE_SITES: List[str] = literal_eval(
        os.environ.get("TASK_DEACTIVATE_SITES")
    )


@lru_cache
def get_settings() -> BaseSettings:
    return Settings()
