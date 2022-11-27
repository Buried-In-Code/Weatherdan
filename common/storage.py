__all__ = ["Reading", "to_file", "from_file"]

import csv
from dataclasses import dataclass, field
from datetime import date

from common import get_project_root

DATA_FILE = get_project_root() / "data.csv"


@dataclass
class Reading:
    timestamp: date
    device: str = "GW1100"
    value: float = field(default=0.0, compare=False, hash=False)

    def __post_init__(self):
        if not self.device:
            self.device = "GW1100"

    def __lt__(self, other):
        if not isinstance(other, Reading):
            raise NotImplementedError()
        if self.device != other.device:
            return self.device < other.device
        return self.timestamp < other.timestamp

    def __eq__(self, other):
        if not isinstance(other, Reading):
            raise NotImplementedError()
        return (self.device, self.timestamp) == (other.device, other.timestamp)

    def __hash__(self):
        return hash((type(self), self.device, self.timestamp))


def to_file(*new_entries: Reading):
    contents = set(new_entries) | from_file()
    with DATA_FILE.open("w", encoding="UTF-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["Device", "Timestamp", "Value"])
        for entry in sorted(contents, key=lambda x: x.timestamp, reverse=True):
            writer.writerow([entry.device, entry.timestamp.isoformat(), entry.value])


def from_file() -> set[Reading]:
    output = set()
    if not DATA_FILE.exists():
        return output
    with DATA_FILE.open("r", encoding="UTF-8") as stream:
        reader = csv.DictReader(stream)
        for entry in reader:
            output.add(
                Reading(
                    device=entry["Device"] if "Device" in entry else None,
                    timestamp=date.fromisoformat(entry["Timestamp"]),
                    value=float(entry["Value"]),
                )
            )
    return output
