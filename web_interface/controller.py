__all__ = [
    "device_list",
    "list_available_years",
    "list_available_months",
    "generate_yearly_stats",
    "generate_monthly_stats",
    "generate_weekly_stats",
    "generate_daily_stats",
]

import logging
from datetime import date, timedelta
from decimal import Decimal

from natsort import humansorted as sorted
from natsort import ns

from common.console import date_to_str
from common.statistics import date_list, device_list
from common.storage import from_file
from web_interface.schemas import Device, Stat

LOGGER = logging.getLogger(__name__)


def list_available_years() -> list[int]:
    return sorted({x.year for x in date_list()}, alg=ns.NA | ns.G)


def list_available_months(year: int) -> list[int]:
    return sorted({x.month for x in date_list() if x.year == year}, alg=ns.NA | ns.G)


def generate_yearly_stats(device: str, maximum: int = 1000) -> Device:
    yearly = {}
    for entry in sorted(
        {x for x in from_file() if x.device == device},
        key=lambda x: x.timestamp,
        reverse=True,
        alg=ns.NA | ns.G,
    ):
        key = entry.timestamp.replace(day=1, month=1)
        if key not in yearly:
            yearly[key] = Decimal(0.0)
        yearly[key] += entry.value
    return Device(
        name=device,
        stats=list(
            reversed(
                [Stat(timestamp=key.strftime("%Y"), value=value) for key, value in yearly.items()][
                    :maximum
                ]
            )
        ),
    )


def generate_monthly_stats(year: int, device: str, maximum: int = 1000) -> Device:
    monthly = {}
    for entry in sorted(
        {x for x in from_file() if x.device == device},
        key=lambda x: x.timestamp,
        reverse=True,
        alg=ns.NA | ns.G,
    ):
        key = entry.timestamp.replace(day=1)
        if key not in monthly:
            monthly[key] = Decimal(0.0)
        monthly[key] += entry.value
    if year:
        monthly = {k: v for k, v in monthly.items() if k.year == year}
    return Device(
        name=device,
        stats=list(
            reversed(
                [
                    Stat(timestamp=key.strftime("%b/%Y"), value=value)
                    for key, value in monthly.items()
                ][:maximum]
            )
        ),
    )


def generate_weekly_stats(year: int, month: int, device: str, maximum: int = 1000) -> Device:
    def get_week_ends(datestamp: date) -> tuple[date, date]:
        start = datestamp - timedelta(days=datestamp.isoweekday() - 1)
        end = start + timedelta(days=6)
        return start, end

    weekly = {}
    for entry in sorted(
        {x for x in from_file() if x.device == device},
        key=lambda x: x.timestamp,
        reverse=True,
        alg=ns.NA | ns.G,
    ):
        key = get_week_ends(datestamp=entry.timestamp)
        if key not in weekly:
            weekly[key] = Decimal(0.0)
        weekly[key] += entry.value
    if year and month:
        weekly = {
            k: v
            for k, v in weekly.items()
            if (k[0].year == year and k[0].month == month)
            or (k[1].year == year and k[1].month == month)
        }
    elif year:
        weekly = {k: v for k, v in weekly.items() if k[0].year == year or k[1].year == year}
    elif month:
        weekly = {k: v for k, v in weekly.items() if k[0].month == month or k[1].month == month}
    return Device(
        name=device,
        stats=list(
            reversed(
                [
                    Stat(timestamp=f"{key[0].strftime('%d')}-{date_to_str(key[1])}", value=value)
                    for key, value in weekly.items()
                ][:maximum]
            )
        ),
    )


def generate_daily_stats(year: int, month: int, device: str, maximum: int = 1000) -> Device:
    daily = {}
    for entry in sorted(
        {x for x in from_file() if x.device == device},
        key=lambda x: x.timestamp,
        reverse=True,
        alg=ns.NA | ns.G,
    ):
        key = entry.timestamp
        if key not in daily:
            daily[key] = Decimal(0.0)
        daily[key] += entry.value
    if year and month:
        daily = {k: v for k, v in daily.items() if k.year == year and k.month == month}
    elif year:
        daily = {k: v for k, v in daily.items() if k.year == year}
    elif month:
        daily = {k: v for k, v in daily.items() if k.month == month}
    return Device(
        name=device,
        stats=list(
            reversed(
                [Stat(timestamp=date_to_str(key), value=value) for key, value in daily.items()][
                    :maximum
                ]
            )
        ),
    )
