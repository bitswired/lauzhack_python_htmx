from pathlib import Path

from litestar import Litestar, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files.config import StaticFilesConfig
from litestar.template.config import TemplateConfig

from .filtering_sorting_router import filtering_sorting_router
from .form_submission_router import form_submission_router
from .live_data_router import live_data_router


@get()
async def index_view() -> Template:
    return Template(
        template_name="index.html",
    )


app = Litestar(
    route_handlers=[
        index_view,
        live_data_router,
        form_submission_router,
        filtering_sorting_router,
    ],
    static_files_config=[
        StaticFilesConfig(directories=[Path("static")], path="/static"),
    ],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    ),
)
