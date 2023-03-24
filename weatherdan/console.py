__all__ = ["CONSOLE", "date_to_str"]

from datetime import date

from rich.console import Console
from rich.theme import Theme

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
        },
    ),
)


def date_to_str(value: date) -> str:
    return value.strftime("%d-%b-%Y")
