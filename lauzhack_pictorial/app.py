from pathlib import Path

from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files.config import StaticFilesConfig
from litestar.template.config import TemplateConfig

from .db import repo_provider
from .middlewares import CookieAuthenticationMiddleware
from .routers import main_router

app = Litestar(
    lifespan=[repo_provider],
    route_handlers=[main_router],
    static_files_config=[
        StaticFilesConfig(directories=[Path("static_tailwind")], path="/tailwind"),
    ],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    ),
    middleware=[CookieAuthenticationMiddleware],
)
