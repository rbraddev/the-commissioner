from pydantic import BaseModel


class User(BaseModel):
    username: str
    access_lvl: int


class Token(BaseModel):
    access_token: str
    token_type: str
    userdata: User
