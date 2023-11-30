from typing import Optional

from litestar.datastructures import State

from lauzhack_pictorial.db import Repositopry


class AppState(State):
    repository: Optional[Repositopry]
