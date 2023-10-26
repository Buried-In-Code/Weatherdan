__all__ = ["router"]

import logging
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum

from fastapi import APIRouter, Body, Cookie, Query
from fastapi.exceptions import HTTPException
from pony.orm import db_session

from weatherdan.constants import constants
from weatherdan.database.tables import RainfallReading
from weatherdan.ecowitt.category import Category
from weatherdan.models import Reading, WeekReading
from weatherdan.responses import ErrorResponse
from weatherdan.utils import get_week_ends

router = APIRouter(
    prefix="/rainfall",
    tags=["Rainfall"],
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
LOGGER = logging.getLogger(__name__)


class Timeframe(Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"


def get_daily_readings(year: int | None = None, month: int | None = None) -> list[Reading]:
    with db_session:
        entries = sorted([x.to_model() for x in RainfallReading.select()])
        if year:
            entries = [x for x in entries if x.datestamp.year == year]
        if month:
            entries = [x for x in entries if x.datestamp.month == month]
        return entries


def get_weekly_readings(
    year: int | None = None,
    month: int | None = None,
) -> list[WeekReading]:
    with db_session:
        weekly = {}
        for entry in sorted(RainfallReading.select(), key=lambda x: x.datestamp):
            key = get_week_ends(value=entry.datestamp)
            if key not in weekly:
                weekly[key] = WeekReading(
                    start_datestamp=key[0],
                    end_datestamp=key[1],
                    value=Decimal(0),
                )
            weekly[key].value += entry.value
        entries = sorted(weekly.values())
        if year:
            entries = [x for x in entries if year in (x.start_datestamp.year, x.end_datestamp.year)]
        if month:
            entries = [
                x for x in entries if month in (x.start_datestamp.month, x.end_datestamp.month)
            ]
        return entries


def get_monthly_readings(year: int | None = None) -> list[Reading]:
    with db_session:
        monthly = {}
        for entry in sorted(RainfallReading.select(), key=lambda x: x.datestamp):
            key = entry.datestamp.replace(day=1)
            if key not in monthly:
                monthly[key] = Reading(datestamp=key, value=Decimal(0))
            monthly[key].value += entry.value
        entries = sorted(monthly.values())
        if year:
            entries = [x for x in entries if x.datestamp.year == year]
        return entries


def get_yearly_readings() -> list[Reading]:
    with db_session:
        yearly = {}
        for entry in sorted(RainfallReading.select(), key=lambda x: x.datestamp):
            key = entry.datestamp.replace(day=1, month=1)
            if key not in yearly:
                yearly[key] = Reading(datestamp=key, value=Decimal(0))
            yearly[key].value += entry.value
        return sorted(yearly.values())


@router.get(path="")
def list_readings(
    *,
    timeframe: Timeframe = Timeframe.DAILY,
    year: int | None = None,
    month: int | None = None,
    all_results: bool = Query(alias="allResults", default=False),
    count: int = Cookie(alias="weatherdan_count", default=28),
) -> list[Reading | WeekReading]:
    if all_results:
        count = 100
    if timeframe == Timeframe.DAILY:
        return get_daily_readings(year=year, month=month)[-count:]
    if timeframe == Timeframe.WEEKLY:
        return get_weekly_readings(year=year, month=month)[-count:]
    if timeframe == Timeframe.MONTHLY:
        return get_monthly_readings(year=year)[-count:]
    return get_yearly_readings()[-count:]


@router.post(path="", status_code=201)
def add_reading(*, input: Reading) -> Reading:  # noqa: A002
    with db_session:
        if reading := RainfallReading.get(datestamp=input.datestamp):
            reading.value = input.value
        else:
            reading = RainfallReading(datestamp=input.datestamp, value=input.value)
        return reading.to_model()


@router.delete(path="", status_code=204)
def remove_reading(*, datestamp: date = Body(embed=True)) -> None:
    with db_session:
        reading = RainfallReading.get(datestamp=datestamp)
        if not reading:
            raise HTTPException(status_code=404, detail="Reading doesn't exist")
        reading.delete()


@router.put(path="", status_code=204)
def refresh_readings(*, force: bool = False) -> None:
    temp_time = datetime.now() - timedelta(hours=3)  # noqa: DTZ005
    if not force and constants.settings.last_updated.rainfall >= temp_time:
        raise HTTPException(status_code=208, detail="No update needed")
    with db_session:
        device = constants.ecowitt.list_devices()[0]
        # region History readings
        history_readings = constants.ecowitt.get_history_readings(
            device=device.mac,
            category=Category.RAINFALL,
            start_date=constants.settings.last_updated.rainfall,
        )
        for timestamp, value in history_readings.items():
            if reading := RainfallReading.get(datestamp=timestamp.date()):
                reading.value = value
            else:
                reading = RainfallReading(datestamp=timestamp.date(), value=value)
        # endregion
        # region Live reading
        live_reading = constants.ecowitt.get_live_reading(
            device=device.mac,
            category=Category.RAINFALL,
        )
        if live_reading:
            if reading := RainfallReading.get(datestamp=live_reading.time.date()):
                reading.value = live_reading.value
            else:
                reading = RainfallReading(
                    datestamp=live_reading.time.date(),
                    value=live_reading.value,
                )
        # endregion
    constants.settings.last_updated.rainfall = datetime.now()  # noqa: DTZ005
    constants.settings.save()
