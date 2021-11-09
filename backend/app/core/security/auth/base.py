import app.core.errors as errors


class Auth:
    def __init__(self, username: str, password: str):
        if "" in [username, password]:
            raise errors.unauth_error("Incorrect username or password", "Basic")

        self.username: str = username
        self.password: str = password

    def authenticate(self) -> NotImplemented:
        return NotImplemented

    async def aauthenticate(self) -> NotImplemented:
        return NotImplemented
