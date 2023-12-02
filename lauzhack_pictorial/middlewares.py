from litestar.connection import ASGIConnection
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

from .db import Repository


class CookieAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    """
    Middleware that handles authentication via cookies.

    This middleware extends AbstractAuthenticationMiddleware and implements
    authentication logic that inspects the incoming request for a session cookie
    to authenticate the user. If the cookie is present and corresponds to a valid
    user, the `authenticate_request` coroutine sets the user object in the
    authentication result.

    If no valid session is found, or the user cannot be authenticated, the
    result will indicate an anonymous or unauthenticated request. Typically,
    this would be one of multiple authentication mechanisms in the application.

    Usage:
        - This middleware should be added to the middleware stack during the
          application setup. For example:
            ```
            app = Litestar(middleware=[CookieAuthenticationMiddleware])
            ```

    Note:
        - The specific cookie name ('pictorial-session' in this case) used to store the
          session identifier should be consistent with the cookie set during the login process.
        - The Repository dependency is expected to be attached to the application state,
          and provides methods such as `get_user_by_id` to retrieve user information
          from the database.
    """

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        """
        Coroutine that checks for a user's session cookie and attempts to authenticate them.

        It retrieves a 'pictorial-session' cookie from the incoming connection, uses
        it to look up the user in the database, and constructs an AuthenticationResult
        accordingly.

        Parameters:
            connection (ASGIConnection): The connection object for the incoming request.

        Returns:
            AuthenticationResult: The result of the authentication attempt, containing
                                  a user object if authentication was successful, and
                                  an auth type (in this case, 'cookie').
        """
        # Retrieve the session ID from the 'pictorial-session' cookie.
        id = connection.cookies.get("pictorial-session")

        # Access the application state to get the repository for database operations.
        repository: Repository = connection.app.state.repository

        # If a session ID is present, query the repository for the associated user.
        if id:
            user = await repository.get_user_by_id(id)
            # If a user is found, return a successful AuthenticationResult.
            if user:
                return AuthenticationResult(user=user, auth="cookie")

        # If authentication fails, return an AuthenticationResult indicating no user.
        return AuthenticationResult(user=None, auth="cookie")
