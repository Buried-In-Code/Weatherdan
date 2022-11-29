__all__ = ["__version__", "get_project_root", "get_cache_root", "get_config_root", "setup_logging"]

import logging
from importlib.metadata import version
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler

from common.console import CONSOLE

__version__ = version("weatherdan")


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_cache_root() -> Path:
    root = Path.home() / ".cache" / "weatherdan"
    root.mkdir(parents=True, exist_ok=True)
    return root


def get_config_root() -> Path:
    root = Path.home() / ".config" / "weatherdan"
    root.mkdir(parents=True, exist_ok=True)
    return root


def setup_logging(debug: bool = False):
    log_folder = get_project_root() / "logs"
    log_folder.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)-8s] {%(name)s} | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if debug else logging.INFO,
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                omit_repeated_times=False,
                show_level=False,
                show_path=False,
                show_time=False,
                console=CONSOLE,
            ),
            RotatingFileHandler(
                filename=log_folder / "Weatherdan.log", maxBytes=100000000, backupCount=3
            ),
        ],
    )
