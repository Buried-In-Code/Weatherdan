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

from weatherdan.models import Reading

db = Database()


class RainfallReading(db.Entity):
    _table_ = "rainfall"

    datestamp: date = PrimaryKey(date)
    value: Decimal = Required(Decimal)

    def to_model(self: Self) -> Reading:
        return Reading(
            datestamp=self.datestamp,
            value=self.value,
        )

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, RainfallReading):
            raise NotImplementedError
        return self.datestamp < other.datestamp


class SolarReading(db.Entity):
    _table_ = "solar"

    datestamp: date = PrimaryKey(date)
    value: Decimal = Required(Decimal)

    def to_model(self: Self) -> Reading:
        return Reading(
            datestamp=self.datestamp,
            value=self.value,
        )

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, SolarReading):
            raise NotImplementedError
        return self.datestamp < other.datestamp


class UVIndexReading(db.Entity):
    _table_ = "uv_index"

    datestamp: date = PrimaryKey(date)
    value: Decimal = Required(Decimal)

    def to_model(self: Self) -> Reading:
        return Reading(
            datestamp=self.datestamp,
            value=self.value,
        )

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, UVIndexReading):
            raise NotImplementedError
        return self.datestamp < other.datestamp


class WindReading(db.Entity):
    _table_ = "wind"

    datestamp: date = PrimaryKey(date)
    value: Decimal = Required(Decimal)

    def to_model(self: Self) -> Reading:
        return Reading(
            datestamp=self.datestamp,
            value=self.value,
        )

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, WindReading):
            raise NotImplementedError
        return self.datestamp < other.datestamp
