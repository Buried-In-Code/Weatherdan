__all__ = ["add_entry", "remove_entry", "write_to_file", "read_from_file"]

import csv
from datetime import date
from decimal import Decimal

from weatherdan import get_data_root
from weatherdan.models import Reading

DATA_FILE = get_data_root() / "weatherdan-data.csv"


def add_entry(entry: Reading) -> None:
    entries = read_from_file()
    if entry in entries:
        entries.remove(entry)
    entries.add(entry)
    write_to_file(entries=entries)


def remove_entry(timestamp: date) -> None:
    temp = Reading(timestamp=timestamp, value=Decimal(-1))
    entries = read_from_file()
    if temp in entries:
        entries.remove(temp)
    write_to_file(entries=entries)


def write_to_file(entries: set[Reading]) -> None:
    with DATA_FILE.open("w", encoding="UTF-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["Timestamp", "Value"])
        for entry in sorted(entries, key=lambda x: x.timestamp, reverse=True):
            writer.writerow([entry.timestamp.isoformat(), entry.value])


def read_from_file() -> set[Reading]:
    output = set()
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="UTF-8") as stream:
            reader = csv.DictReader(stream)
            for entry in reader:
                output.add(
                    Reading(
                        timestamp=date.fromisoformat(entry["Timestamp"]),
                        value=Decimal(entry["Value"]),
                    ),
                )
    return output
