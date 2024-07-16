__all__ = ["Timeframe"]

from enum import Enum


class Timeframe(Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"
