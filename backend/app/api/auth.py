from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.settings import get_settings, Settings
from app.core.security.utils import get_auth_mode, create_access_token, get_current_user
from app.models.token import Token, User


router = APIRouter()
httpbasic = HTTPBasic()


@router.post("/token", response_model=Token)
async def get_access_token(
    credentials: HTTPBasicCredentials = Depends(httpbasic),
    settings: Settings = Depends(get_settings),
):
    auth_mode = get_auth_mode(settings.AUTH_MODE)
    auth = auth_mode(credentials.username, credentials.password)

    await auth.aauthenticate() if auth_mode.concurrency == "async" else auth.authenticate()

    access_token = create_access_token(
        data={"sub": credentials.username},
        expiry=settings.AUTH_TOKEN_EXPIRY,
        key=settings.AUTH_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/user", response_model=User)
async def current_user(current_user: User = Depends(get_current_user)):
    return current_user
