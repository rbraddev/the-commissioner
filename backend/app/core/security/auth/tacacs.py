import app.core.errors as errors
from app.core.security.auth.base import Auth
from app.settings import get_settings
from tacacs_plus.client import TACACSClient

settings = get_settings()


class TacacsAuth(Auth):
    concurrency = "sync"

    def authenticate(self) -> bool:
        try:
            client = TACACSClient(host=settings.TACACS_SVR, port=49, secret=settings.TACACS_KEY)
            return client.authenticate(self.username, self.password).valid
        except ConnectionRefusedError:
            raise errors.server_error("Unable to connect to TACACS")
