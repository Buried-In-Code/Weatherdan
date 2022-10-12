from datetime import date

from rich.prompt import Confirm, FloatPrompt

from common.console import CONSOLE, DatePrompt
from common.statistics import print_stats
from common.storage import Reading, to_file


def main():
    entries = set()
    while Confirm.ask("Add rainfall entry", console=CONSOLE):
        timestamp = DatePrompt.ask("Enter date", default=date.today(), console=CONSOLE)
        value = FloatPrompt.ask("Enter rainfall (mm)", default=0.0, console=CONSOLE)
        entry = Reading(timestamp=timestamp, value=value)
        entries.add(entry)
    to_file(*entries)
    print_stats()


if __name__ == "__main__":
    main()
