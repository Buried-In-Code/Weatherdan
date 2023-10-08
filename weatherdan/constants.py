__all__ = ["Constants"]

import logging
import sys
from functools import cached_property
from typing import Self

from weatherdan.ecowitt.service import Ecowitt
from weatherdan.settings import Settings

LOGGER = logging.getLogger("weatherdan")


class Constants:
    @cached_property
    def settings(self: Self) -> Settings:
        return Settings.load()

    @cached_property
    def ecowitt(self: Self) -> Ecowitt:
        if not self.settings.ecowitt.application_key:
            sys.exit("Missing Ecowitt credential: application_key")
        if not self.settings.ecowitt.api_key:
            sys.exit("Missing Ecowitt credential: api_key")
        ecowitt = Ecowitt(
            application_key=self.settings.ecowitt.application_key,
            api_key=self.settings.ecowitt.api_key,
        )
        if not ecowitt.test_credentials():
            sys.exit("Invalid Ecowitt credentials")
        return ecowitt
