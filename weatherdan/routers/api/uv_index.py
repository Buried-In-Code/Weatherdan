__all__ = ["router"]

import logging
from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session, select

from weatherdan.constants import constants
from weatherdan.database import get_session
from weatherdan.ecowitt.category import Category
from weatherdan.models import GraphData, Reading, UVIndex
from weatherdan.responses import ErrorResponse
from weatherdan.routers.api.timeframe import Timeframe
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
    prefix="/uv-index",
    tags=["UV Index"],
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
LOGGER = logging.getLogger(__name__)


@router.get(path="")
def list_readings(
    *,
    session: Annotated[Session, Depends(get_session)],
    timeframe: Annotated[Timeframe, Query()] = Timeframe.DAILY,
    year: Annotated[int | None, Query()] = None,
    month: Annotated[int | None, Query()] = None,
    max_entries: Annotated[int, Query(alias="max-entries")] = 28,
) -> list[Reading] | GraphData:
    readings = sorted(session.exec(select(UVIndex)).all())
    if timeframe == Timeframe.DAILY:
        return get_daily_readings(entries=readings, year=year, month=month)[-max_entries:]
    if timeframe == Timeframe.WEEKLY:
        return GraphData(
            high=get_weekly_high_readings(entries=readings, year=year, month=month)[-max_entries:],
            low=get_weekly_low_readings(entries=readings, year=year, month=month)[-max_entries:],
            average=get_weekly_average_readings(entries=readings, year=year, month=month)[
                -max_entries:
            ],
        )
    if timeframe == Timeframe.MONTHLY:
        return GraphData(
            high=get_monthly_high_readings(entries=readings, year=year)[-max_entries:],
            low=get_monthly_low_readings(entries=readings, year=year)[-max_entries:],
            average=get_monthly_average_readings(entries=readings, year=year)[-max_entries:],
        )
    return GraphData(
        high=get_yearly_high_readings(entries=readings)[-max_entries:],
        low=get_yearly_low_readings(entries=readings)[-max_entries:],
        average=get_yearly_average_readings(entries=readings)[-max_entries:],
    )


@router.post(path="", status_code=201)
def add_reading(
    *,
    session: Annotated[Session, Depends(get_session)],
    body: Annotated[Reading, Body(alias="input")],
) -> UVIndex:
    if reading := session.get(UVIndex, body.datestamp):
        reading.value = body.value
    else:
        reading = UVIndex.model_validate(body)
    session.add(reading)
    session.commit()
    session.refresh(reading)
    return reading


@router.delete(path="", status_code=204)
def remove_reading(
    *,
    session: Annotated[Session, Depends(get_session)],
    datestamp: Annotated[date, Body(embed=True)],
) -> None:
    reading = session.get(UVIndex, datestamp)
    if not reading:
        raise HTTPException(status_code=404, detail="Reading doesn't exist")
    session.delete(reading)
    session.commit()


@router.put(path="", status_code=204)
def refresh_readings(
    *, session: Annotated[Session, Depends(get_session)], force: Annotated[bool, Query()] = False
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
            reading.value = max(value, reading.value)
        else:
            reading = UVIndex(datestamp=timestamp.date(), value=value)
        session.add(reading)
    # endregion
    # region Live reading
    if live_reading := constants.ecowitt.get_live_reading(
        device=constants.ecowitt.device.mac, category=Category.UV_INDEX
    ):
        if reading := session.get(UVIndex, live_reading.time.date()):
            reading.value = max(live_reading.value, reading.value)
        else:
            reading = UVIndex(datestamp=live_reading.time.date(), value=live_reading.value)
        session.add(reading)
    # endregion
    session.commit()
    constants.settings.last_updated.uv_index = datetime.now()
    constants.settings.save()
