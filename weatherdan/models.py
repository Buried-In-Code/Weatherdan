__all__ = [
    "HighReading",
    "WeekHighReading",
    "RangeReading",
    "WeekRangeReading",
    "TotalReading",
    "WeekTotalReading",
]

from datetime import date
from decimal import Decimal
from typing import Self

from pydantic import BaseModel


class Reading(BaseModel):
    datestamp: date

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, Reading):
            raise NotImplementedError
        return self.datestamp < other.datestamp

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, Reading):
            raise NotImplementedError
        return self.datestamp == other.datestamp

    def __hash__(self: Self) -> int:
        return hash((type(self), self.datestamp))


class WeekReading(BaseModel):
    start_datestamp: date
    end_datestamp: date

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, WeekReading):
            raise NotImplementedError
        if self.start_datestamp != other.start_datestamp:
            return self.start_datestamp < other.start_datestamp
        return self.end_datestamp < other.end_datestamp

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, WeekReading):
            raise NotImplementedError
        if self.start_datestamp != other.start_datestamp:
            return self.start_datestamp == other.start_datestamp
        return self.end_datestamp == other.end_datestamp

    def __hash__(self: Self) -> int:
        return hash((type(self), self.start_datestamp, self.end_datestamp))


class HighReading(Reading):
    high: Decimal


class WeekHighReading(WeekReading):
    high: Decimal


class RangeReading(Reading):
    high: Decimal
    low: Decimal


class WeekRangeReading(WeekReading):
    high: Decimal
    low: Decimal


class TotalReading(Reading):
    total: Decimal = Decimal(0)


class WeekTotalReading(WeekReading):
    total: Decimal = Decimal(0)
