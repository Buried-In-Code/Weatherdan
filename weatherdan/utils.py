__all__ = [
    "get_daily_readings",
    "get_weekly_total_readings",
    "get_monthly_total_readings",
    "get_yearly_total_readings",
    "get_weekly_high_readings",
    "get_monthly_high_readings",
    "get_yearly_high_readings",
    "get_weekly_average_readings",
    "get_monthly_average_readings",
    "get_yearly_average_readings",
    "get_weekly_low_readings",
    "get_monthly_low_readings",
    "get_yearly_low_readings",
]

from collections.abc import Callable
from datetime import date, timedelta

from weatherdan.models import Reading, WeekReading


def get_week_ends(value: date) -> tuple[date, date]:
    start = value - timedelta(days=value.isoweekday() - 1)
    end = start + timedelta(days=6)
    return start, end


def filter_entries(
    entries: list[Reading],
    year: int | None = None,
    month: int | None = None,
) -> list[Reading]:
    if year:
        entries = [x for x in entries if x.datestamp.year == year]
    if month:
        entries = [x for x in entries if x.datestamp.month == month]
    return entries


def filter_week_entries(
    entries: list[WeekReading],
    year: int | None = None,
    month: int | None = None,
) -> list[WeekReading]:
    if year:
        entries = [x for x in entries if year in (x.start_datestamp.year, x.end_datestamp.year)]
    if month:
        entries = [x for x in entries if month in (x.start_datestamp.month, x.end_datestamp.month)]
    return entries


def aggregate_entries(
    entries: list[Reading],
    grouping: Callable[[date], date | tuple[date, date]],
    aggregation: Callable[[date | tuple[date, date], list[Reading]], Reading | WeekReading],
) -> list[Reading | WeekReading]:
    grouped = {}
    for entry in entries:
        key = grouping(entry.datestamp)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(entry)
    return [aggregation(key, values) for key, values in grouped.items()]


def get_daily_readings(
    entries: list[Reading],
    year: int | None = None,
    month: int | None = None,
) -> list[Reading]:
    return filter_entries(entries=entries, year=year, month=month)


def week_grouping(value: date) -> tuple[date, date]:
    return get_week_ends(value=value)


def month_grouping(value: date) -> date:
    return value.replace(day=1)


def year_grouping(value: date) -> date:
    return value.replace(month=1, day=1)


def total_aggregation(key: date, values: list[Reading]) -> Reading:
    return Reading(datestamp=key, value=sum(x.value for x in values))


def total_week_aggregation(key: tuple[date, date], values: list[Reading]) -> WeekReading:
    return WeekReading(
        start_datestamp=key[0],
        end_datestamp=key[1],
        value=sum(x.value for x in values),
    )


def high_aggregation(key: date, values: list[Reading]) -> Reading:
    return Reading(datestamp=key, value=max(x.value for x in values))


def high_week_aggregation(key: tuple[date, date], values: list[Reading]) -> WeekReading:
    return WeekReading(
        start_datestamp=key[0],
        end_datestamp=key[1],
        value=max(x.value for x in values),
    )


def average_aggregation(key: date, values: list[Reading]) -> Reading:
    values = [x.value for x in values]
    return Reading(datestamp=key, value=round(sum(values) / len(values), 2))


def average_week_aggregation(key: tuple[date, date], values: list[Reading]) -> WeekReading:
    values = [x.value for x in values]
    return WeekReading(
        start_datestamp=key[0],
        end_datestamp=key[1],
        value=round(sum(values) / len(values), 2),
    )


def low_aggregation(key: date, values: list[Reading]) -> Reading:
    return Reading(datestamp=key, value=min(x.value for x in values))


def low_week_aggregation(key: tuple[date, date], values: list[Reading]) -> WeekReading:
    return WeekReading(
        start_datestamp=key[0],
        end_datestamp=key[1],
        value=min(x.value for x in values),
    )


def get_weekly_total_readings(
    entries: list[Reading],
    year: int | None = None,
    month: int | None = None,
) -> list[WeekReading]:
    entries = aggregate_entries(
        entries=entries,
        grouping=week_grouping,
        aggregation=total_week_aggregation,
    )
    return filter_week_entries(entries=entries, year=year, month=month)


def get_weekly_high_readings(
    entries: list[Reading],
    year: int | None = None,
    month: int | None = None,
) -> list[WeekReading]:
    entries = aggregate_entries(
        entries=entries,
        grouping=week_grouping,
        aggregation=high_week_aggregation,
    )
    return filter_week_entries(entries=entries, year=year, month=month)


def get_weekly_average_readings(
    entries: list[Reading],
    year: int | None = None,
    month: int | None = None,
) -> list[WeekReading]:
    entries = aggregate_entries(
        entries=entries,
        grouping=week_grouping,
        aggregation=average_week_aggregation,
    )
    return filter_week_entries(entries=entries, year=year, month=month)


def get_weekly_low_readings(
    entries: list[Reading],
    year: int | None = None,
    month: int | None = None,
) -> list[WeekReading]:
    entries = aggregate_entries(
        entries=entries,
        grouping=week_grouping,
        aggregation=low_week_aggregation,
    )
    return filter_week_entries(entries=entries, year=year, month=month)


def get_monthly_total_readings(entries: list[Reading], year: int | None = None) -> list[Reading]:
    entries = aggregate_entries(
        entries=entries,
        grouping=month_grouping,
        aggregation=total_aggregation,
    )
    return filter_entries(entries=entries, year=year)


def get_monthly_high_readings(entries: list[Reading], year: int | None = None) -> list[Reading]:
    entries = aggregate_entries(
        entries=entries,
        grouping=month_grouping,
        aggregation=high_aggregation,
    )
    return filter_entries(entries=entries, year=year)


def get_monthly_average_readings(entries: list[Reading], year: int | None = None) -> list[Reading]:
    entries = aggregate_entries(
        entries=entries,
        grouping=month_grouping,
        aggregation=average_aggregation,
    )
    return filter_entries(entries=entries, year=year)


def get_monthly_low_readings(entries: list[Reading], year: int | None = None) -> list[Reading]:
    entries = aggregate_entries(
        entries=entries,
        grouping=month_grouping,
        aggregation=low_aggregation,
    )
    return filter_entries(entries=entries, year=year)


def get_yearly_total_readings(entries: list[Reading]) -> list[Reading]:
    return aggregate_entries(entries=entries, grouping=year_grouping, aggregation=total_aggregation)


def get_yearly_high_readings(entries: list[Reading]) -> list[Reading]:
    return aggregate_entries(entries=entries, grouping=year_grouping, aggregation=high_aggregation)


def get_yearly_average_readings(entries: list[Reading]) -> list[Reading]:
    return aggregate_entries(
        entries=entries,
        grouping=year_grouping,
        aggregation=average_aggregation,
    )


def get_yearly_low_readings(entries: list[Reading]) -> list[Reading]:
    return aggregate_entries(entries=entries, grouping=year_grouping, aggregation=low_aggregation)
