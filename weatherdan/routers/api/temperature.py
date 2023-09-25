__all__ = ["router"]

import logging
from datetime import date, datetime, timedelta
from enum import Enum

from fastapi import APIRouter, Body, Cookie
from fastapi.exceptions import HTTPException
from pony.orm import db_session

from weatherdan.database.tables import TemperatureReading
from weatherdan.ecowitt.category import Category
from weatherdan.ecowitt.service import Ecowitt
from weatherdan.models import RangeReading, WeekRangeReading
from weatherdan.responses import ErrorResponse
from weatherdan.settings import Settings

router = APIRouter(
    prefix="/temperature",
    tags=["Temperature"],
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
LOGGER = logging.getLogger(__name__)


class Timeframe(Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"


def get_daily_readings(year: int | None = None, month: int | None = None) -> list[RangeReading]:
    with db_session:
        entries = sorted([x.to_model() for x in TemperatureReading.select()])
        if year:
            entries = [x for x in entries if x.datestamp.year == year]
        if month:
            entries = [x for x in entries if x.datestamp.month == month]
        return entries


def get_weekly_readings(
    year: int | None = None,
    month: int | None = None,
) -> list[WeekRangeReading]:
    def get_week_ends(datestamp: date) -> tuple[date, date]:
        start = datestamp - timedelta(days=datestamp.isoweekday() - 1)
        end = start + timedelta(days=6)
        return start, end

    with db_session:
        weekly = {}
        for entry in sorted(TemperatureReading.select(), key=lambda x: x.datestamp):
            key = get_week_ends(datestamp=entry.datestamp)
            if key not in weekly:
                weekly[key] = WeekRangeReading(
                    start_datestamp=key[0],
                    end_datestamp=key[1],
                    high=entry.high,
                    low=entry.low,
                )
            if entry.high > weekly[key].high:
                weekly[key].high = entry.high
            if entry.low < weekly[key].low:
                weekly[key].low = entry.low
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


def get_monthly_readings(year: int | None = None) -> list[RangeReading]:
    with db_session:
        monthly = {}
        for entry in sorted(TemperatureReading.select(), key=lambda x: x.datestamp):
            key = entry.datestamp.replace(day=1)
            if key not in monthly:
                monthly[key] = RangeReading(datestamp=key, high=entry.high, low=entry.low)
            if entry.high > monthly[key].high:
                monthly[key].high = entry.high
            if entry.low < monthly[key].low:
                monthly[key].low = entry.low
        entries = sorted(monthly.values())
        if year:
            entries = [x for x in entries if x.datestamp.year == year]
        return entries


def get_yearly_readings() -> list[RangeReading]:
    with db_session:
        yearly = {}
        for entry in sorted(TemperatureReading.select(), key=lambda x: x.datestamp):
            key = entry.datestamp.replace(day=1, month=1)
            if key not in yearly:
                yearly[key] = RangeReading(datestamp=key, high=entry.high, low=entry.low)
            if entry.high > yearly[key].high:
                yearly[key].high = entry.high
            if entry.low < yearly[key].low:
                yearly[key].low = entry.low
        return sorted(yearly.values())


@router.get(path="")
def list_readings(
    *,
    timeframe: Timeframe = Timeframe.DAILY,
    year: int | None = None,
    month: int | None = None,
    count: int = Cookie(alias="weatherdan_count", default=28),
) -> list[RangeReading | WeekRangeReading]:
    if timeframe == Timeframe.DAILY:
        return get_daily_readings(year=year, month=month)[-count:]
    if timeframe == Timeframe.WEEKLY:
        return get_weekly_readings(year=year, month=month)[-count:]
    if timeframe == Timeframe.MONTHLY:
        return get_monthly_readings(year=year)[-count:]
    return get_yearly_readings()[-count:]


@router.post(path="", status_code=201)
def add_reading(*, input: RangeReading) -> RangeReading:  # noqa: A002
    with db_session:
        if reading := TemperatureReading.get(datestamp=input.datestamp):
            reading.high = input.high
            reading.low = input.low
        else:
            reading = TemperatureReading(datestamp=input.datestamp, high=input.high, low=input.low)
        return reading.to_model()


@router.delete(path="", status_code=204)
def remove_reading(*, datestamp: date = Body(embed=True)) -> None:
    with db_session:
        reading = TemperatureReading.get(datestamp=datestamp)
        if not reading:
            raise HTTPException(status_code=404, detail="Reading doesn't exist")
        reading.delete()


@router.put(path="", status_code=204)
def refresh_readings(*, force: bool = False) -> None:
    settings = Settings.load()
    temp_time = datetime.now() - timedelta(hours=3)  # noqa: DTZ005
    if not force and settings.last_updated.temperature >= temp_time:
        raise HTTPException(status_code=508, detail="No update needed")
    ecowitt = Ecowitt(
        application_key=settings.ecowitt.application_key,
        api_key=settings.ecowitt.api_key,
    )
    if not ecowitt.test_credentials():
        raise HTTPException(status_code=401, detail="Missing Ecowitt authentication")
    with db_session:
        device = ecowitt.list_devices()[0]
        # region History readings
        history_readings = ecowitt.get_history_readings(
            device=device.mac,
            category=Category.TEMPERATURE,
            start_date=settings.last_updated.temperature,
        )
        for timestamp, value in history_readings.items():
            if reading := TemperatureReading.get(datestamp=timestamp.date()):
                if value > reading.high:
                    reading.high = value
                if value < reading.low:
                    reading.low = value
            else:
                reading = TemperatureReading(datestamp=timestamp.date(), high=value, low=value)
        # endregion
        # region Live reading
        live_reading = ecowitt.get_live_reading(device=device.mac, category=Category.RAINFALL)
        if live_reading:
            if reading := TemperatureReading.get(datestamp=live_reading.time.date()):
                if live_reading.value > reading.high:
                    reading.high = live_reading.value
                if live_reading.value < reading.low:
                    reading.low = live_reading.value
            else:
                reading = TemperatureReading(
                    datestamp=live_reading.time.date(),
                    high=live_reading.value,
                    low=live_reading.value,
                )
        # endregion
    settings.last_updated.temperature = datetime.now()  # noqa: DTZ005
    settings.save()
