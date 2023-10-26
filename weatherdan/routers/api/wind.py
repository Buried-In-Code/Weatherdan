__all__ = ["router"]

import logging
from datetime import date, datetime, timedelta
from enum import Enum

from fastapi import APIRouter, Body, Cookie, Query
from fastapi.exceptions import HTTPException
from pony.orm import db_session

from weatherdan.constants import constants
from weatherdan.database.tables import WindReading
from weatherdan.ecowitt.category import Category
from weatherdan.models import GraphData, Reading, WeekGraphData
from weatherdan.responses import ErrorResponse
from weatherdan.utils import (
    get_daily_readings,
    get_monthly_average_readings,
    get_monthly_high_readings,
    get_monthly_low_readings,
    get_weekly_average_readings,
    get_weekly_high_readings,
    get_weekly_low_readings,
    get_yearly_average_readings,
    get_yearly_high_readings,
    get_yearly_low_readings,
)

router = APIRouter(
    prefix="/wind",
    tags=["Wind"],
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
    all_results: bool = Query(alias="allResults", default=False),
    count: int = Cookie(alias="weatherdan_count", default=28),
) -> GraphData | WeekGraphData:
    if all_results:
        count = 100
    with db_session:
        if timeframe == Timeframe.DAILY:
            return GraphData(
                high=get_daily_readings(
                    entries=sorted([x.to_model() for x in WindReading.select()]),
                    year=year,
                    month=month,
                )[-count:],
            )
        if timeframe == Timeframe.WEEKLY:
            return WeekGraphData(
                high=get_weekly_high_readings(
                    entries=sorted([x.to_model() for x in WindReading.select()]),
                    year=year,
                    month=month,
                )[-count:],
                average=get_weekly_average_readings(
                    entries=sorted([x.to_model() for x in WindReading.select()]),
                    year=year,
                    month=month,
                )[-count:],
                low=get_weekly_low_readings(
                    entries=sorted([x.to_model() for x in WindReading.select()]),
                    year=year,
                    month=month,
                )[-count:],
            )
        if timeframe == Timeframe.MONTHLY:
            return GraphData(
                high=get_monthly_high_readings(
                    entries=sorted([x.to_model() for x in WindReading.select()]),
                    year=year,
                )[-count:],
                average=get_monthly_average_readings(
                    entries=sorted([x.to_model() for x in WindReading.select()]),
                    year=year,
                )[-count:],
                low=get_monthly_low_readings(
                    entries=sorted([x.to_model() for x in WindReading.select()]),
                    year=year,
                )[-count:],
            )
        return GraphData(
            high=get_yearly_high_readings(
                entries=sorted([x.to_model() for x in WindReading.select()]),
            )[-count:],
            average=get_yearly_average_readings(
                entries=sorted([x.to_model() for x in WindReading.select()]),
            )[-count:],
            low=get_yearly_low_readings(
                entries=sorted([x.to_model() for x in WindReading.select()]),
            )[-count:],
        )


@router.post(path="", status_code=201)
def add_reading(*, input: Reading) -> Reading:  # noqa: A002
    with db_session:
        if reading := WindReading.get(datestamp=input.datestamp):
            reading.value = input.value
        else:
            reading = WindReading(datestamp=input.datestamp, value=input.value)
        return reading.to_model()


@router.delete(path="", status_code=204)
def remove_reading(*, datestamp: date = Body(embed=True)) -> None:
    with db_session:
        reading = WindReading.get(datestamp=datestamp)
        if not reading:
            raise HTTPException(status_code=404, detail="Reading doesn't exist")
        reading.delete()


@router.put(path="", status_code=204)
def refresh_readings(*, force: bool = False) -> None:
    temp_time = datetime.now() - timedelta(hours=3)  # noqa: DTZ005
    if not force and constants.settings.last_updated.wind >= temp_time:
        raise HTTPException(status_code=208, detail="No update needed")
    with db_session:
        device = constants.ecowitt.list_devices()[0]
        # region History readings
        history_readings = constants.ecowitt.get_history_readings(
            device=device.mac,
            category=Category.WIND,
            start_date=constants.settings.last_updated.wind,
        )
        for timestamp, value in history_readings.items():
            if reading := WindReading.get(datestamp=timestamp.date()):
                if value > reading.value:
                    reading.value = value
            else:
                reading = WindReading(datestamp=timestamp.date(), value=value)
        # endregion
        # region Live reading
        live_reading = constants.ecowitt.get_live_reading(device=device.mac, category=Category.WIND)
        if live_reading:
            if reading := WindReading.get(datestamp=live_reading.time.date()):
                if live_reading.value > reading.value:
                    reading.value = live_reading.value
            else:
                reading = WindReading(
                    datestamp=live_reading.time.date(),
                    value=live_reading.value,
                )
        # endregion
    constants.settings.last_updated.wind = datetime.now()  # noqa: DTZ005
    constants.settings.save()
