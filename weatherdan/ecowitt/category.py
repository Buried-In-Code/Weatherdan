__all__ = ["Category"]

from enum import Enum
from typing import Self


class Category(Enum):
    PRESSURE = "pressure.relative"
    RAINFALL = "rainfall.daily"
    SOLAR = "solar_and_uvi.solar"
    UV_INDEX = "solar_and_uvi.uvi"
    WIND = "wind.wind_speed"

    @property
    def group_1(self: Self) -> str:
        return self.value.split(".")[0]

    @property
    def group_2(self: Self) -> str:
        return self.value.split(".")[1]
