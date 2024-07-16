__all__ = ["router"]

import logging
from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session, select

from weatherdan.constants import constants
from weatherdan.database import get_session
from weatherdan.ecowitt.category import Category
from weatherdan.models import Reading, UVIndex, WeekReading
from weatherdan.responses import ErrorResponse
from weatherdan.routers.api.timeframe import Timeframe
from weatherdan.utils import (
    get_daily_readings,
    get_monthly_total_readings,
    get_weekly_total_readings,
    get_yearly_total_readings,
)

router = APIRouter(
    prefix="/uv-index",
    tags=["UV Index"],
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
LOGGER = logging.getLogger(__name__)


@router.get(path="")
def list_readings(
    *,
    session: Annotated[Session, Depends(get_session)],
    timeframe: Timeframe = Timeframe.DAILY,
    year: int | None = None,
    month: int | None = None,
    max_entries: int = Query(alias="max-entries", default=28),
) -> list[Reading | WeekReading]:
    readings = sorted(session.exec(select(UVIndex)).all())
    if timeframe == Timeframe.DAILY:
        return get_daily_readings(entries=readings, year=year, month=month)[-max_entries:]
    if timeframe == Timeframe.WEEKLY:
        return get_weekly_total_readings(entries=readings, year=year, month=month)[-max_entries:]
    if timeframe == Timeframe.MONTHLY:
        return get_monthly_total_readings(entries=readings, year=year)[-max_entries:]
    return get_yearly_total_readings(entries=readings)[-max_entries:]


@router.post(path="", status_code=201)
def add_reading(*, session: Annotated[Session, Depends(get_session)], input: Reading) -> UVIndex:  # noqa: A002
    if reading := session.get(UVIndex, input.datestamp):
        reading.value = input.value
    else:
        reading = UVIndex.model_validate(input)
    session.add(reading)
    session.commit()
    session.refresh(reading)
    return reading


@router.delete(path="", status_code=204)
def remove_reading(
    *, session: Annotated[Session, Depends(get_session)], datestamp: date = Body(embed=True)
) -> None:
    reading = session.get(UVIndex, datestamp)
    if not reading:
        raise HTTPException(status_code=404, detail="Reading doesn't exist")
    session.delete(reading)
    session.commit()


@router.put(path="", status_code=204)
def refresh_readings(
    *, session: Annotated[Session, Depends(get_session)], force: bool = False
) -> None:
    temp_time = datetime.now() - timedelta(hours=3)
    if not force and constants.settings.last_updated.uv_index >= temp_time:
        raise HTTPException(status_code=208, detail="No update needed")
    # region History readings
    history_readings = constants.ecowitt.get_history_readings(
        device=constants.ecowitt.device.mac,
        category=Category.UV_INDEX,
        start_date=constants.settings.last_updated.uv_index,
    )
    for timestamp, value in history_readings.items():
        if reading := session.get(UVIndex, timestamp.date()):
            if value > reading.value:
                reading.value = value
        else:
            reading = UVIndex(datestamp=timestamp.date(), value=value)
        session.add(reading)
    # endregion
    # region Live reading
    if live_reading := constants.ecowitt.get_live_reading(
        device=constants.ecowitt.device.mac, category=Category.UV_INDEX
    ):
        if reading := session.get(UVIndex, live_reading.time.date()):
            if live_reading.value > reading.value:
                reading.value = live_reading.value
        else:
            reading = UVIndex(datestamp=live_reading.time.date(), value=live_reading.value)
        session.add(reading)
    # endregion
    session.commit()
    constants.settings.last_updated.uv_index = datetime.now()
    constants.settings.save()
