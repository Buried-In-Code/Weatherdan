__all__ = [
    "list_available_years",
    "list_available_months",
    "generate_yearly_stats",
    "generate_monthly_stats",
    "generate_weekly_stats",
    "generate_daily_stats",
]

import logging
from datetime import date, timedelta, datetime
from decimal import Decimal

from natsort import humansorted as sorted
from natsort import ns

from common.console import date_to_str
from common.storage import from_file
from common.settings import Settings
from common.services import update_data
from common.services.ecowitt import Ecowitt
from website.schemas import Stat

LOGGER = logging.getLogger(__name__)


def date_list() -> list[date]:
    return sorted({x.timestamp for x in from_file()}, alg=ns.NA | ns.G)


def refresh_data():
    settings = Settings.load().save()
    if settings.ecowitt.last_updated >= datetime.now() - timedelta(hours=3):
        return

    LOGGER.info("Refreshing data")
    ecowitt = Ecowitt(settings.ecowitt)
    if not ecowitt.test_credentials():
        LOGGER.critical("Invalid Ecowitt credentials")
        return
    update_data(ecowitt=ecowitt, settings=settings)


def list_available_years() -> list[int]:
    return sorted({x.year for x in date_list()}, alg=ns.NA | ns.G)


def list_available_months(year: int) -> list[int]:
    return sorted({x.month for x in date_list() if x.year == year}, alg=ns.NA | ns.G)


def generate_yearly_stats(maximum: int = 1000) -> list[Stat]:
    yearly = {}
    for entry in sorted(from_file(), key=lambda x: x.timestamp, reverse=True, alg=ns.NA | ns.G):
        key = entry.timestamp.replace(day=1, month=1)
        if key not in yearly:
            yearly[key] = Decimal(0.0)
        yearly[key] += entry.value
    return list(
        reversed(
            [Stat(timestamp=k.strftime("%Y"), value=v) for k, v in yearly.items()][:maximum]
        )
    )


def generate_monthly_stats(year: int, maximum: int = 1000) -> list[Stat]:
    monthly = {}
    for entry in sorted(from_file(), key=lambda x: x.timestamp, reverse=True, alg=ns.NA | ns.G):
        key = entry.timestamp.replace(day=1)
        if key not in monthly:
            monthly[key] = Decimal(0.0)
        monthly[key] += entry.value
    if year:
        monthly = {k: v for k, v in monthly.items() if k.year == year}
    return list(
        reversed(
            [Stat(timestamp=k.strftime("%b-%Y"), value=v) for k, v in monthly.items()][:maximum]
        )
    )


def generate_weekly_stats(year: int, month: int, maximum: int = 1000) -> list[Stat]:
    def get_week_ends(datestamp: date) -> tuple[date, date]:
        start = datestamp - timedelta(days=datestamp.isoweekday() - 1)
        end = start + timedelta(days=6)
        return start, end

    weekly = {}
    for entry in sorted(from_file(), key=lambda x: x.timestamp, reverse=True, alg=ns.NA | ns.G):
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
    return list(
        reversed(
            [Stat(timestamp=f"{k[0].strftime('%d')} - {date_to_str(k[1])}", value=v) for k, v in weekly.items()][:maximum]
        )
    )


def generate_daily_stats(year: int, month: int, maximum: int = 1000) -> list[Stat]:
    daily = {}
    for entry in sorted(from_file(), key=lambda x: x.timestamp, reverse=True, alg=ns.NA | ns.G):
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
    return list(
        reversed(
            [Stat(timestamp=date_to_str(k), value=v) for k, v in daily.items()][:maximum]
        )
    )
