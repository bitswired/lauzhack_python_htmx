from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncGenerator, Optional

import aiosql
import aiosqlite
from litestar import Litestar

from .models import User

queries = aiosql.from_path(Path(__file__).parent / "queries.sql", "aiosqlite")

__all__ = ["db_conn", "db_provider", "models"]


@asynccontextmanager
async def db_conn() -> AsyncGenerator[aiosqlite.Connection, Any]:
    conn = await aiosqlite.connect("db/db.sqlite3")
    conn.row_factory = aiosqlite.Row

    try:
        yield conn, queries
    finally:
        await conn.close()


@asynccontextmanager
async def db_provider(app: Litestar) -> AsyncGenerator[None, None]:
    conn = await aiosqlite.connect("db/db.sqlite3")
    conn.row_factory = aiosqlite.Row

    app.state.conn = conn
    app.state.queries = queries

    try:
        yield
    finally:
        await conn.close()


@dataclass
class Repositopry:
    conn: aiosqlite.Connection
    queries: Any

    async def get_users(self) -> list[User]:
        users = await self.queries.get_users(self.conn)
        return [User(**user) for user in users]

    async def get_user_by_credentials(
        self, email: str, password: str
    ) -> Optional[User]:
        user = await self.queries.get_user_by_credentials(self.conn, email, password)
        return User(**user) if user else None

    async def get_user_by_id(self, id: int) -> Optional[User]:
        user = await self.queries.get_user_by_id(self.conn, id)
        return User(**user) if user else None

    async def create_user(self, email: str, password: str) -> int:
        user_id = await self.queries.create_user(self.conn, email, password)
        await self.conn.commit()
        return user_id


@asynccontextmanager
async def repo_provider(app: Litestar) -> AsyncGenerator[None, None]:
    conn = await aiosqlite.connect("db/db.sqlite3")
    conn.row_factory = aiosqlite.Row

    app.state.repository = Repositopry(conn, queries)

    try:
        yield
    finally:
        await conn.close()
