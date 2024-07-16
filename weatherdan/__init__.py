__all__ = [
    "__version__",
    "get_project_root",
    "get_cache_root",
    "get_config_root",
    "get_data_root",
    "setup_logging",
    "elapsed_timer",
]

import logging
import os
from contextlib import contextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path
from timeit import default_timer

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme
from rich.traceback import install

__version__ = "0.6.3"
CONSOLE = Console(
    theme=Theme(
        {
            "prompt": "green",
            "prompt.choices": "cyan",
            "prompt.default": "dim cyan",
            "logging.level.debug": "dim white",
            "logging.level.info": "white",
            "logging.level.warning": "yellow",
            "logging.level.error": "bold red",
            "logging.level.critical": "bold magenta",
        }
    )
)


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
    install(show_locals=True, max_frames=5, console=CONSOLE)
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
                show_time=False,
                show_path=False,
                console=CONSOLE,
            ),
            RotatingFileHandler(
                filename=log_folder / "weatherdan.log", maxBytes=100000000, backupCount=3
            ),
        ],
    )

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)


@contextmanager
def elapsed_timer() -> float:
    start = default_timer()
    elapser = lambda: default_timer() - start  # noqa: E731
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end - start  # noqa: E731
