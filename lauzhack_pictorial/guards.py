from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers.base import BaseRouteHandler


def user_auth_guard(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    if not connection.user:
        raise NotAuthorizedException()
