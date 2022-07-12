import importlib
from datetime import datetime, timedelta
from typing import Type

import app.core.errors as errors
from app.core.security.auth.base import Auth
from app.settings import Settings, get_settings
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_auth_mode(mode: str) -> Type[Auth]:
    try:
        auth_mode = importlib.import_module(f"app.core.security.auth.{mode.lower()}")
        auth_cls = getattr(auth_mode, f"{mode.lower().capitalize()}Auth")
    except ModuleNotFoundError:
        raise errors.server_error("Unable to load authentication module")
    return auth_cls


def create_access_token(data: dict, expiry: int, key: str, algorithm: str) -> bytes:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), settings: Settings = Depends(get_settings)) -> str:
    try:
        payload = jwt.decode(token, settings.AUTH_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise errors.unauth_error("Could not validate token", "Bearer")
    except JWTError:
        raise errors.unauth_error("Could not validate token", "Bearer")

    return {"username": username, "access_lvl": settings.USER_LVLS.get(username, 0)}
