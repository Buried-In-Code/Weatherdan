__all__ = ["date_list", "device_list"]

from datetime import date

from natsort import humansorted as sorted
from natsort import ns

from common.storage import from_file


def device_list() -> list[str]:
    return sorted({x.device for x in from_file()}, alg=ns.NA | ns.G)


def date_list() -> list[date]:
    return sorted({x.timestamp for x in from_file()}, alg=ns.NA | ns.G)
