from datetime import datetime, timedelta
from time import sleep

from rich.console import Group
from rich.live import Live
from rich.prompt import Prompt

from common.console import CONSOLE
from common.settings import Settings
from common.statistics import (
    generate_daily_table,
    generate_monthly_table,
    generate_weekly_table,
    generate_yearly_table,
)
from common.storage import Reading, to_file
from ecowitt.service import Category, Ecowitt

SETTINGS = Settings.load()
ECOWITT = Ecowitt(
    application_key=SETTINGS.ecowitt.application_key, api_key=SETTINGS.ecowitt.api_key
)


def generate_table() -> Group:
    pull_ecowitt_history()
    pull_ecowitt_data()
    return Group(
        generate_daily_table(),
        generate_weekly_table(),
        generate_monthly_table(),
        generate_yearly_table(),
    )


def pull_ecowitt_data():
    devices = ECOWITT.list_devices()
    for device in devices:
        timestamp, rainfall = ECOWITT.get_device_reading(device, Category.RAINFALL)
        to_file(Reading(timestamp=timestamp.date(), value=float(rainfall)))

    SETTINGS.ecowitt.last_updated = datetime.now() - timedelta(days=3)
    SETTINGS.save()


def pull_ecowitt_history():
    for device in ECOWITT.list_devices():
        history = ECOWITT.list_device_history(
            device, SETTINGS.ecowitt.last_updated, Category.RAINFALL
        )
        if history:
            for timestamp, rainfall in history.items():
                to_file(Reading(timestamp=timestamp.date(), value=float(rainfall)))


def setup_ecowitt():
    ECOWITT.application_key = Prompt.ask(
        "Ecowitt Application Key", default=ECOWITT.application_key, console=CONSOLE
    )
    ECOWITT.api_key = Prompt.ask(
        "Ecowitt API Key", default=ECOWITT.api_key, console=CONSOLE
    )
    SETTINGS.ecowitt.application_key = ECOWITT.application_key
    SETTINGS.ecowitt.api_key = ECOWITT.api_key
    SETTINGS.save()


def main():
    try:
        while not ECOWITT.test_credentials():
            setup_ecowitt()
        CONSOLE.print("Ecowitt account setup", style="logging.level.debug")
        with Live(
            generate_table(), console=CONSOLE, screen=False, refresh_per_second=20
        ) as live:
            while True:
                sleep(1 * 60 * 60)
                live.update(generate_table())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
