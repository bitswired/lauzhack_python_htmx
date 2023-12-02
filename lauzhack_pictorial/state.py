from typing import Optional

from litestar.datastructures import State

from lauzhack_pictorial.db import Repository


class AppState(State):
    """
    AppState extends the default State class provided by the Litestar framework
    to include application-specific state, such as the database repository.

    The AppState class is designed to be a container for shared data that needs
    to be accessible across different parts of the application, such as during
    request handling.

    Attributes:
        repository (Repository, optional): An instance of the Repository class,
                                           which provides access to database
                                           operations. Having it as an optional
                                           attribute allows for lazy loading or
                                           conditional initialization.
    """

    repository: Optional[Repository]
