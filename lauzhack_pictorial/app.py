from pathlib import Path

from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files.config import StaticFilesConfig
from litestar.template.config import TemplateConfig

from .config import CONFIG
from .db import repo_provider
from .middlewares import CookieAuthenticationMiddleware
from .routers import generate_router, library_router, main_router

CONFIG

app = Litestar(
    lifespan=[repo_provider],
    route_handlers=[main_router, generate_router, library_router],
    static_files_config=[
        StaticFilesConfig(directories=[Path("static")], path="/static"),
    ],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    ),
    middleware=[CookieAuthenticationMiddleware],
)
