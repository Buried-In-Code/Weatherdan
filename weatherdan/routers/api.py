__all__ = ["router"]

import logging
from datetime import date, datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter, Body

from weatherdan.models import MonthReading, Reading, WeekReading, YearReading
from weatherdan.responses import ErrorResponse
from weatherdan.services import update_data
from weatherdan.services.ecowitt import Ecowitt
from weatherdan.settings import Settings
from weatherdan.storage import add_entry, read_from_file, remove_entry

router = APIRouter(
    prefix="/api",
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
stat_router = APIRouter(prefix="/stats", tags=["Stats"])
LOGGER = logging.getLogger(__name__)


@stat_router.post(path="", status_code=204)
def add_reading(reading: Reading) -> None:
    add_entry(entry=reading)


@stat_router.delete(path="", status_code=204)
def remove_reading(timestamp: date = Body(embed=True)) -> None:
    remove_entry(timestamp=timestamp)


@stat_router.put(path="", status_code=204)
def refresh_readings() -> None:
    settings = Settings()
    if settings.ecowitt.last_updated >= datetime.now() - timedelta(hours=3):
        return

    LOGGER.info("Refreshing data")
    ecowitt = Ecowitt()
    if not ecowitt.test_credentials():
        LOGGER.critical("Invalid Ecowitt credentials")
        return
    update_data(ecowitt=ecowitt)


@stat_router.get(path="/daily")
def get_daily_readings(
    year: int | None = None,
    month: int | None = None,
    count: int = 1000,
) -> list[Reading]:
    entries = read_from_file()
    if year:
        entries = [x for x in entries if x.timestamp.year == year]
    if month:
        entries = [x for x in entries if x.timestamp.month == month]
    return reversed(entries[:count])


def to_week_readings(entries: set[Reading]) -> list[WeekReading]:
    def get_week_ends(datestamp: date) -> tuple[date, date]:
        start = datestamp - timedelta(days=datestamp.isoweekday() - 1)
        end = start + timedelta(days=6)
        return start, end

    weekly = {}
    for entry in sorted(entries, key=lambda x: x.timestamp, reverse=True):
        key = get_week_ends(datestamp=entry.timestamp)
        if key not in weekly:
            weekly[key] = WeekReading(
                start_timestamp=key[0],
                end_timestamp=key[1],
                value=Decimal(0),
            )
        weekly[key].value += entry.value
    return list(weekly.values())


@stat_router.get(path="/weekly")
def get_weekly_readings(
    year: int | None = None,
    month: int | None = None,
    count: int = 1000,
) -> list[WeekReading]:
    entries = to_week_readings(entries=read_from_file())
    if year:
        entries = [
            x for x in entries if x.start_timestamp.year == year or x.end_timestamp.year == year
        ]
    if month:
        entries = [
            x for x in entries if x.start_timestamp.month == month or x.end_timestamp.month == month
        ]
    return reversed(entries[:count])


def to_month_readings(entries: set[Reading]) -> list[MonthReading]:
    monthly = {}
    for entry in sorted(entries, key=lambda x: x.timestamp, reverse=True):
        key = entry.timestamp.replace(day=1)
        if key not in monthly:
            monthly[key] = MonthReading(timestamp=key, value=Decimal(0))
        monthly[key].value += entry.value
    return list(monthly.values())


@stat_router.get(path="/monthly")
def get_monthly_readings(year: int | None = None, count: int = 1000) -> list[MonthReading]:
    entries = to_month_readings(entries=read_from_file())
    if year:
        entries = [x for x in entries if x.timestamp.year == year]
    return reversed(entries[:count])


def to_year_readings(entries: set[Reading]) -> list[YearReading]:
    yearly = {}
    for entry in sorted(entries, key=lambda x: x.timestamp, reverse=True):
        key = entry.timestamp.replace(day=1, month=1)
        if key not in yearly:
            yearly[key] = YearReading(timestamp=key, value=Decimal(0))
        yearly[key].value += entry.value
    return list(yearly.values())


@stat_router.get(path="/yearly")
def get_yearly_readings(count: int = 1000) -> list[YearReading]:
    entries = to_year_readings(entries=read_from_file())
    return reversed(entries[:count])


router.include_router(stat_router)
