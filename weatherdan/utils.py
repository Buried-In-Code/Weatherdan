__all__ = [
    "get_week_ends",
    "get_daily_readings",
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

import sys
from datetime import date, timedelta
from decimal import Decimal

from weatherdan.models import Reading, WeekReading


def get_week_ends(value: date) -> tuple[date, date]:
    start = value - timedelta(days=value.isoweekday() - 1)
    end = start + timedelta(days=6)
    return start, end


def get_daily_readings(
    entries: list[Reading],
    year: int | None = None,
    month: int | None = None,
) -> list[Reading]:
    if year:
        entries = [x for x in entries if x.datestamp.year == year]
    if month:
        entries = [x for x in entries if x.datestamp.month == month]
    return entries


def get_weekly_high_readings(
    entries: list[Reading],
    year: int | None = None,
    month: int | None = None,
) -> list[WeekReading]:
    weekly = {}
    for entry in entries:
        key = get_week_ends(value=entry.datestamp)
        if key not in weekly:
            weekly[key] = WeekReading(
                start_datestamp=key[0],
                end_datestamp=key[1],
                value=Decimal(0),
            )
        if entry.value > weekly[key].value:
            weekly[key].value = entry.value
    entries = sorted(weekly.values())
    if year:
        entries = [x for x in entries if year in (x.start_datestamp.year, x.end_datestamp.year)]
    if month:
        entries = [x for x in entries if month in (x.start_datestamp.month, x.end_datestamp.month)]
    return entries


def get_monthly_high_readings(entries: list[Reading], year: int | None = None) -> list[Reading]:
    monthly = {}
    for entry in entries:
        key = entry.datestamp.replace(day=1)
        if key not in monthly:
            monthly[key] = Reading(datestamp=key, value=Decimal(0))
        if entry.value > monthly[key].value:
            monthly[key].value = entry.value
    entries = sorted(monthly.values())
    if year:
        entries = [x for x in entries if x.datestamp.year == year]
    return entries


def get_yearly_high_readings(entries: list[Reading]) -> list[Reading]:
    yearly = {}
    for entry in entries:
        key = entry.datestamp.replace(day=1, month=1)
        if key not in yearly:
            yearly[key] = Reading(datestamp=key, value=Decimal(0))
        if entry.value > yearly[key].value:
            yearly[key].value = entry.value
    return sorted(yearly.values())


def get_weekly_average_readings(
    entries: list[Reading],
    year: int | None = None,
    month: int | None = None,
) -> list[WeekReading]:
    weekly = {}
    for entry in entries:
        key = get_week_ends(value=entry.datestamp)
        if key not in weekly:
            weekly[key] = []
        weekly[key].append(entry.value)
    entries = [
        WeekReading(
            start_datestamp=key[0],
            end_datestamp=key[1],
            value=round(sum(value) / len(value), 2),
        )
        for key, value in weekly.items()
    ]
    if year:
        entries = [x for x in entries if year in (x.start_datestamp.year, x.end_datestamp.year)]
    if month:
        entries = [x for x in entries if month in (x.start_datestamp.month, x.end_datestamp.month)]
    return entries


def get_monthly_average_readings(entries: list[Reading], year: int | None = None) -> list[Reading]:
    monthly = {}
    for entry in entries:
        key = entry.datestamp.replace(day=1)
        if key not in monthly:
            monthly[key] = []
        monthly[key].append(entry.value)
    entries = [
        Reading(datestamp=key, value=round(sum(value) / len(value), 2))
        for key, value in monthly.items()
    ]
    if year:
        entries = [x for x in entries if x.datestamp.year == year]
    return entries


def get_yearly_average_readings(entries: list[Reading]) -> list[Reading]:
    yearly = {}
    for entry in entries:
        key = entry.datestamp.replace(day=1, month=1)
        if key not in yearly:
            yearly[key] = []
        yearly[key].append(entry.value)
    return [
        Reading(datestamp=key, value=round(sum(value) / len(value), 2))
        for key, value in yearly.items()
    ]


def get_weekly_low_readings(
    entries: list[Reading],
    year: int | None = None,
    month: int | None = None,
) -> list[WeekReading]:
    weekly = {}
    for entry in entries:
        key = get_week_ends(value=entry.datestamp)
        if key not in weekly:
            weekly[key] = WeekReading(
                start_datestamp=key[0],
                end_datestamp=key[1],
                value=Decimal(sys.maxsize),
            )
        if entry.value < weekly[key].value:
            weekly[key].value = entry.value
    entries = sorted(weekly.values())
    if year:
        entries = [x for x in entries if year in (x.start_datestamp.year, x.end_datestamp.year)]
    if month:
        entries = [x for x in entries if month in (x.start_datestamp.month, x.end_datestamp.month)]
    return entries


def get_monthly_low_readings(entries: list[Reading], year: int | None = None) -> list[Reading]:
    monthly = {}
    for entry in entries:
        key = entry.datestamp.replace(day=1)
        if key not in monthly:
            monthly[key] = Reading(datestamp=key, value=Decimal(sys.maxsize))
        if entry.value < monthly[key].value:
            monthly[key].value = entry.value
    entries = sorted(monthly.values())
    if year:
        entries = [x for x in entries if x.datestamp.year == year]
    return entries


def get_yearly_low_readings(entries: list[Reading]) -> list[Reading]:
    yearly = {}
    for entry in entries:
        key = entry.datestamp.replace(day=1, month=1)
        if key not in yearly:
            yearly[key] = Reading(datestamp=key, value=Decimal(sys.maxsize))
        if entry.value < yearly[key].value:
            yearly[key].value = entry.value
    return sorted(yearly.values())
