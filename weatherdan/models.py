__all__ = ["Reading", "WeekReading", "MonthReading", "YearReading"]

from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class Reading(BaseModel):
    timestamp: date
    value: Decimal

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, Reading):
            raise NotImplementedError
        return self.timestamp < other.timestamp

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, Reading):
            raise NotImplementedError
        return self.timestamp == other.timestamp

    def __hash__(self):
        return hash((type(self), self.timestamp))


class WeekReading(BaseModel):
    start_timestamp: date
    end_timestamp: date
    value: Decimal

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, WeekReading):
            raise NotImplementedError
        return self.start_timestamp < other.start_timestamp

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, WeekReading):
            raise NotImplementedError
        return self.start_timestamp == other.start_timestamp

    def __hash__(self):
        return hash((type(self), self.start_timestamp))


class MonthReading(BaseModel):
    timestamp: date
    value: Decimal

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, MonthReading):
            raise NotImplementedError
        return self.timestamp < other.timestamp

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, MonthReading):
            raise NotImplementedError
        return self.timestamp == other.timestamp

    def __hash__(self):
        return hash((type(self), self.timestamp))


class YearReading(BaseModel):
    timestamp: date
    value: Decimal

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, YearReading):
            raise NotImplementedError
        return self.timestamp < other.timestamp

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, YearReading):
            raise NotImplementedError
        return self.timestamp == other.timestamp

    def __hash__(self):
        return hash((type(self), self.timestamp))
