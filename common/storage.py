__all__ = ["Reading", "to_file", "from_file"]

import csv
from dataclasses import dataclass
from datetime import date

from common import get_project_root

DATA_FILE = get_project_root() / "data.csv"


@dataclass
class Reading:
    timestamp: date
    value: float

    def __hash__(self):
        return hash(self.timestamp)


def to_file(*new_entries: Reading):
    contents = from_file() | set(new_entries)
    with DATA_FILE.open("w", encoding="UTF-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["Timestamp", "Value"])
        for entry in sorted(contents, key=lambda x: x.timestamp, reverse=True):
            writer.writerow([entry.timestamp.isoformat(), entry.value])


def from_file() -> set[Reading]:
    output = set()
    if not DATA_FILE.exists():
        return output
    with DATA_FILE.open("r", encoding="UTF-8") as stream:
        reader = csv.DictReader(stream)
        for entry in reader:
            output.add(
                Reading(
                    timestamp=date.fromisoformat(entry["Timestamp"]),
                    value=float(entry["Value"]),
                )
            )
    return output
