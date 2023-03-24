__all__ = ["Reading", "to_file", "from_file"]

import csv
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from weatherdan import get_data_root

DATA_FILE = get_data_root() / "weatherdan-data.csv"


@dataclass
class Reading:
    timestamp: date
    value: Decimal = field(compare=False, hash=False)

    def __lt__(self, other):  # noqa: ANN001
        if not isinstance(other, Reading):
            raise NotImplementedError
        return self.timestamp < other.timestamp

    def __eq__(self, other):  # noqa: ANN001
        if not isinstance(other, Reading):
            raise NotImplementedError
        return self.timestamp == other.timestamp

    def __hash__(self):
        return hash((type(self), self.timestamp))


def to_file(*new_entries: Reading) -> None:
    contents = set(new_entries) | from_file()
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
                    value=Decimal(entry["Value"]),
                ),
            )
    return output
