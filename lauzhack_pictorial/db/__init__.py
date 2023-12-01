from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncGenerator, Optional

import aiosql
import aiosqlite
from litestar import Litestar

from .models import Generation, User

queries = aiosql.from_path(Path(__file__).parent / "queries.sql", "aiosqlite")

__all__ = ["repo_provider"]


@dataclass
class Repository:
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

    async def create_generation(self, user_id: int, image_id: str, prompt: str) -> int:
        generation_id = await self.queries.create_generation(
            self.conn, user_id, image_id, prompt
        )
        await self.conn.commit()
        return generation_id

    async def get_user_generations(self, user_id: int) -> list[Generation]:
        generations = await self.queries.get_user_generations(self.conn, user_id)
        return [Generation(**generation) for generation in generations]


@asynccontextmanager
async def repo_provider(app: Litestar) -> AsyncGenerator[None, None]:
    conn = await aiosqlite.connect("db/db.sqlite3")
    conn.row_factory = aiosqlite.Row

    app.state.repository = Repository(conn, queries)

    try:
        yield
    finally:
        await conn.close()
