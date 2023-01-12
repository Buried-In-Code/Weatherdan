__all__ = [
    "__version__",
    "get_project_root",
    "get_cache_root",
    "get_config_root",
    "get_data_root",
    "setup_logging",
]

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler
from rich.traceback import install

from common.console import CONSOLE

__version__ = "0.2.0"


def get_cache_root() -> Path:
    cache_home = os.getenv("XDG_CACHE_HOME", default=str(Path.home() / ".cache"))
    folder = Path(cache_home).resolve() / "weatherdan"
    folder.mkdir(exist_ok=True, parents=True)
    return folder


def get_config_root() -> Path:
    config_home = os.getenv("XDG_CONFIG_HOME", default=str(Path.home() / ".config"))
    folder = Path(config_home).resolve() / "weatherdan"
    folder.mkdir(exist_ok=True, parents=True)
    return folder


def get_data_root() -> Path:
    data_home = os.getenv("XDG_DATA_HOME", default=str(Path.home() / ".local" / "share"))
    folder = Path(data_home).resolve() / "weatherdan"
    folder.mkdir(exist_ok=True, parents=True)
    return folder


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def setup_logging(debug: bool = False) -> None:
    install(show_locals=True, console=CONSOLE)
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
