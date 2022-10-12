__all__ = [
    "CONSOLE",
    "DatePrompt",
    "DatetimePrompt",
    "create_menu",
    "generate_table",
    "date_to_str",
    "datetime_to_str",
]

from datetime import date, datetime

from rich import box
from rich.console import Console
from rich.prompt import DefaultType, IntPrompt, InvalidResponse, PromptBase, Text
from rich.table import Table
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
        }
    )
)


def date_to_str(value: date) -> str:
    return value.strftime("%d-%b-%Y")


def datetime_to_str(value: datetime) -> str:
    return value.strftime("%d-%b-%Y %H:%M")


def str_to_date(value: str) -> date:
    return datetime.strptime(value, "%d-%b-%Y").date()


def str_to_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%d-%b-%Y %H:%M")


class DatetimePrompt(PromptBase[datetime]):
    response_type = datetime
    validate_error_message = "[prompt.invalid]Please enter a valid ISO-8601 datetime"

    def render_default(self, default: DefaultType) -> Text:
        return Text(datetime_to_str(default) if default else "", style="prompt.default")

    def check_choice(self, value: str) -> bool:
        assert self.choices is not None
        try:
            return str_to_datetime(value.strip()) in self.choices
        except ValueError:
            return False

    def process_response(self, value: str) -> datetime:
        try:
            mapped_value = str_to_datetime(value.strip())
        except ValueError:
            try:
                mapped_value = str_to_datetime(value.strip() + ":00")
            except ValueError:
                try:
                    mapped_value = str_to_datetime(value.strip() + " 00:00")
                except ValueError:
                    raise InvalidResponse(self.validate_error_message)

        if self.choices is not None and not self.check_choice(value):
            raise InvalidResponse(self.illegal_choice_message)

        return mapped_value


class DatePrompt(PromptBase[date]):
    response_type = date
    validate_error_message = "[prompt.invalid]Please enter a valid ISO-8601 date"

    def render_default(self, default: DefaultType) -> Text:
        return Text(date_to_str(default) if default else "", style="prompt.default")

    def check_choice(self, value: str) -> bool:
        assert self.choices is not None
        try:
            return str_to_date(value.strip()) in self.choices
        except ValueError:
            return False

    def process_response(self, value: str) -> date:
        try:
            mapped_value = str_to_date(value.strip())
        except ValueError:
            raise InvalidResponse(self.validate_error_message)

        if self.choices is not None and not self.check_choice(value):
            raise InvalidResponse(self.illegal_choice_message)

        return mapped_value


def create_menu(
    options: list[str], prompt: str | None = None, default: str | None = None
) -> int | None:
    if not options:
        return 0
    for index, item in enumerate(options):
        CONSOLE.print(f"[prompt]{index + 1}:[/] [prompt.choices]{item}[/]")
    if default:
        CONSOLE.print(f"[prompt]0:[/] [prompt.default]{default}[/]")
    selected = IntPrompt.ask(
        prompt=prompt, default=0 if default else None, console=CONSOLE
    )
    if selected < 0 or selected > len(options) or (selected == 0 and not default):
        CONSOLE.print(f"Invalid Option: `{selected}`", style="prompt.invalid")
        return create_menu(options=options, prompt=prompt, default=default)
    return selected


def generate_table(title: str, columns: list[str], rows: list[list[str]]) -> Table:
    table = Table(
        *columns,
        title=title,
        box=box.SIMPLE,
        title_style="magenta",
        header_style="bold blue",
        border_style="blue",
        row_styles=["white", "dim white"],
        footer_style="dim blue",
    )
    for row in rows:
        table.add_row(*row)
    return table
