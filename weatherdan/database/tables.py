__all__ = [
    "HumidityReading",
    "PressureReading",
    "RainfallReading",
    "SolarReading",
    "TemperatureReading",
]

from datetime import date
from decimal import Decimal
from typing import Self

from pony.orm import Database, PrimaryKey, Required

from weatherdan.models import HighReading, RangeReading, TotalReading

db = Database()


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


class PressureReading(db.Entity):
    _table_ = "pressure"

    datestamp: date = PrimaryKey(date)
    high: Decimal = Required(Decimal)
    low: Decimal = Required(Decimal)

    def to_model(self: Self) -> RangeReading:
        return RangeReading(
            datestamp=self.datestamp,
            high=self.high,
            low=self.low,
        )


class RainfallReading(db.Entity):
    _table_ = "rainfall"

    datestamp: date = PrimaryKey(date)
    total: Decimal = Required(Decimal)

    def to_model(self: Self) -> TotalReading:
        return TotalReading(
            datestamp=self.datestamp,
            total=self.total,
        )


class SolarReading(db.Entity):
    _table_ = "solar"

    datestamp: date = PrimaryKey(date)
    high: Decimal = Required(Decimal)

    def to_model(self: Self) -> HighReading:
        return HighReading(
            datestamp=self.datestamp,
            high=self.high,
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


class UVIndexReading(db.Entity):
    _table_ = "uv_index"

    datestamp: date = PrimaryKey(date)
    high: Decimal = Required(Decimal)

    def to_model(self: Self) -> HighReading:
        return HighReading(
            datestamp=self.datestamp,
            high=self.high,
        )
