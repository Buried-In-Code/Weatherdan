__all__ = ["__version__", "get_project_root", "get_cache_root", "get_config_root", "setup_logging"]

import logging
from importlib.metadata import version
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
