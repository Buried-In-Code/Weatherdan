__all__ = ["router"]

import logging
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum

from fastapi import APIRouter, Body, Query
from fastapi.exceptions import HTTPException
from pony.orm import db_session

from weatherdan.constants import constants
from weatherdan.database.tables import RainfallReading
from weatherdan.ecowitt.category import Category
from weatherdan.models import Reading, WeekReading
from weatherdan.responses import ErrorResponse
from weatherdan.utils import (
    get_daily_readings,
    get_monthly_total_readings,
    get_weekly_total_readings,
    get_yearly_total_readings,
)

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


@router.get(path="")
def list_readings(
    *,
    timeframe: Timeframe = Timeframe.DAILY,
    year: int | None = None,
    month: int | None = None,
    max_entries: int = Query(alias="max-entries", default=28),
) -> list[Reading | WeekReading]:
    with db_session:
        entries = sorted(x.to_model() for x in RainfallReading.select())
        if timeframe == Timeframe.DAILY:
            return get_daily_readings(entries=entries, year=year, month=month)[-max_entries:]
        if timeframe == Timeframe.WEEKLY:
            return get_weekly_total_readings(entries=entries, year=year, month=month)[-max_entries:]
        if timeframe == Timeframe.MONTHLY:
            return get_monthly_total_readings(entries=entries, year=year)[-max_entries:]
        return get_yearly_total_readings(entries=entries)[-max_entries:]


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
    def update_reading(datestamp: date, value: Decimal) -> None:
        if reading := RainfallReading.get(datestamp=datestamp):
            if value > reading.value:
                reading.value = value
        else:
            reading = RainfallReading(datestamp=datestamp, value=value)

    temp_time = datetime.now() - timedelta(hours=3)
    if not force and constants.settings.last_updated.rainfall >= temp_time:
        raise HTTPException(status_code=208, detail="No update needed")
    with db_session:
        # region History readings
        history_readings = constants.ecowitt.get_history_readings(
            device=constants.ecowitt.device.mac,
            category=Category.RAINFALL,
            start_date=constants.settings.last_updated.rainfall,
        )
        for timestamp, value in history_readings.items():
            update_reading(datestamp=timestamp.date(), value=value)
        # endregion
        # region Live reading
        if live_reading := constants.ecowitt.get_live_reading(
            device=constants.ecowitt.device.mac,
            category=Category.RAINFALL,
        ):
            update_reading(datestamp=live_reading.time.date(), value=live_reading.value)
        # endregion
    constants.settings.last_updated.rainfall = datetime.now()
    constants.settings.save()
