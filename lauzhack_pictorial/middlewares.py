from litestar.connection import ASGIConnection
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

from .db import Repository


class CookieAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        id = connection.cookies.get("pictorial-session")
        repository: Repository = connection.app.state.repository
        if id:
            user = await repository.get_user_by_id(id)
            if user:
                return AuthenticationResult(user=user, auth="cookie")

        return AuthenticationResult(user=None, auth="cookie")
