from litestar.connection import ASGIConnection
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

from .db import Repositopry, db_conn


class CookieAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        id = connection.cookies.get("pictorial-session")
        repository: Repositopry = connection.app.state.repository
        if id:
            async with db_conn() as (conn, queries):
                user = await repository.get_user_by_id(id)
                if user:
                    return AuthenticationResult(user=user, auth="cookie")

        return AuthenticationResult(user=None, auth="cookie")
