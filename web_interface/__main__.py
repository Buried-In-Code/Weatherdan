import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from rich.logging import RichHandler

from common import __version__, get_project_root
from common.console import CONSOLE
from web_interface.routers.api import router as api_router
from web_interface.routers.html import router as html_router

LOGGER = logging.getLogger("Pydex")


def setup_logging(debug: bool = False):
    logging.getLogger("uvicorn").handlers.clear()
    logging.basicConfig(
        format="%(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]",
        level=logging.DEBUG if debug else logging.INFO,
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                log_time_format="[%Y-%m-%d %H:%M:%S]",
                omit_repeated_times=False,
                console=CONSOLE,
            )
        ],
    )


setup_logging()


def create_app() -> FastAPI:
    app = FastAPI(name="Weather-Dan", version=__version__)
    app.include_router(html_router)
    app.include_router(api_router)
    return app


app = create_app()
app.mount(
    "/static", StaticFiles(directory=get_project_root() / "static"), name="static"
)
