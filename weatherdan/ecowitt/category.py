__all__ = ["Category"]

from enum import Enum
from typing import Self


class Category(Enum):
    RAINFALL = "rainfall.daily"
    TEMPERATURE = "indoor.temperature"
    HUMIDITY = "indoor.humidity"

    @property
    def group_1(self: Self) -> str:
        return self.value.split(".")[0]

    @property
    def group_2(self: Self) -> str:
        return self.value.split(".")[1]
