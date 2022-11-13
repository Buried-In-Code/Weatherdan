import logging
from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
from time import sleep

from common.storage import Reading, to_file
from ecowitt import __version__, setup_logging
from ecowitt.exceptions import ServiceError
from ecowitt.service import Category, Ecowitt
from ecowitt.settings import Settings

SETTINGS = Settings.load()
ECOWITT = Ecowitt(
    application_key=SETTINGS.ecowitt.application_key, api_key=SETTINGS.ecowitt.api_key
)
LOGGER = logging.getLogger("ecowitt")


def pull_ecowitt_history():
    LOGGER.info("Pulling historical Ecowitt data")
    for device in ECOWITT.list_devices():
        history = ECOWITT.list_device_history(
            device, SETTINGS.ecowitt.last_updated, Category.RAINFALL
        )
        if history:
            for timestamp, rainfall in history.items():
                to_file(Reading(timestamp=timestamp.date(), value=float(rainfall)))


def pull_ecowitt_data():
    LOGGER.info("Pulling current Ecowitt data")
    devices = ECOWITT.list_devices()
    for device in devices:
        timestamp, rainfall = ECOWITT.get_device_reading(device, Category.RAINFALL)
        to_file(Reading(timestamp=timestamp.date(), value=float(rainfall)))

    SETTINGS.ecowitt.last_updated = datetime.now() - timedelta(days=3)
    SETTINGS.save()


def parse_arguments() -> Namespace:
    parser = ArgumentParser(prog="Weatherdan", allow_abbrev=False)
    parser.version = __version__
    parser.add_argument("--version", action="version")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main():
    args = parse_arguments()
    setup_logging(args.debug)

    if not ECOWITT.test_credentials():
        LOGGER.critical("Invalid Ecowitt credentials")
        return
    LOGGER.info("Ecowitt account connected")
    try:
        while True:
            try:
                pull_ecowitt_history()
                pull_ecowitt_data()
            except ServiceError as err:
                LOGGER.error(err)
            LOGGER.info("Sleeping for an hour")
            sleep(1 * 60 * 60)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
