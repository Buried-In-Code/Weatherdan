__all__ = [
    "load_daily_stats",
    "load_weekly_stats",
    "load_monthly_stats",
    "load_yearly_stats",
]

from datetime import date, timedelta

from common.storage import from_file


def load_daily_stats() -> dict[date, float]:
    daily = sorted(from_file(), key=lambda x: x.timestamp, reverse=True)
    return {x.timestamp: x.value for x in daily}


def load_weekly_stats() -> dict[tuple[date, date], float]:
    def get_week_ends(datestamp: date) -> tuple[date, date]:
        start = datestamp - timedelta(days=datestamp.isoweekday() - 1)
        end = start + timedelta(days=6)
        return start, end

    weekly = {}
    for entry in sorted(from_file(), key=lambda x: x.timestamp, reverse=True):
        key = get_week_ends(entry.timestamp)
        if key not in weekly:
            weekly[key] = 0.0
        weekly[key] += entry.value
    return weekly


def load_monthly_stats() -> dict[date, float]:
    monthly = {}
    for entry in sorted(from_file(), key=lambda x: x.timestamp, reverse=True):
        key = entry.timestamp.replace(day=1)
        if key not in monthly:
            monthly[key] = 0.0
        monthly[key] += entry.value
    return monthly


def load_yearly_stats() -> dict[date, float]:
    yearly = {}
    for entry in sorted(from_file(), key=lambda x: x.timestamp, reverse=True):
        key = entry.timestamp.replace(day=1, month=1)
        if key not in yearly:
            yearly[key] = 0.0
        yearly[key] += entry.value
    return yearly
