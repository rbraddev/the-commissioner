from tacacs_plus.client import TACACSClient

from app.core.security.auth.base import Auth
from app.settings import get_settings
import app.core.errors as errors


settings = get_settings()


class TacacsAuth(Auth):
    concurrency = "sync"

    def authenticate(self) -> None:
        try:
            client = TACACSClient(
                host=settings.TACACS_SVR, port=49, secret=settings.TACACS_KEY
            )
            if not client.authenticate(self.username, self.password).valid:
                raise errors.unauth_error("Incorrect username or password", "Basic")
        except ConnectionRefusedError:
            raise errors.server_error("Unable to connect to TACACS")
