from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers.base import BaseRouteHandler


def user_auth_guard(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    """
    Guard function that checks if a user is authenticated before allowing proceeding with a request.

    This guard is designed to be used as a pre-request check within route handlers to ensure that
    the user is authorized to access the requested resource. If the user is found to be unauthorized,
    a `NotAuthorizedException` is raised, which should typically result in a 401 Unauthorized
    response being sent back to the client.

    Parameters:
        connection (ASGIConnection): The connection object representing a single HTTP request.
                                     It provides access to the request details, including the
                                     user object associated with the current connection.
        _ (BaseRouteHandler): The route handler that the guard is linked to. This argument is
                              unused in this guard function and is represented by an underscore to
                              indicate it's a placeholder. The guard function interface requires it as
                              part of the function signature, but not every guard will need it.

    Raises:
        NotAuthorizedException: If the `connection` object does not have an associated `user` attribute,
                                indicating that there is no authenticated user for the request, this
                                exception is raised to signify an unauthorized access attempt.

    Usage:
        - This guard function should be added to routes that require user authentication.
        - It should be used together with the route handler registration process. For example:
            ```
            app = Litestar(...)
            app.get("/protected", pre_request=user_auth_guard)(protected_route_handler)
            ```

    Note:
        - Ensure that your route handlers and middleware correctly populate the `user` attribute
          within the `connection` object. Typically, this involves a middleware that authenticates
          users and attaches the user information to the connection for later use by route handlers
          and guard functions.
    """

    # Check if there is a user associated with the current connection.
    # The `user` attribute should be set elsewhere, likely by an authentication middleware.
    if not connection.user:
        # If no user is found, raise the `NotAuthorizedException` to indicate that the user
        # is not authorized to perform the requested operation.
        raise NotAuthorizedException()
