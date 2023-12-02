from pathlib import Path

# Importing important classes and functions from Litestar
from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files.config import StaticFilesConfig
from litestar.template.config import TemplateConfig

# Importing application-specific configurations and components
from .config import CONFIG
from .db import repo_provider
from .middlewares import CookieAuthenticationMiddleware
from .routers import generate_router, library_router, main_router

# Application configuration object (defined in the config module)
CONFIG


def configure_app():
    """
    Configures the Litestar application instance with the specified
    lifespan methods, route handlers, static files configuration, template
    engine configuration, and middleware.

    This function is responsible for initializing the Litestar app with all
    necessary components and configurations. It should be called to set up the
    environment before starting the web server.

    Returns:
        app (Litestar): The configured Litestar application instance.
    """
    # Create and configure the Litestar application instance
    app = Litestar(
        lifespan=[repo_provider],  # Lifespan methods for startup and shutdown
        route_handlers=[
            main_router,  # Router for the main set of routes
            generate_router,  # Router for generation-specific routes
            library_router,  # Router for library-related routes
        ],
        static_files_config=[
            StaticFilesConfig(
                directories=[Path("static")],  # Directories containing static files
                path="/static",  # URL path to serve static files
            ),
        ],
        template_config=TemplateConfig(
            directory=Path(__file__).parent / "templates",  # Path to template directory
            engine=JinjaTemplateEngine,  # Template engine to use (Jinja)
        ),
        middleware=[
            CookieAuthenticationMiddleware
        ],  # Middleware for handling cookie authentication
    )
    return app


app = configure_app()
