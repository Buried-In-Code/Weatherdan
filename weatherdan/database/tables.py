__all__ = ["HumidityReading", "RainfallReading", "TemperatureReading"]

from datetime import date
from decimal import Decimal
from typing import Self

from pony.orm import Database, Optional, PrimaryKey, Required

from weatherdan.models import RangeReading, Reading

db = Database()


class RainfallReading(db.Entity):
    _table_ = "rainfall"

    datestamp: date = PrimaryKey(date)
    value: Decimal = Optional(Decimal, default=Decimal(0), sql_default=0)

    def to_model(self: Self) -> Reading:
        return Reading(
            datestamp=self.datestamp,
            value=self.value,
        )


class TemperatureReading(db.Entity):
    _table_ = "temperature"

    datestamp: date = PrimaryKey(date)
    high: Decimal = Required(Decimal)
    low: Decimal = Required(Decimal)

    def to_model(self: Self) -> RangeReading:
        return RangeReading(
            datestamp=self.datestamp,
            high=self.high,
            low=self.low,
        )


class HumidityReading(db.Entity):
    _table_ = "humidity"

    datestamp: date = PrimaryKey(date)
    high: Decimal = Required(Decimal)
    low: Decimal = Required(Decimal)

    def to_model(self: Self) -> RangeReading:
        return RangeReading(
            datestamp=self.datestamp,
            high=self.high,
            low=self.low,
        )
