__all__ = ["update_data"]

import logging
from datetime import datetime
from decimal import Decimal

from common.services.ecowitt import Category, Ecowitt
from common.services.exceptions import ServiceError
from common.settings import Settings
from common.storage import Reading, to_file

LOGGER = logging.getLogger(__name__)


def _retrieve_live_readings(ecowitt: Ecowitt, device: tuple[str, str]) -> None:
    LOGGER.info(f"Pulling live readings for device '{device[1]}'")
    timestamp, rainfall = ecowitt.get_device_reading(mac=device[0], category=Category.RAINFALL)
    to_file(Reading(timestamp=timestamp.date(), value=Decimal(rainfall)))


def _retrieve_historical_readings(
    ecowitt: Ecowitt, device: tuple[str, str], last_updated: datetime
) -> None:
    LOGGER.info(f"Pulling historical readings for device '{device[1]}'")
    if history := ecowitt.list_device_history(
        mac=device[0], last_updated=last_updated, category=Category.RAINFALL
    ):
        for timestamp, rainfall in history.items():
            to_file(Reading(timestamp=timestamp.date(), value=Decimal(rainfall)))


def update_data(ecowitt: Ecowitt, settings: Settings) -> bool:
    for device in ecowitt.list_devices():
        try:
            _retrieve_historical_readings(
                ecowitt=ecowitt, device=device, last_updated=settings.ecowitt.last_updated
            )
            _retrieve_live_readings(ecowitt=ecowitt, device=device)
            settings.ecowitt.last_updated = datetime.now()
            settings.save()
            return True
        except ServiceError:
            return False
