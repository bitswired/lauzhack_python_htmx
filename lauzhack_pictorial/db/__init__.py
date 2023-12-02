from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncGenerator, Optional

import aiosql
import aiosqlite
from litestar import Litestar

from .models import Generation, User

# Load SQL queries from queries.sql file using aiosql.
queries = aiosql.from_path(Path(__file__).parent / "queries.sql", "aiosqlite")

__all__ = ["repo_provider"]


@dataclass
class Repository:
    """
    A data repository class that provides asynchronous methods for interacting with the database.

    It utilizes aiosqlite to execute SQL queries defined in a separate SQL file.
    The Repository class acts as an abstraction layer over the SQLite database,
    providing convenience methods for common operations.

    Args:
        conn (aiosqlite.Connection): An asynchronous connection to the SQLite database.
        queries (Any): Loaded SQL queries using aiosql.

    Returns:
        Provides a series of asynchronous methods for database operations such as getting users,
        creating users, or creating generations. Each method returns the appropriate pydantic model.
    """

    conn: aiosqlite.Connection
    queries: Any

    async def get_users(self) -> list[User]:
        """Retrieve a list of all users in the database."""
        users = await self.queries.get_users(self.conn)
        return [User(**user) for user in users]

    async def get_user_by_credentials(
        self, email: str, password: str
    ) -> Optional[User]:
        """Get a user from the database based on email and password."""
        user = await self.queries.get_user_by_credentials(self.conn, email, password)
        return User(**user) if user else None

    async def get_user_by_id(self, id: int) -> Optional[User]:
        """Get a user from the database based on user ID."""
        user = await self.queries.get_user_by_id(self.conn, id)
        return User(**user) if user else None

    async def create_user(self, email: str, password: str) -> int:
        """Create a new user in the database and returns the user ID."""
        user_id = await self.queries.create_user(self.conn, email, password)
        await self.conn.commit()
        return user_id

    async def create_generation(self, user_id: int, image_id: str, prompt: str) -> int:
        """Create a new generation record associated with the user."""
        generation_id = await self.queries.create_generation(
            self.conn, user_id, image_id, prompt
        )
        await self.conn.commit()
        return generation_id

    async def get_user_generations(self, user_id: int) -> list[Generation]:
        """Retrieve a list of generations associated with the user."""
        generations = await self.queries.get_user_generations(self.conn, user_id)
        return [Generation(**generation) for generation in generations]


@asynccontextmanager
async def repo_provider(app: Litestar) -> AsyncGenerator[None, None]:
    """
    An asynchronous context manager for providing a repository object to the application.

    It opens a database connection when entering the context and closes it upon exiting.
    The repository instantiated within this context is set in the application's state
    for easy access during request handling.

    Args:
        app (Litestar): An instance of the Litestar application.

    Yields:
        None: While yielding, the application has access to the repository.

    Ensures that the database connection is closed after the completion of the request lifecycle.
    """
    conn = await aiosqlite.connect("db/db.sqlite3")
    conn.row_factory = aiosqlite.Row

    app.state.repository = Repository(conn, queries)

    try:
        yield
    finally:
        await conn.close()
