__all__ = [
    "RainfallReading",
    "SolarReading",
    "UVIndexReading",
    "WindReading",
]

from datetime import date
from decimal import Decimal
from typing import Self

from pony.orm import Database, PrimaryKey, Required

from weatherdan.models import HighReading, TotalReading

db = Database()


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


class UVIndexReading(db.Entity):
    _table_ = "uv_index"

    datestamp: date = PrimaryKey(date)
    high: Decimal = Required(Decimal)

    def to_model(self: Self) -> HighReading:
        return HighReading(
            datestamp=self.datestamp,
            high=self.high,
        )


class WindReading(db.Entity):
    _table_ = "wind"

    datestamp: date = PrimaryKey(date)
    high: Decimal = Required(Decimal)

    def to_model(self: Self) -> HighReading:
        return HighReading(
            datestamp=self.datestamp,
            high=self.high,
        )
