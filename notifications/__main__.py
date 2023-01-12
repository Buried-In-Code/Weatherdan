import logging
import smtplib
import ssl
import time
from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
from email.message import EmailMessage

from rich import box
from rich.panel import Panel

from common.console import CONSOLE
from common.services.ecowitt import Category, Ecowitt
from common.services.exceptions import ServiceError
from common.settings import EmailSettings, Settings
from notifications import __version__, setup_logging

LOGGER = logging.getLogger("readings")


def send_email(settings: EmailSettings, device: str, email_content: str = "") -> None:
    if not settings.enable:
        return
    LOGGER.info("Sending email")

    message = EmailMessage()
    message["From"] = settings.sender_email
    message["To"] = settings.reciever_emails
    message["Subject"] = f"Ecowitt {device} Status"
    message.set_content(email_content)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=ssl.create_default_context())
        server.login(user=settings.sender_email, password=settings.sender_password)
        server.send_message(msg=message)


def retrieve_readings(ecowitt: Ecowitt, device: tuple[str, str], last_updated: datetime) -> bool:
    try:
        _ = ecowitt.list_device_history(
            mac=device[0], last_updated=last_updated, category=Category.RAINFALL
        )
        _, _ = ecowitt.get_device_reading(mac=device[0], category=Category.RAINFALL)
        return True
    except ServiceError:
        return False


def parse_arguments() -> Namespace:
    parser = ArgumentParser(prog="Weatherdan", allow_abbrev=False)
    parser.version = __version__
    parser.add_argument("--version", action="version")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main() -> None:  # noqa: C901
    args = parse_arguments()
    setup_logging(args.debug)

    CONSOLE.print(
        Panel.fit(
            "Welcome to Weatherdan",
            title="Notifications",
            subtitle=f"v{__version__}",
            box=box.SQUARE,
        ),
        style="bold magenta",
        justify="center",
    )

    settings = Settings.load().save()
    ecowitt = Ecowitt(settings.ecowitt)
    if not ecowitt.test_credentials():
        LOGGER.critical("Invalid Ecowitt credentials")
        return

    active_devices = {}
    while True:
        for device in ecowitt.list_devices():
            if device[0] not in active_devices:
                active_devices[device[0]] = True
            if not retrieve_readings(
                ecowitt=ecowitt, device=device, last_updated=settings.ecowitt.last_updated
            ):
                if active_devices[device[0]]:
                    LOGGER.warning(f"{device[1]} connection lost")
                    send_email(
                        settings=settings.email,
                        device=device[1],
                        email_content=f"Connection to {device[1]} has been lost.",
                    )
                    active_devices[device[0]] = False
            else:
                if not active_devices[device[0]]:
                    LOGGER.info(f"{device[1]} connection restored")
                    send_email(
                        settings=settings.email,
                        device=device[1],
                        email_content=f"Connection to {device[1]} has been restored.",
                    )
                    active_devices[device[0]] = True
        all_devices_live = True
        for _, value in active_devices.items():
            if not value:
                all_devices_live = False
        if all_devices_live:
            settings.ecowitt.last_updated = datetime.now() - timedelta(days=3)
        LOGGER.info("Sleeping for an hour")
        time.sleep(1 * 60 * 60)


if __name__ == "__main__":
    main()
