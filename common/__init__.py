__all__ = [
    "__version__",
    "get_project_root",
    "get_cache_root",
    "get_config_root",
]

from importlib.metadata import version
from pathlib import Path

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
