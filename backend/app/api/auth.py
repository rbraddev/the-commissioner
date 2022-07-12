from app.core.security.utils import create_access_token, get_auth_mode, get_current_user
from app.core import errors
from app.db import get_engine
from app.models.auth import Token, User
from app.models.logs import AuthLogs
from app.settings import Settings, get_settings
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session
from datetime import datetime

router = APIRouter()
httpbasic = HTTPBasic()


@router.post("/token", response_model=Token)
async def get_access_token(
    credentials: HTTPBasicCredentials = Depends(httpbasic),
    settings: Settings = Depends(get_settings),
):
    auth_mode = get_auth_mode(settings.AUTH_MODE)
    auth = auth_mode(credentials.username, credentials.password)

    authenticated = await auth.aauthenticate() if auth_mode.concurrency == "async" else auth.authenticate()

    with Session(get_engine()) as session:
        session.add(
            AuthLogs(
                time=datetime.now(),
                username=credentials.username,
                success=authenticated,
            )
        )
        session.commit()

    if not authenticated:
        raise errors.unauth_error("Incorrect username or password", "Basic")

    access_token = create_access_token(
        data={"sub": credentials.username},
        expiry=settings.AUTH_TOKEN_EXPIRY,
        key=settings.AUTH_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "userdata": {
            "username": credentials.username,
            "access_lvl": settings.USER_LVLS.get(credentials.username),
        },
    }


@router.get("/user", response_model=User)
async def current_user(current_user: User = Depends(get_current_user)):
    return current_user
