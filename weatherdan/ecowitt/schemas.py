__all__ = ["Device", "LiveReading"]

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel as PyModel


class BaseModel(
    PyModel,
    populate_by_name=True,
    str_strip_whitespace=True,
    extra="forbid",
):
    pass


class Device(BaseModel):
    id: int  # noqa: A003
    name: str
    mac: str
    type: int  # noqa: A003
    date_zone_id: str
    createtime: datetime
    longitude: Decimal
    latitude: Decimal
    stationtype: str


class LiveReading(BaseModel):
    time: datetime
    unit: str
    value: Decimal
