__all__ = ["update_data"]

import logging
from datetime import UTC, datetime
from decimal import Decimal

from weatherdan.models import Reading
from weatherdan.services.ecowitt import Category, Ecowitt
from weatherdan.services.exceptions import ServiceError
from weatherdan.settings import Settings
from weatherdan.storage import add_entry

LOGGER = logging.getLogger(__name__)


def _retrieve_live_readings(ecowitt: Ecowitt, device: tuple[str, str]) -> None:
    LOGGER.info("Pulling live readings for device '%s'", device[1])
    timestamp, rainfall = ecowitt.get_device_reading(mac=device[0], category=Category.RAINFALL)
    add_entry(entry=Reading(timestamp=timestamp.date(), value=Decimal(rainfall)))


def _retrieve_historical_readings(
    ecowitt: Ecowitt,
    device: tuple[str, str],
    last_updated: datetime,
) -> None:
    LOGGER.info("Pulling historical readings for device '%s'", device[1])
    if history := ecowitt.list_device_history(
        mac=device[0],
        last_updated=last_updated,
        category=Category.RAINFALL,
    ):
        for timestamp, rainfall in history.items():
            add_entry(entry=Reading(timestamp=timestamp.date(), value=Decimal(rainfall)))


def update_data(ecowitt: Ecowitt) -> bool:
    settings = Settings()
    for device in ecowitt.list_devices():
        try:
            _retrieve_historical_readings(
                ecowitt=ecowitt,
                device=device,
                last_updated=settings.ecowitt.last_updated,
            )
            _retrieve_live_readings(ecowitt=ecowitt, device=device)
            settings.ecowitt.last_updated = datetime.now(tz=UTC).astimezone()
            settings.save()
            return True
        except (ServiceError, TypeError):
            return False
    return False
