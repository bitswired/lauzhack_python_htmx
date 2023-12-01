from typing import Optional

from litestar.datastructures import State

from lauzhack_pictorial.db import Repository


class AppState(State):
    repository: Optional[Repository]
