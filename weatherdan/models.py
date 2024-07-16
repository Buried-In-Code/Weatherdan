__all__ = [
    "GraphData",
    "Rainfall",
    "Reading",
    "Solar",
    "UVIndex",
    "WeekReading",
    "Wind",
]

from datetime import date
from decimal import Decimal
from typing import Self

from sqlmodel import Field, SQLModel


class Reading(SQLModel):
    datestamp: date = Field(index=True, primary_key=True)
    value: Decimal


class Rainfall(Reading, table=True):
    __tablename__ = "rainfall"

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, Rainfall):
            raise NotImplementedError
        return self.datestamp < other.datestamp

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, Rainfall):
            raise NotImplementedError
        return self.datestamp == other.datestamp

    def __hash__(self: Self) -> int:
        return hash((type(self), self.datestamp))


class Solar(Reading, table=True):
    __tablename__ = "solar"

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, Solar):
            raise NotImplementedError
        return self.datestamp < other.datestamp

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, Solar):
            raise NotImplementedError
        return self.datestamp == other.datestamp

    def __hash__(self: Self) -> int:
        return hash((type(self), self.datestamp))


class UVIndex(Reading, table=True):
    __tablename__ = "uv_index"

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, UVIndex):
            raise NotImplementedError
        return self.datestamp < other.datestamp

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, UVIndex):
            raise NotImplementedError
        return self.datestamp == other.datestamp

    def __hash__(self: Self) -> int:
        return hash((type(self), self.datestamp))


class Wind(Reading, table=True):
    __tablename__ = "wind"

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, Wind):
            raise NotImplementedError
        return self.datestamp < other.datestamp

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, Wind):
            raise NotImplementedError
        return self.datestamp == other.datestamp

    def __hash__(self: Self) -> int:
        return hash((type(self), self.datestamp))


class WeekReading(SQLModel):
    start_datestamp: date
    end_datestamp: date
    value: Decimal

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


class GraphData(SQLModel):
    high: list[Reading | WeekReading] = Field(default_factory=list)
    average: list[Reading | WeekReading] = Field(default_factory=list)
    low: list[Reading | WeekReading] = Field(default_factory=list)
