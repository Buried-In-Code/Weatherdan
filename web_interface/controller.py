__all__ = [
    "list_available_years",
    "list_available_months",
    "generate_yearly_stats",
    "generate_monthly_stats",
    "generate_weekly_stats",
    "generate_daily_stats",
]

import logging

from common.console import date_to_str
from common.statistics import (
    load_daily_stats,
    load_monthly_stats,
    load_weekly_stats,
    load_yearly_stats,
)
from common.storage import from_file

LOGGER = logging.getLogger(__name__)


def list_available_years() -> list[int]:
    LOGGER.info("Loading available years")
    output = set()
    for entry in from_file():
        output.add(entry.timestamp.year)
    return sorted(output)


def list_available_months(year: int) -> list[int]:
    LOGGER.info(f"Loading available months in {year}")
    output = set()
    for entry in from_file():
        if entry.timestamp.year == year:
            output.add(entry.timestamp.month)
    return sorted(output)


def generate_yearly_stats() -> dict[str, float]:
    LOGGER.info("Generating yearly stats")
    return {k.strftime("%Y"): v for k, v in load_yearly_stats().items()}


def generate_monthly_stats(year: int) -> dict[str, float]:
    LOGGER.info(f"Generating monthly stats for {year}")
    if not year:
        output = load_monthly_stats()
    else:
        output = {k: v for k, v in load_monthly_stats().items() if k.year == year}
    return {k.strftime("%b-%Y"): v for k, v in output.items()}


def generate_weekly_stats(year: int, month: int) -> dict[str, float]:
    LOGGER.info(f"Generating weekly stats for {year}-{month}")
    if not year and not month:
        output = load_weekly_stats()
    elif year and not month:
        output = {
            k: v for k, v in load_weekly_stats().items() if k[0].year == year or k[1].year == year
        }
    elif not year and month:
        output = {
            k: v
            for k, v in load_weekly_stats().items()
            if k[0].month == month or k[1].month == month
        }
    else:
        output = {
            k: v
            for k, v in load_weekly_stats().items()
            if (k[0].year == year and k[0].month == month)
            or (k[1].year == year and k[1].month == month)
        }
    return {f"{k[0].strftime('%d')} - {date_to_str(k[1])}": v for k, v in output.items()}


def generate_daily_stats(year: int, month: int) -> dict[str, float]:
    LOGGER.info(f"Generating weekly stats for {year}-{month}")
    if not year and not month:
        output = load_daily_stats()
    elif year and not month:
        output = {k: v for k, v in load_daily_stats().items() if k.year == year}
    elif not year and month:
        output = {k: v for k, v in load_daily_stats().items() if k.month == month}
    else:
        output = {
            k: v for k, v in load_daily_stats().items() if k.year == year and k.month == month
        }
    return {date_to_str(k): v for k, v in output.items()}
