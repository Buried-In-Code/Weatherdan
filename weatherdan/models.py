__all__ = ["GraphData", "WeekGraphData", "Reading", "WeekReading"]

from datetime import date
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, Field


class Reading(BaseModel):
    datestamp: date
    value: Decimal

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


class GraphData(BaseModel):
    high: list[Reading] = Field(default_factory=list)
    average: list[Reading] = Field(default_factory=list)
    low: list[Reading] = Field(default_factory=list)


class WeekGraphData(BaseModel):
    high: list[WeekReading] = Field(default_factory=list)
    average: list[WeekReading] = Field(default_factory=list)
    low: list[WeekReading] = Field(default_factory=list)
