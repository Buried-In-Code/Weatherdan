__all__ = [
    "print_stats",
    "load_daily_stats",
    "generate_daily_table",
    "load_weekly_stats",
    "generate_weekly_table",
    "load_monthly_stats",
    "generate_monthly_table",
    "load_yearly_stats",
    "generate_yearly_table",
]

from datetime import date, timedelta

from rich.table import Column, Table

from common.console import CONSOLE, date_to_str, generate_table
from common.storage import from_file


def get_table_headers():
    return ["Date", Column("Rain (mm)", justify="right")]


def print_stats():
    CONSOLE.print(generate_daily_table())
    CONSOLE.print(generate_weekly_table())
    CONSOLE.print(generate_monthly_table())
    CONSOLE.print(generate_yearly_table())


def load_daily_stats() -> dict[date, float]:
    daily = sorted(from_file(), key=lambda x: x.timestamp, reverse=True)
    return {x.timestamp: x.value for x in daily}


def generate_daily_table(max_rows: int = 13) -> Table | None:
    return generate_table(
        title="Daily Stats",
        columns=get_table_headers(),
        rows=[[date_to_str(k), f"{v:,.2f}"] for k, v in load_daily_stats().items()][:max_rows],
    )


def load_weekly_stats() -> dict[tuple[date, date], float]:
    def get_week_ends(datestamp: date) -> tuple[date, date]:
        start = datestamp - timedelta(days=datestamp.isoweekday() - 1)
        end = start + timedelta(days=6)
        return start, end

    weekly = {}
    for entry in sorted(from_file(), key=lambda x: x.timestamp, reverse=True):
        key = get_week_ends(entry.timestamp)
        if key not in weekly:
            weekly[key] = 0.0
        weekly[key] += entry.value
    return weekly


def generate_weekly_table(max_rows: int = 13) -> Table | None:
    return generate_table(
        title="Weekly Stats",
        columns=get_table_headers(),
        rows=[
            [f"{k[0].strftime('%d')} - {date_to_str(k[1])}", f"{v:,.2f}"]
            for k, v in load_weekly_stats().items()
        ][:max_rows],
    )


def load_monthly_stats() -> dict[date, float]:
    monthly = {}
    for entry in sorted(from_file(), key=lambda x: x.timestamp, reverse=True):
        key = entry.timestamp.replace(day=1)
        if key not in monthly:
            monthly[key] = 0.0
        monthly[key] += entry.value
    return monthly


def generate_monthly_table(max_rows: int = 13) -> Table | None:
    return generate_table(
        title="Monthly Stats",
        columns=get_table_headers(),
        rows=[[k.strftime("%b-%Y"), f"{v:,.2f}"] for k, v in load_monthly_stats().items()][
            :max_rows
        ],
    )


def load_yearly_stats() -> dict[date, float]:
    yearly = {}
    for entry in sorted(from_file(), key=lambda x: x.timestamp, reverse=True):
        key = entry.timestamp.replace(day=1, month=1)
        if key not in yearly:
            yearly[key] = 0.0
        yearly[key] += entry.value
    return yearly


def generate_yearly_table(max_rows: int = 13) -> Table | None:
    return generate_table(
        title="Yearly Stats",
        columns=get_table_headers(),
        rows=[[k.strftime("%Y"), f"{v:,.2f}"] for k, v in load_yearly_stats().items()][:max_rows],
    )


if __name__ == "__main__":
    print_stats()
