__all__ = ["router"]

import logging
from datetime import date, datetime, timedelta
from enum import Enum

from fastapi import APIRouter, Body, Cookie
from fastapi.exceptions import HTTPException
from pony.orm import db_session

from weatherdan.constants import constants
from weatherdan.database.tables import UVIndexReading
from weatherdan.ecowitt.category import Category
from weatherdan.models import HighReading, WeekHighReading
from weatherdan.responses import ErrorResponse

router = APIRouter(
    prefix="/uv-index",
    tags=["UV Index"],
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
LOGGER = logging.getLogger(__name__)


class Timeframe(Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"


def get_daily_readings(year: int | None = None, month: int | None = None) -> list[HighReading]:
    with db_session:
        entries = sorted([x.to_model() for x in UVIndexReading.select()])
        if year:
            entries = [x for x in entries if x.datestamp.year == year]
        if month:
            entries = [x for x in entries if x.datestamp.month == month]
        return entries


def get_weekly_readings(
    year: int | None = None,
    month: int | None = None,
) -> list[HighReading]:
    def get_week_ends(datestamp: date) -> tuple[date, date]:
        start = datestamp - timedelta(days=datestamp.isoweekday() - 1)
        end = start + timedelta(days=6)
        return start, end

    with db_session:
        weekly = {}
        for entry in sorted(UVIndexReading.select(), key=lambda x: x.datestamp):
            key = get_week_ends(datestamp=entry.datestamp)
            if key not in weekly:
                weekly[key] = WeekHighReading(
                    start_datestamp=key[0],
                    end_datestamp=key[1],
                    high=entry.high,
                )
            if entry.high > weekly[key].high:
                weekly[key].high = entry.high
        entries = sorted(weekly.values())
        if year:
            entries = [
                x
                for x in entries
                if x.start_datestamp.year == year or x.end_datestamp.year == year  # noqa: PLR1714
            ]
        if month:
            entries = [
                x
                for x in entries
                if x.start_datestamp.month == month  # noqa: PLR1714
                or x.end_datestamp.month == month
            ]
        return entries


def get_monthly_readings(year: int | None = None) -> list[HighReading]:
    with db_session:
        monthly = {}
        for entry in sorted(UVIndexReading.select(), key=lambda x: x.datestamp):
            key = entry.datestamp.replace(day=1)
            if key not in monthly:
                monthly[key] = HighReading(datestamp=key, high=entry.high)
            if entry.high > monthly[key].high:
                monthly[key].high = entry.high
        entries = sorted(monthly.values())
        if year:
            entries = [x for x in entries if x.datestamp.year == year]
        return entries


def get_yearly_readings() -> list[HighReading]:
    with db_session:
        yearly = {}
        for entry in sorted(UVIndexReading.select(), key=lambda x: x.datestamp):
            key = entry.datestamp.replace(day=1, month=1)
            if key not in yearly:
                yearly[key] = HighReading(datestamp=key, high=entry.high)
            if entry.high > yearly[key].high:
                yearly[key].high = entry.high
        return sorted(yearly.values())


@router.get(path="")
def list_readings(
    *,
    timeframe: Timeframe = Timeframe.DAILY,
    year: int | None = None,
    month: int | None = None,
    count: int = Cookie(alias="weatherdan_count", default=28),
) -> list[HighReading | WeekHighReading]:
    if timeframe == Timeframe.DAILY:
        return get_daily_readings(year=year, month=month)[-count:]
    if timeframe == Timeframe.WEEKLY:
        return get_weekly_readings(year=year, month=month)[-count:]
    if timeframe == Timeframe.MONTHLY:
        return get_monthly_readings(year=year)[-count:]
    return get_yearly_readings()[-count:]


@router.post(path="", status_code=201)
def add_reading(*, input: HighReading) -> HighReading:  # noqa: A002
    with db_session:
        if reading := UVIndexReading.get(datestamp=input.datestamp):
            reading.high = input.high
        else:
            reading = UVIndexReading(datestamp=input.datestamp, high=input.high)
        return reading.to_model()


@router.delete(path="", status_code=204)
def remove_reading(*, datestamp: date = Body(embed=True)) -> None:
    with db_session:
        reading = UVIndexReading.get(datestamp=datestamp)
        if not reading:
            raise HTTPException(status_code=404, detail="Reading doesn't exist")
        reading.delete()


@router.put(path="", status_code=204)
def refresh_readings(*, force: bool = False) -> None:
    temp_time = datetime.now() - timedelta(hours=3)  # noqa: DTZ005
    if not force and constants.settings.last_updated.uv_index >= temp_time:
        raise HTTPException(status_code=208, detail="No update needed")
    with db_session:
        device = constants.ecowitt.list_devices()[0]
        # region History readings
        history_readings = constants.ecowitt.get_history_readings(
            device=device.mac,
            category=Category.UV_INDEX,
            start_date=constants.settings.last_updated.uv_index,
        )
        for timestamp, value in history_readings.items():
            if reading := UVIndexReading.get(datestamp=timestamp.date()):
                if value > reading.high:
                    reading.high = value
            else:
                reading = UVIndexReading(datestamp=timestamp.date(), high=value)
        # endregion
        # region Live reading
        live_reading = constants.ecowitt.get_live_reading(
            device=device.mac,
            category=Category.UV_INDEX,
        )
        if live_reading:
            if reading := UVIndexReading.get(datestamp=live_reading.time.date()):
                if live_reading.value > reading.high:
                    reading.high = live_reading.value
            else:
                reading = UVIndexReading(
                    datestamp=live_reading.time.date(),
                    high=live_reading.value,
                )
        # endregion
    constants.settings.last_updated.uv_index = datetime.now()  # noqa: DTZ005
    constants.settings.save()
